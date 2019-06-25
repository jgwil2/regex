import sys

class Regex(object):
    '''

    '''
    def __init__(self, pattern):
        '''
        Compile an NFA given a regular expression.
        '''

        for c in pattern:
            if c == '(':
                pass
            elif c == ')':
                pass
            elif c == '|':
                self.nfa = NFA.alternate()
            elif c == '*':
                self.nfa = NFA.star()
            elif c == '+':
                self.nfa = NFA.plus()
            elif c == '?':
                self.nfa = NFA.question()
            else:
                self.nfa = NFA.literal(c)


    def test(self, string):
        return self.nfa.simulate(string)

class NFA(object):
    '''
    An NFA is a collection of linked state structures with a start
    state and a set of matching states.
    The NFA works by reading a string and updating a state list
    according to each state's set of out edges.
    The NFA accepts a string if the final state list contains a
    matching state, and rejects it otherwise.
    '''
    def __init__(self, start_state):
        self.start_state = start_state

    @staticmethod
    def literal(c):
        '''
        Returns an NFA for a literal character
        '''
        # TODO clean this up w/ named params
        end_state = State(None, None, True)
        edge = Edge(c, end_state)
        start_state = State(edge)
        return NFA(start_state)

    @staticmethod
    def concat(f1, f2):
        '''
        Concatenation
        '''
        pass

    @staticmethod
    def alternate(f1, f2):
        '''
        Alternation
        '''
        pass

    @staticmethod
    def question(f):
        '''
        "?": zero or one
        '''
        pass

    @staticmethod
    def star(self):
        '''
        "*": zero or more
        '''
        pass

    @staticmethod
    def plus(self):
        '''
        "+": one or more
        '''
        pass

    def simulate(self, string):
        '''
        Starting from self.start_state, simulate the NFA for the string
        '''
        active_states = [self.start_state]
        next_states = []
        for c in string:
            for state in active_states:
                if state.out1 and (state.out1.char == c or state.out1.char == ''):
                    next_states.append(state.out1.to_state)
                if state.out2 and (state.out2.char == c or state.out2.char == ''):
                    next_states.append(state.out2.to_state)
            active_states = next_states
            next_states = []

        for state in active_states:
            if state.is_match:
                return True

        return False

class State(object):
    '''
    Each state is defined by its out edges.
    '''
    def __init__(self, out1=None, out2=None, is_match=False):
        self.out1 = out1
        self.out2 = out2
        self.is_match = is_match

    def __str__(self):
        return 'State(out1: {}, out2: {})'.format(self.out1, self.out2)

    def __repr__(self):
        return self.__str__()

class Edge(object):
    '''
    An edge has a character (which may be the empty string)
    and a target state (which may be None in the case of dangling
    edges).
    '''
    def __init__(self, char, to_state=None):
        self.to_state = to_state
        self.char = char

    def __str__(self):
        return 'Edge(char: {}, to_state: {})'.format(self.char, self.to_state)

    def __repr__(self):
        return self.__str__()

def main():
    if len(sys.argv) > 2:
        re = Regex(sys.argv[1])
        print(re.test(sys.argv[2]))
    else:
        raise Exception('Please provide a regular expression and a string to test')

if __name__ == '__main__':
    main()

