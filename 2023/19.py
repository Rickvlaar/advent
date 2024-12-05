from util import console, parse_file_as_list, time_function
from copy import deepcopy
from dataclasses import field, dataclass

test_file = parse_file_as_list('input/19_test.txt')
day_file = parse_file_as_list('input/19.txt')


@dataclass
class SubRule:
    category: str
    operator: str
    limit_value: int
    return_value: str
    cat_ranges: dict = None
    parent_sub_rule: 'SubRule' = None
    parent_workflow_rule: 'WorkflowRule' = None
    is_end_state: bool = False
    part_accepted: bool = False


@dataclass
class WorkflowRule:
    name: str
    fallback: str
    rules: list[SubRule] = field(default_factory=list)


@time_function()
def run_a(file: list[str]):
    rules_dict, part_descriptions = convert_file_to_workflow_rules_and_parts(file)

    total_part_ratings = 0
    for part_description in part_descriptions:
        part_rating = 0
        accepted = evaluate_part(rules_dict, part_description)
        if accepted:
            part_rating = sum(part_description.values())
        total_part_ratings += part_rating

    return total_part_ratings


@time_function()
def run_b(file: list[str]):
    initial_category_ratings = {
            'x': [1, 4000],
            'm': [1, 4000],
            'a': [1, 4000],
            's': [1, 4000]
    }

    workflow_rules_dict = convert_file_to_workflow_rules_dict(file)
    end_states = []

    start_rule = SubRule(
            return_value='in',
            operator=None,
            limit_value=None,
            category=None
    )
    # for sub_rule in workflow_rules_dict.get('in').rules:
    #     sub_rule.parent_workflow_rule = workflow_rules_dict.get('in')
    evaluate_sub_rule(start_rule, workflow_rules_dict, end_states, initial_category_ratings)

    all_totals = 0

    for end_state in end_states:
        if not end_state.part_accepted:
            continue
        totals = 1
        for category, value_range in end_state.cat_ranges.items():
            diff = value_range[1] - value_range[0] + 1
            totals *= diff
        all_totals += totals

    return all_totals


def evaluate_sub_rule(from_rule: SubRule, workflow_rules_dict: dict[str: WorkflowRule], end_states: list,
                      initial_category_ratings):
    work_flow_rule = workflow_rules_dict.get(from_rule.return_value)

    new_category_ratings = deepcopy(initial_category_ratings)

    for rule in work_flow_rule.rules:
        sub_rule = deepcopy(rule)
        sub_rule.parent_sub_rule = from_rule
        sub_rule.parent_workflow_rule = work_flow_rule

        # apply rule condition
        if rule.limit_value:
            sub_rule_cat_ratings = deepcopy(new_category_ratings)
            category_rating_rule = sub_rule_cat_ratings.get(rule.category)
            category_rating_other_rules = new_category_ratings.get(rule.category)
            if category_rating_rule[0] < rule.limit_value < category_rating_rule[1]:
                if rule.operator == '>':
                    # limit value is within range, discard lower part
                    category_rating_rule[0] = rule.limit_value + 1
                    category_rating_other_rules[1] = rule.limit_value
                if rule.operator == '<':
                    # limit value is within range, discard higher part
                    category_rating_rule[1] = rule.limit_value - 1
                    category_rating_other_rules[0] = rule.limit_value

            sub_rule.cat_ranges = sub_rule_cat_ratings
        else:
            sub_rule.cat_ranges = new_category_ratings
        # pass adjusted ratings dict to next iteration

        if rule.return_value in {'A', 'R'}:
            sub_rule.is_end_state = True
            sub_rule.part_accepted = rule.return_value == 'A'
            end_states.append(sub_rule)
        else:
            evaluate_sub_rule(sub_rule, workflow_rules_dict, end_states, sub_rule.cat_ranges)


def evaluate_part(rules_dict: dict[str: callable], part_description: dict[str: int]):
    return_val = 'in'
    while return_val not in {'A', 'R'}:
        return_val = rules_dict[return_val](part_description)

    return True if return_val == 'A' else False


def convert_file_to_workflow_rules_dict(file: list[str]) -> dict[str: WorkflowRule]:
    workflow_rules_dict = dict()
    for index, line in enumerate(file):
        if not line:
            break

        rule_name, rules_string = line[:-1].split('{')
        rules = rules_string.split(',')
        sub_rules = get_sub_rules(rules[:-1])

        fallback_rule = rules[-1]
        sub_rules.append(SubRule(category=None, operator=None, limit_value=None, return_value=fallback_rule))

        workflow_rule = WorkflowRule(
                name=rule_name,
                rules=sub_rules,
                fallback=fallback_rule
        )
        workflow_rules_dict[workflow_rule.name] = workflow_rule
    return workflow_rules_dict


def get_sub_rules(rules: list[str]):
    return [SubRule(category=rule[0], operator=rule[1], limit_value=int(rule[2:]), return_value=result) for rule, result
            in [rule_string.split(':') for rule_string in rules]]


def convert_file_to_workflow_rules_and_parts(file: list[str]):
    rules_dict = dict()

    start_part_parsing_from_ind = 0
    for index, line in enumerate(file):
        if not line:
            start_part_parsing_from_ind = index + 1
            break

        rule_name, rules_string = line[:-1].split('{')
        rules = rules_string.split(',')
        fallback_rule = rules[-1]

        func_name = f'check_{rule_name}'
        func_call = f'def {func_name}(rule: dict[str: int]) -> bool:'

        for rule_string in rules[:-1]:
            rule, result = rule_string.split(':')
            category = rule[0]
            operator_symbol = rule[1]
            compared_value = rule[2:]

            rule_func = f'''
                category_value = rule['{category}']
                if category_value {operator_symbol} {compared_value}:
                    return '{result}'
            '''

            func_call += rule_func

        fall_back_func_part = f'''    else:
                    return '{fallback_rule}'
        '''

        func_call += fall_back_func_part
        exec(func_call)

        rules_dict[rule_name] = eval(func_name)

    part_descriptions = []
    for part_description in file[start_part_parsing_from_ind:]:
        part_description = part_description.replace('=', '\':')
        part_description = part_description.replace(',', ',\'')
        part_description = part_description.replace('{', '{\'')
        part_description_dict = eval(part_description)
        part_descriptions.append(part_description_dict)
    return rules_dict, part_descriptions


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
