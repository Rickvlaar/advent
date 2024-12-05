from util import console, parse_file_as_list, time_function
from collections import Counter
from operator import itemgetter

test_file = parse_file_as_list('input/7_test.txt')
day_file = parse_file_as_list('input/7.txt')


@time_function()
def run_a(file: list[str]):
    card_rank_dict = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3,
                      '3': 2, '2': 1}

    hand_bet_list = get_hands_bet_dict(file, card_rank_dict)
    for hand in hand_bet_list:
        determine_hand_rank(hand)

    return sum([(index + 1) * hand['bet'] for index, hand in
                enumerate(sorted(hand_bet_list, key=itemgetter('hand_rank', 'hand_cards_ranked')))])


@time_function()
def run_b(file: list[str]):
    card_rank_dict = {'A': 13, 'K': 12, 'Q': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4,
                      '3': 3, '2': 2, 'J': 1}

    hand_bet_list = get_hands_bet_dict(file, card_rank_dict)
    for hand in hand_bet_list:
        determine_hand_rank(hand, True)

    return sum([(index + 1) * hand['bet'] for index, hand in
                enumerate(sorted(hand_bet_list, key=itemgetter('hand_rank', 'hand_cards_ranked')))])


def get_hands_bet_dict(file: list[str], card_rank_dict: dict[str:int]) -> list[dict[str:any]]:
    return [{'hand':              hand,
             'bet':               int(bet),
             'counter':           Counter(hand),
             'hand_cards_ranked': [card_rank_dict[card] for card in hand]
             } for hand, bet in [line.split(' ') for line in file]]


def determine_hand_rank(hand: dict[str:any], joker_style: bool = False):
    joker_bonus = 0
    if joker_style:
        if hand['counter']['J'] < 5:
            joker_bonus = hand['counter']['J']
            hand['counter']['J'] = 0

    # determine highest counter
    sorted_counter = hand['counter'].most_common()
    highest_count = sorted_counter[0][1] + joker_bonus

    if highest_count == 5:
        hand['hand_rank'] = 7
    elif highest_count == 4:
        hand['hand_rank'] = 6
    elif highest_count == 3 and sorted_counter[1][1] == 2:
        hand['hand_rank'] = 5
    elif highest_count == 3:
        hand['hand_rank'] = 4
    elif highest_count == 2 and sorted_counter[1][1] == 2:
        hand['hand_rank'] = 3
    elif highest_count == 2:
        hand['hand_rank'] = 2
    else:
        hand['hand_rank'] = 1


if __name__ == '__main__':
    answer_a = run_a(day_file)
    answer_b = run_b(day_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
