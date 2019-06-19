import sys

class RegEx(object):
    def __init__(self, pattern):
        self.nfa = NFA(pattern)

    def test(self, string):
        return self.nfa.simulate(string)

class NFA(object):
    '''
    An NFA is a collection of linked state structures with a start
    state and a set of matching states.
    The NFA works by reading a string and updating a state list
    according to each state's set of out arrows.
    The NFA accepts a string if the final state list contains a
    matching state, and rejects it otherwise.
    '''
    def __init__(self, regex):
        '''
        Compile an NFA given a regular expression.
        '''

        for c in regex:
            if c == '(':
                pass
            elif c == ')':
                pass
            elif c == '|':
                self.alternate()
            elif c == '*':
                self.star()
            elif c == '+':
                self.plus()
            elif c == '?':
                self.question()
            else:
                pass

    def literal(self, c):
        '''
        Returns an NFA for a literal character
        '''
        pass

    def concat(self, f1, f2):
        '''
        Concatenation
        Returns an NFA connecting the out arrows of f1 to the
        start state of f2
        '''
        pass

    def alternate(self, f1, f2):
        '''
        Alternation
        Returns an NFA with a new start state with arrows pointing
        to both f1 and f2
        '''
        pass

    def question(self, f):
        '''
        "?": zero or one
        Returns an NFA with a new start state pointing to both f
        and the empty path
        '''
        pass

    def star(self):
        '''
        "*": zero or more
        Returns an NFA with a new start state pointing to both f
        and the empty path, with f.out pointing back to f.start_state
        '''
        pass

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
    Each state is defined by its out arrows.
    '''
    def __init__(self, out1=None, out2=None, is_match=False):
        self.out1 = out1
        self.out2 = out2
        self.is_match = is_match

    def __str__(self):
        return 'State(out1: {}, out2: {})'.format(self.out1, self.out2)

    def __repr__(self):
        return self.__str__()

class Arrow(object):
    '''
    An arrow has a character (which may be the empty string)
    and a target state (which may be None in the case of dangling
    arrows).
    '''
    def __init__(self, char, to_state=None):
        self.to_state = to_state
        self.char = char

    def __str__(self):
        return 'Arrow(char: {}, to_state: {})'.format(self.char, self.to_state)

    def __repr__(self):
        return self.__str__()

def main():
    if len(sys.argv) > 2:
        re = RegEx(sys.argv[1])
        print(re.test(sys.argv[2]))
    else:
        raise Exception('Please provide a regular expression and a string to test')

if __name__ == '__main__':
    main()

