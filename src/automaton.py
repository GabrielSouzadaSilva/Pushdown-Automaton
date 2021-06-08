import copy
dictionary = {'Symbols': ['a', 'b'], 'States': ['q0', 'q1', 'qf'],
              'Initial State': 'q0', 'Final States': ['qf'], 'Stack Symbols': ['A', 'B']}

Rules = [{'origin_state': 'q0', 'word_read_symbol': 'a', 'stack_read_symbol': '-', 'final_state': 'q0', 'stack_written_symbol': 'B'},
         {'origin_state': 'q0', 'word_read_symbol': 'b', 'stack_read_symbol': 'B', 'final_state': 'q1', 'stack_written_symbol': '-'},
         {'origin_state': 'q0', 'word_read_symbol': '?', 'stack_read_symbol': '?', 'final_state': 'qf', 'stack_written_symbol': '-'},
         {'origin_state': 'q1', 'word_read_symbol': 'b', 'stack_read_symbol': 'B', 'final_state': 'q1', 'stack_written_symbol': '-'},
         {'origin_state': 'q1', 'word_read_symbol': '?', 'stack_read_symbol': '?', 'final_state': 'qf', 'stack_written_symbol': '-'}]

dictionary2 = {'Symbols': ['a', 'b'], 'States': ['q0', 'q1', 'qf'],
               'Initial State': 'q0', 'Final States': ['qf'], 'Stack Symbols': ['A', 'B']}

Rules2 = [{'origin_state': 'q0', 'word_read_symbol': 'a', 'stack_read_symbol': '-', 'final_state': 'q0', 'stack_written_symbol': 'A'},
          {'origin_state': 'q0', 'word_read_symbol': 'b', 'stack_read_symbol': '-', 'final_state': 'q0', 'stack_written_symbol': 'B'},
          {'origin_state': 'q0', 'word_read_symbol': '-', 'stack_read_symbol': '-', 'final_state': 'q1', 'stack_written_symbol': '-'},
          {'origin_state': 'q1', 'word_read_symbol': 'a', 'stack_read_symbol': 'A', 'final_state': 'q1', 'stack_written_symbol': '-'},
          {'origin_state': 'q1', 'word_read_symbol': 'b', 'stack_read_symbol': 'B', 'final_state': 'q1', 'stack_written_symbol': '-'},
          {'origin_state': 'q1', 'word_read_symbol': '?', 'stack_read_symbol': '?', 'final_state': 'qf', 'stack_written_symbol': '-'}]

Word = 'aaabbb'
Word2 = 'abaabaabaaba'


class Stack:
    def __init__(self):
        self.values = []

    def __repr__(self) -> str:
        return str(self.values)

    def addValue(self, value):
        self.values.append(value)

    def readValue(self):
        self.values.pop()

    def peek(self):
        if not self.checkEmpty():
            return self.values[-1]

    def checkEmpty(self) -> bool:
        if len(self.values) == 0:
            return True
        return False


class Automaton:
    def __init__(self, word, grammar, rules):

        self.stack = Stack()

        self.symbols = grammar['Symbols']
        self.states = grammar['States']
        self.initial = grammar['Initial State']
        self.final = grammar['Final States']
        self.stack_sym = grammar['Stack Symbols']

        self.word = word
        self.actual_state = self.initial
        self.rules = rules

        self.ch_count = 0
        self.fork = [{'ch_count': self.ch_count, 'state': self.actual_state, 'stack': self.stack, 'rule': None}]
        self.accepted = False

        self.runningWord(self.fork)
        while not self.accepted:
            print('\n\nanother attempt')
            self.runningWord(self.fork)
            if len(self.fork) == 0:
                break

    def runningWord(self, data):
        self.ch_count = data[0]['ch_count']
        self.actual_state = data[0]['state']
        self.stack = data[0]['stack']

        print('data   ', data)
        for letter in range(self.ch_count, len(self.word)+1):

            try:
                # print('text rules ', self.actual_state, self.word[letter])
                rules = self.checkRule(self.actual_state, self.word[letter], data[0]['rule'])
            except:
                # print('text rules -1', self.actual_state, 'fim')
                rules = self.checkRule(self.actual_state, '?', data[0]['rule'])

            if len(rules) > 0:
                #print(rules)
                self.actual_state = rules[0]['final_state']

                if rules[0]['stack_written_symbol'] != '-':
                    self.stack.addValue(rules[0]['stack_written_symbol'])

                if rules[0]['stack_read_symbol'] != '-':
                    # print('stack read ', self.stack.peek(), rules[0]['stack_read_symbol'])
                    if not self.stack.checkEmpty() and self.stack.peek() == rules[0]['stack_read_symbol']:
                        self.stack.readValue()
                    else:
                        break

                try:
                    if rules[0]['word_read_symbol'] == '-':
                        self.GUI('-', rules[0])
                    else:
                        self.GUI(self.word[letter], rules[0])
                except:
                    self.GUI('?', rules[0])

                if len(rules) > 1:
                    ch_count = copy.deepcopy(self.ch_count)
                    actual_state = copy.deepcopy(self.actual_state)
                    stack = copy.deepcopy(self.stack)
                    new_rules = copy.deepcopy(self.rules)
                    new_rules.remove(rules[0])  # remover a regra já usada

                    new_data = {'ch_count': ch_count,
                                'state': actual_state, 'stack': stack,
                                'rule': new_rules}  # self.rules[(self.rules.index(rules[1])):]
                    self.fork.append(new_data)

                # if rules[0]['word_read_symbol'] != '-':
                self.ch_count += 1

            else:
                # rules = self.checkRule(self.actual_state, '-', data[0]['rule'])
                # print('else len_rules  ', rules)
                break

        self.fork.pop(0)

        if self.stack.checkEmpty() and (self.actual_state in self.final):
            print('Accepted')
            self.accepted = True
        else:
            print('Refused')

    def checkRule(self, state, letter, rule=None) -> list:  # Checa se a letra se encaixa nas regras da gramática

        if rule is None:
            Rules_filtered = self.rules
        else:
            Rules_filtered = rule

        listRules = []

        for rule in Rules_filtered:
            if state == rule['origin_state']:

                if letter == rule['word_read_symbol']:
                    if letter == '?':
                        # print('check letter ?', self.ch_count, len(self.word))
                        if self.ch_count == len(self.word):  # checar se a apalavra foi processada
                            listRules.append(rule)

                    elif rule['stack_read_symbol'] == '?':
                        if self.stack.checkEmpty():
                            listRules.append(rule)

                    else:
                        listRules.append(rule)

                if rule['word_read_symbol'] == '-':
                    listRules.append(rule)

        # print('                    list rules ', listRules)
        return listRules

    def GUI(self, letter, rule):
        # print(self.ch_count, end='   ')
        print('\u03B4('+rule['origin_state']+', ' + letter + ', ' + rule['stack_read_symbol'] + ') = (' +
              rule['final_state'] + ', ' + rule['stack_written_symbol'] + ')', end='  ')
        print('Pilha:', self.stack)


Automaton(Word2, dictionary2, Rules2)
