import copy


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
    def __init__(self, grammar, rules):

        self.stack = Stack()

        self.symbols = grammar['Symbols']
        self.states = grammar['States']
        self.initial = grammar['Initial State']
        self.final = grammar['Final States']
        self.stack_sym = grammar['Stack Symbols']

        self.word = input("Insira a palavra desejada: ")
        self.actual_state = self.initial
        self.rules = rules
        
        
        self.ch_count = 0
        self.fork = [{'ch_count': self.ch_count, 'state': self.actual_state, 'stack': self.stack, 'rule': None}]
        self.accepted = False
        
        
        self.checkValidity()


            
    
    def execute(self):
        
        counter = 0
        
        while not self.accepted:
            counter += 1
            print('\nTry #'+str(counter), end='\n')
            self.runningWord(self.fork)
            if len(self.fork) == 0:
                break
        
    

    def runningWord(self, data):
        self.ch_count = data[0]['ch_count']
        self.actual_state = data[0]['state']
        self.stack = data[0]['stack']

        letter = self.ch_count
        while letter < len(self.word)+1:

            try:
                rules = self.checkRule(self.actual_state, self.word[letter], data[0]['rule'])
            except:
                rules = self.checkRule(self.actual_state, '?', data[0]['rule'])

            if len(rules) > 0:
                
                if len(rules) > 1:
                    ch_count = copy.deepcopy(self.ch_count)
                    actual_state = copy.deepcopy(self.actual_state)
                    stack = copy.deepcopy(self.stack)
                    new_rules = copy.deepcopy(self.rules)
                    new_rules.remove(rules[0])  # remover a regra já usada

                    new_data = {'ch_count': ch_count,
                                'state': actual_state, 'stack': stack,
                                'rule': new_rules}
                    self.fork.append(new_data)
                    
                self.actual_state = rules[0]['final_state']

                if rules[0]['stack_written_symbol'] != '-':
                    self.stack.addValue(rules[0]['stack_written_symbol'])

                if rules[0]['stack_read_symbol'] in self.stack_sym:
                    if (not self.stack.checkEmpty()) and (self.stack.peek() == rules[0]['stack_read_symbol']):
                        self.stack.readValue()
                    else:
                        break

                if rules[0]['word_read_symbol'] == '-':
                    self.GUI('-', rules[0])
                elif rules[0]['word_read_symbol'] == '?':
                    self.GUI('?', rules[0])
                else:
                    self.GUI(self.word[letter], rules[0])
                    letter += 1
                    self.ch_count += 1

            else:
                break

        self.fork.pop(0)

        if self.stack.checkEmpty() and (self.actual_state in self.final):
            print('Accepted\n')
            self.accepted = True
        else:
            print('Refused\n')

    def checkRule(self, state, letter, rule=None) -> list:  # Checa se a letra se encaixa nas regras da gramática

        if rule == None:
            Rules_filtered = self.rules
        else:
            Rules_filtered = rule

        listRules = []

        for rule in Rules_filtered:
            if state == rule['origin_state']:

                if letter == rule['word_read_symbol']:
                    if letter == '?':

                        if self.ch_count == len(self.word):  # checar se a apalavra foi processada
                            listRules.append(rule)

                    elif rule['stack_read_symbol'] == '?':
                        if self.stack.checkEmpty():
                            listRules.append(rule)

                    else:
                        listRules.append(rule)

                if rule['word_read_symbol'] == '-':
                    listRules.append(rule)

        return listRules

    def GUI(self, letter, rule):
        
        print(self.ch_count, end='   ')
        print('\u03B4('+rule['origin_state']+', ' + letter + ', ' + rule['stack_read_symbol'] + ') = (' +
              rule['final_state'] + ', ' + rule['stack_written_symbol'] + ')', end='  ')
        print('Pilha:', self.stack)
        
    
    def checkValidity(self):
        
        for i in self.word:
            if i not in self.symbols:
                raise ValueError("Word doesn't exist in the grammar")
    
        





