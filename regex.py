import sys

class Regex(object):
    '''
    Wrapper for an NFA that corresponds to a given regular expression.
    This class is responsible for parsing the regular expression into a
    convenient string format and then constructing the NFA.
    '''
    def __init__(self, expr):
        '''
        Compiles an NFA given a regular expression pattern.
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
                # TODO detect '[' and skip up to ']', calling `literal`
                # with all characters in between
                nfa_stack.append(NFA.literal(c))


        self.nfa = nfa_stack.pop()

    @staticmethod
    def parse(expr):
        return Regex.convert_infix_to_post(Regex.insert_concat_operator(expr))

    @staticmethod
    def convert_infix_to_post(expr):
        '''
        Converts a regular expression with literal concat operator to
        postfix notation via Dijkstra's shunting-yard algorithm.
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
            if c in precedence:
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
            else:
                output_queue.append(c)

        while 0 != len(operator_stack):
            output_queue.append(operator_stack.pop())

        return ''.join(output_queue)

    @staticmethod
    def insert_concat_operator(expr):
        '''
        Inserts a literal concatenation operator '.' into a regular
        expression.
        '''
        converted = []
        ignore = False
        for index, c in enumerate(expr):
            converted.append(c)
            if index < len(expr)-1:
                c2 = expr[index+1]

                # treat [*] as a unit
                if c == '[':
                    ignore = True
                elif c == ']':
                    ignore = False

                if not ignore and c not in '(|' and c2 not in ')|*?+':
                    converted.append('.')

        return ''.join(converted)

    def test(self, string):
        return self.nfa.simulate(string)

class NFA(object):
    '''
    An NFA is a collection of linked state structures with a start state
    and a set of matching states. The NFA works by reading a string and
    updating a state list according to each state's out edges. The NFA
    accepts a string if the final state list contains a matching state,
    and rejects it otherwise. This class contains constructor methods
    corresponding to the regular operations. It can simulate the NFA
    given a string and decide whether the string is in the regular
    language it represents or not.
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
        # new start state uses out2 to connect to original machine, so
        # out1 can be written to by a concatenation operation
        new_start_state = State(out2=edge, is_match=True)
        for accept_state in nfa.accept_states:
            accept_state.out2 = Edge('', nfa.start_state)
        new_accept_states = nfa.accept_states
        new_accept_states.append(new_start_state)
        return NFA(new_start_state, new_accept_states)

    @staticmethod
    def question(nfa):
        '''
        "?": zero or one
        '''
        edge = Edge('', nfa.start_state)
        new_start_state = State(out2=edge, is_match=True)
        new_accept_states = nfa.accept_states
        new_accept_states.append(new_start_state)
        return NFA(new_start_state, new_accept_states)

    @staticmethod
    def plus(nfa):
        '''
        "+": one or more
        '''
        edge = Edge('', nfa.start_state)
        new_start_state = State(out2=edge, is_match=False)
        for accept_state in nfa.accept_states:
            accept_state.out2 = Edge('', nfa.start_state)
        return NFA(new_start_state, nfa.accept_states)

    @staticmethod
    def find_active_states(active_states, visited_states=[]):
        '''
        Recursively finds all states linked to a set of starting states
        by an epsilon edge (an edge whose `char` is empty string).
        '''
        def mark_as_visited(state):
            visited_states.append(state)

        def is_epsilon_edge(edge):
            return edge and edge.chars == ''

        def is_active(state):
            return state in active_states

        for state in active_states:

            mark_as_visited(state)

            if (is_epsilon_edge(state.out1)
                and not is_active(state.out1.to_state)):
                active_states.append(state.out1.to_state)
            if (is_epsilon_edge(state.out2)
                and not is_active(state.out2.to_state)):
                active_states.append(state.out2.to_state)

        # if there are any active_states that have not been visited,
        # follow their epsilon edges
        unvisited_states = [state for state in active_states if state not
                            in visited_states]
        if len(unvisited_states) > 0:
            return find_active_states(active_states, visited_states)

        return active_states

    def simulate(self, string):
        '''
        Starting from self.start_state, simulates the NFA.
        Returns True if the NFA accepts the string, otherwise False.
        '''
        active_states = NFA.find_active_states([self.start_state])

        for c in string:
            next_states = []
            for state in active_states:
                # NOTE should this logic be in Edge?
                if state.out1 and c in state.out1.chars:
                    next_states.append(state.out1.to_state)
                if state.out2 and c in state.out2.chars:
                    next_states.append(state.out2.to_state)

            active_states = NFA.find_active_states(next_states)

        for state in active_states:
            if state.is_match:
                return True

        return False

class State(object):
    '''
    Each state is a node defined by its out edges. A state may be an
    accept state or not.
    '''
    def __init__(self, out1=None, out2=None, is_match=False):
        self.out1 = out1
        self.out2 = out2
        self.is_match = is_match

class Edge(object):
    '''
    An edge has a character (which may be the empty string) and a target
    state (which may be None in the case of dangling edges).
    '''
    def __init__(self, chars, to_state=None):
        self.to_state = to_state
        self.chars = chars

def main():
    if len(sys.argv) > 2:
        re = Regex(sys.argv[1])
        for word in sys.argv[2:]:
            if re.test(word):
                print(word)
    else:
        raise Exception('Please provide a regular expression and at \
                        least one string to test')

if __name__ == '__main__':
    main()

