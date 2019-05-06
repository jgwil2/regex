import sys

class RegEx(object):
    def __init__(self, pattern):
        self.nfa = NFA(pattern)

    def test(self, string):
        self.nfa.test(string)

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
        self.frag_stack = []
        self.start_state = State()
        self.current_states = set([self.start_state])
        for c in regex:
            if c == '(':
                pass
            if c == ')':
                pass
            if c == '|':
                self.alternate()
            if c == '*':
                self.star()
            if c == '+':
                self.plus()
            if c == '?':
                self.question()
            else:
                self.frag_stack.append(self.literal(c))

    def literal(self, c):
        '''
        Returns fragment for literal character
        '''
        return Fragment(State(Arrow(c)))

    def concat(self, f1, f2):
        '''
        Concatenation
        Returns a fragment connecting the out arrows of f1 to the
        start state of f2
        '''
        pass

    def alternate(self, f1, f2):
        '''
        Alternation
        Returns a fragment with a new start state with arrows pointing
        to both f1 and f2
        '''
        pass

    def question(self, f):
        '''
        "?": zero or one
        Returns a fragment with a new start state pointing to both f
        and the empty path
        '''
        pass

    def star(self):
        '''
        "*": zero or more
        Returns a fragment with a new start state pointing to both f
        and the empty path, with f.out pointing back to f.start_state
        '''
        pass

    def plus(self):
        '''
        "+": one or more
        '''
        pass

    def test(self, string):
        pass

class State(object):
    '''
    Each state is defined by its out arrows.
    '''
    def __init__(self, arrow1=None, arrow2=None):
        self.arrow1 = arrow1
        self.arrow2 = arrow2

class Fragment(object):
    '''
    A fragment is a partial NFA with dangling arrows. The arrows are
    the set of all out arrows of rightmost states in the fragment.
    '''
    def __init__(self, start_state):
        self.start_state = start_state

class Arrow(object):
    '''
    An arrow has a character (which may be the empty string)
    and a target state (which may be None in the case of dangling
    arrows).
    '''
    def __init__(self, c, to_state=None):
        self.to_state = to_state
        self.c = c

def main():
    if len(sys.argv) > 2:
        re = RegEx(sys.argv[1])
        import pdb;pdb.set_trace()
        re.test(sys.argv[2])
    else:
        raise Exception('Please provide a regular expression and a string to test')

if __name__ == '__main__':
    main()

