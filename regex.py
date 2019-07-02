import sys

class Regex(object):
    '''
    Wrapper for an NFA that corresponds to a given regular expression
    '''
    def __init__(self, expr):
        '''
        Compile an NFA given a regular expression pattern
        '''
        nfa_stack = []

        postfix_expr = Regex.parse(expr)

        for index, c in enumerate(postfix_expr):
            if c == '|':
                nfa1 = nfa_stack.pop()
                nfa2 = nfa_stack.pop()
                nfa_stack.append(NFA.union(nfa1, nfa2))
            elif c == '*':
                nfa_stack.append(NFA.star(nfa_stack.pop()))
            elif c == '+':
                nfa_stack.append(NFA.plus(nfa_stack.pop()))
            elif c == '?':
                nfa_stack.append(NFA.question(nfa_stack.pop()))
            elif c == '.':
                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                nfa_stack.append(NFA.concat(nfa1, nfa2))
            else:
                nfa_stack.append(NFA.literal(c))


        self.nfa = nfa_stack.pop()

    @staticmethod
    def parse(expr):
        return Regex.convert_infix_to_post(Regex.insert_concat_operator(expr))

    @staticmethod
    def convert_infix_to_post(expr):
        '''
        Convert a regular expression with literal concat operator to
        postfix notation via Dijkstra's shunting-yard algorithm
        '''
        precedence = {
            '*': 0,
            '?': 0,
            '+': 0,
            '.': 1,
            '|': 2
        }
        output_queue = []
        operator_stack = []

        def top_of_stack():
            return operator_stack[len(operator_stack)-1]

        for index, c in enumerate(expr):
            if c.isalnum():
                output_queue.append(c)
            elif c in precedence:
                while (0 != len(operator_stack)
                and '(' != top_of_stack()
                and precedence[c] >= precedence[top_of_stack()]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(c)
            elif '(' == c:
                operator_stack.append(c)
            elif ')' == c:
                while '(' != top_of_stack():
                    output_queue.append(operator_stack.pop())
                if '(' == top_of_stack():
                    operator_stack.pop()

        while 0 != len(operator_stack):
            output_queue.append(operator_stack.pop())

        return ''.join(output_queue)

    @staticmethod
    def insert_concat_operator(expr):
        '''
        Insert a literal concatenation operator '.' into a regular
        expression
        '''
        converted = []
        for index, c in enumerate(expr):
            converted.append(c)
            if index < len(expr)-1:
                c2 = expr[index+1]
                if c not in '(|' and c2 not in ')|*?+':
                    converted.append('.')

        return ''.join(converted)

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
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states

    @staticmethod
    def literal(c):
        '''
        Returns an NFA for a literal character
        '''
        accept_state = State(is_match=True)
        edge = Edge(c, accept_state)
        start_state = State(edge)
        return NFA(start_state, [accept_state])

    @staticmethod
    def concat(nfa1, nfa2):
        '''
        Concatenation
        '''
        start_state = nfa1.start_state
        accept_states = nfa2.accept_states
        for accept_state in nfa1.accept_states:
            accept_state.is_match = False
            accept_state.out1 = Edge('', nfa2.start_state)
        return NFA(start_state, accept_states)

    @staticmethod
    def union(nfa1, nfa2):
        '''
        Union
        '''
        edge1 = Edge('', nfa1.start_state)
        edge2 = Edge('', nfa2.start_state)
        start_state = State(out1=edge1, out2=edge2, is_match=False)
        return NFA(start_state, nfa1.accept_states + nfa2.accept_states)

    @staticmethod
    def star(nfa):
        '''
        "*": zero or more
        '''
        edge = Edge('', nfa.start_state)
        new_start_state = State(out1=edge, is_match=True)
        for accept_state in nfa.accept_states:
            accept_state.out1 = Edge('', nfa.start_state)
        return NFA(new_start_state, nfa.accept_states.append(new_start_state))

    @staticmethod
    def question(nfa):
        '''
        "?": zero or one
        '''
        edge = Edge('', nfa.start_state)
        new_start_state = State(out1=edge, is_match=True)
        return NFA(new_start_state, nfa.accept_states.append(new_start_state))

    @staticmethod
    def plus(nfa):
        '''
        "+": one or more
        '''
        edge = Edge('', nfa.start_state)
        new_start_state = State(out1=edge, is_match=False)
        for accept_state in nfa.accept_states:
            accept_state.out1 = Edge('', nfa.start_state)
        return NFA(new_start_state, nfa.accept_states)

    def simulate(self, string):
        '''
        Starting from self.start_state, simulate the NFA for the string
        '''
        active_states = [self.start_state]
        next_states = []
        for c in string:
            # FIXME this code will only follow empty char edges one
            # level deep. Find a more elegant way to make sure that all
            # empty char edges are followed!!
            for state in active_states:
                if state.out1 and state.out1.char == '':
                    active_states.append(state.out1.to_state)
                if state.out2 and state.out2.char == '':
                    active_states.append(state.out2.to_state)

            # after all edges whose char is '' have been followed,
            # iterate all active states, and if their out edges
            # match the char, follow the edges
            for state in active_states:
                if state.out1 and state.out1.char == c:
                    next_states.append(state.out1.to_state)
                if state.out2 and state.out2.char == c:
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
        return 'State(out1: {}, out2: {}, is_match: {})'.format(self.out1, self.out2, self.is_match)

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

