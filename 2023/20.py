from util import console, parse_file_as_list, time_function
from dataclasses import field, dataclass

test_file = parse_file_as_list('input/20_test.txt')
day_file = parse_file_as_list('input/20.txt')


# high pulse == 1
# low pulse == 0
@dataclass
class Runner:
    queue: list['Module'] = field(default_factory=list)
    next_queue: list['Module'] = field(default_factory=list)
    pulse_statusses: list[bool] = field(default_factory=list)
    modules_dict: dict[str:'Module'] = field(default_factory=dict)
    pulse_count: int = 0
    max_pulse_count: int = 1000
    button_presses = 0
    low_pulses: int = 0
    high_pulses: int = 0

    def run(self):
        first_module = self.modules_dict['broadcaster']

        while True:
            self.button_presses +=1
            self.low_pulses += 1
            first_module.received_pulse_type = 0
            self.queue.append(('', first_module.name, 0))
            self.pulse()


    def pulse(self):
        while self.queue:
            source_module, target_module, pulse_type = self.queue.pop(0)
            if source_module == 'xn' and pulse_type == 1:
                console.print('xn: ' + str(self.button_presses))
            if source_module == 'qn' and pulse_type == 1:
                console.print('qn: ' + str(self.button_presses))
            if source_module == 'xf' and pulse_type == 1:
                console.print('xf: ' + str(self.button_presses))
            if source_module == 'zl' and pulse_type == 1:
                console.print('zl: ' + str(self.button_presses))
            # if target_module == 'th' and pulse_type == 0:
            #     console.print('th: ' + str(self.button_presses))
            # 224046542165867

            module = self.modules_dict[target_module]
            module.receive_pulse(pulse_type, source_module)
            module.handle_pulse()
            module.send_pulse()

    def record_pulse(self, pulse_type: int):
        if pulse_type:
            self.high_pulses += 1
        else:
            self.low_pulses += 1

    def print_pulse_counts(self):
        console.print(f'low pulses: {self.low_pulses}, high pulses: {self.high_pulses}')
        return self.low_pulses * self.high_pulses


@dataclass
class Module:
    name: str
    pulsed: bool = False
    received_pulse_type: int = None
    connected_modules: dict[str: 'Module'] = field(default_factory=dict)
    connected_modules_list: list[str] = field(default_factory=list)
    runner: Runner = None

    def receive_pulse(self, pulse_type: int, source_module: 'Module'):
        self.received_pulse_type = pulse_type

    def handle_pulse(self):
        self.pulsed = False

    def send_pulse(self):
        self.pulsed = True
        for module in self.connected_modules:
            self.runner.record_pulse(self.received_pulse_type)
            self.enqueue_pulse(self.name, module, self.received_pulse_type)

    def enqueue_pulse(self, source_module: str, target_module: str, pulse_type: int):
        self.runner.queue.append((source_module, target_module, pulse_type))


@dataclass
class FlipFlop(Module):
    is_on: bool = False
    should_pulse = False

    def handle_pulse(self):
        self.pulsed = False
        if self.received_pulse_type == 0:
            self.is_on = not self.is_on
            self.should_pulse = True
        else:
            self.should_pulse = False

    def send_pulse(self):
        if self.should_pulse:
            self.pulsed = True
            pulse_type = 1 if self.is_on else 0
            for module in self.connected_modules:
                self.runner.record_pulse(pulse_type)
                self.enqueue_pulse(self.name, module, pulse_type)


@dataclass
class Conjunction(Module):
    should_pulse = False
    received_modules_pulse_types: dict[str:int] = field(default_factory=dict)
    input_modules_pulse_types: dict[str:int] = field(default_factory=dict)

    def receive_pulse(self, pulse_type: int, source_module: str):
        self.received_modules_pulse_types[source_module] = pulse_type

    def handle_pulse(self):
        self.pulsed = False
        if self.received_modules_pulse_types:
            for module, pulse_type in self.received_modules_pulse_types.items():
                self.input_modules_pulse_types[module] = pulse_type
            self.received_modules_pulse_types.clear()
            self.should_pulse = True
        else:
            self.should_pulse = False

    def send_pulse(self):
        if self.should_pulse:
            pulse_type = 0 if all(self.input_modules_pulse_types.values()) else 1
            self.pulsed = True
            for module in self.connected_modules:
                self.runner.record_pulse(pulse_type)
                self.enqueue_pulse(self.name, module, pulse_type)


@dataclass
class Output(Module):
    def handle_pulse(self):
        if self.received_pulse_type == 0:
            console.print(self.runner.max_pulse_count)
            self.runner.rx_pulses += 1

    def send_pulse(self):
        pass


@time_function()
def run_a(file: list[str]):
    modules_dict = convert_file_to_modules(file)
    output = Output(
            name='rx',
    )
    modules_dict['rx'] = output

    runner = Runner()
    modules_dict = prepare_modules(modules_dict, runner)

    runner.modules_dict = modules_dict

    runner.run()
    return runner.print_pulse_counts()


@time_function()
def run_b(file: list[str]):
    pass


def prepare_modules(modules_dict, runner):
    for name, module in modules_dict.items():
        module.runner = runner
        for connected_module_name in module.connected_modules_list:
            module.connected_modules[connected_module_name] = modules_dict[connected_module_name]

    for name, module in modules_dict.items():
        if str(module.__class__.__name__) == 'Conjunction':
            for input_module in modules_dict.values():
                if module.name == input_module.name:
                    continue
                if name in input_module.connected_modules_list:
                    module.input_modules_pulse_types[input_module.name] = 0

    return modules_dict


def convert_file_to_modules(file: list[str]):
    modules_dict = dict()
    for line in file:
        module_name, connected_modules = line.split(' -> ')

        connected_modules = connected_modules.split(', ')
        module_type_char = module_name[0]
        module_name = module_name[1:]

        # Flipflop
        if module_type_char == '%':
            flipflop = FlipFlop(
                    name=module_name,
                    connected_modules_list=connected_modules
            )
            modules_dict[module_name] = flipflop
        # Conjunction
        elif module_type_char[0] == '&':
            conjunction = Conjunction(
                    name=module_name,
                    connected_modules_list=connected_modules
            )
            modules_dict[module_name] = conjunction
        else:
            broadcaster = Module(
                    name='broadcaster',
                    connected_modules_list=connected_modules
            )
            modules_dict['broadcaster'] = broadcaster
    return modules_dict


if __name__ == '__main__':
    answer_a = run_a(day_file)

    answer_b = run_b(test_file)

    console.print(f'solution A: {answer_a}')
    console.print(f'solution B: {answer_b}')
