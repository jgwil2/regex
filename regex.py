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
        self.frag_stack = []

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
                # if there is something in the frag stack then we pop
                # it off the stack and patch all its out arrows to
                # point to the new frag's start state and push the new
                # fragment back onto the stack
                current = self.literal(c)
                if len(self.frag_stack) > 0:
                    previous = self.frag_stack.pop()
                    current = self.concat(previous, current)

                # FIXME
                # otherwise this is the first character we are reading,
                # so we simply push the fragment onto the stack and
                # track this fragment's start state
                self.start_state = current.start_state
                self.frag_stack.append(current)

        # at the end of the loop, we should create a match state
        # and connect it to remaining fragment(s?) in the stack
        final_state = State(None, None, True)
        frag = self.frag_stack.pop()
        self.patch(frag.out_arrows, final_state)

        self.start_state = frag.start_state

    def literal(self, c):
        '''
        Returns fragment for literal character
        '''
        arrow = Arrow(c)
        return Fragment(State(arrow), [arrow])

    def concat(self, f1, f2):
        '''
        Concatenation
        Returns a fragment connecting the out arrows of f1 to the
        start state of f2
        '''
        self.patch(f1.out_arrows, f2.start_state)
        return Fragment(f1.start_state, f2.out_arrows)

    def alternate(self, f1, f2):
        '''
        Alternation
        Returns a fragment with a new start state with arrows pointing
        to both f1 and f2
        '''
        to_f1 = Arrow('', f1)
        to_f2 = Arrow('', f2)
        return Fragment(State(to_f1, to_f2), [to_f1, to_f2])

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

    def patch(self, arrow_list, state):
        '''
        Procedure: take a list of arrows and a state and set each arrow
        to point to state.
        '''
        for arrow in arrow_list:
            arrow.to_state = state

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

class Fragment(object):
    '''
    A fragment is a partial NFA with dangling arrows. The arrows are
    the set of all out arrows of rightmost states in the fragment.
    Fragment only tracks a start state and a set of out arrows.
    '''
    def __init__(self, start_state, out_arrows=[]):
        self.start_state = start_state
        self.out_arrows = out_arrows

    def __str__(self):
        return 'Fragment(start_state: {}, out_arrows: {})'.format(self.start_state, self.out_arrows)

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

