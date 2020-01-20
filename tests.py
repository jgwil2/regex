import unittest

from regex import Regex, Token

class TestExpressionParser(unittest.TestCase):

    def test_insert_concat_operator(self):
        self.assertEqual(Regex.insert_concat_operator('ab'), 'a.b')
        self.assertEqual(Regex.insert_concat_operator('abc'), 'a.b.c')
        self.assertEqual(Regex.insert_concat_operator('ab*'), 'a.b*')
        self.assertEqual(Regex.insert_concat_operator('a((abc)*c)*'), 'a.((a.b.c)*.c)*')
        self.assertEqual(Regex.insert_concat_operator('(ab)*(cd)*'), '(a.b)*.(c.d)*')
        self.assertEqual(Regex.insert_concat_operator('a(bb)+a'), 'a.(b.b)+.a')
        self.assertEqual(Regex.insert_concat_operator('a[a-z]+a'), 'a.[a-z]+.a')

    def test_convert_infix_to_post(self):
        self.assertEqual(Regex.convert_infix_to_post('a.b'), 'ab.')
        self.assertEqual(Regex.convert_infix_to_post('a.b.c'), 'ab.c.')
        self.assertEqual(Regex.convert_infix_to_post('a.b*'), 'ab*.')
        self.assertEqual(Regex.convert_infix_to_post('a.((a.b.c)*.c)*'), 'aab.c.*c.*.')
        self.assertEqual(Regex.convert_infix_to_post('(a.b)*.(c.d)*'), 'ab.*cd.*.')
        self.assertEqual(Regex.convert_infix_to_post('a.(b.b)+.a'), 'abb.+.a.')
        self.assertEqual(Regex.convert_infix_to_post('a.[a-z]+.a'), 'a[a-z]+.a.')

    def test_tokenize(self):
        self.assertEqual(Regex.tokenize('ab.'), [Token('literal', 'a'), Token('literal', 'b'), Token('.')])
        self.assertEqual(Regex.tokenize('ab.c.'), [Token('literal', 'a'), Token('literal', 'b'), Token('.'), Token('literal', 'c'), Token('.')])
        self.assertEqual(Regex.tokenize('ab*.'), [Token('literal', 'a'), Token('literal', 'b'), Token('*'), Token('.')])
        self.assertEqual(Regex.tokenize('a[a-z]+.a.'), [Token('literal', 'a'), Token('literal', 'a-z'), Token('+'), Token('.'), Token('literal', 'a'), Token('.')])

class TestLiteral(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test(''))
        self.assertFalse(self.regex.test('b'))

class TestConcatenation(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('ab')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('ab'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test(''))
        self.assertFalse(self.regex.test('ac'))

class TestBinaryUnion(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a|b')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('b'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('c'))

class TestStar(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a*')

    def test_constructs_correct_machine(self):
        self.assertTrue(self.regex.nfa.start_state.is_match)
        self.assertTrue(self.regex.nfa.start_state.out2.token.value == '')
        self.assertTrue(self.regex.nfa.start_state.out2.to_state.out1.token.value == 'a')
        self.assertTrue(self.regex.nfa.start_state.out2.to_state.out1.to_state.is_match)
        self.assertTrue(self.regex.nfa.start_state.out2.to_state.out1.to_state.out2.token.value == '')
        self.assertTrue(self.regex.nfa.start_state.out2.to_state.out1.to_state.out2.to_state ==
                        self.regex.nfa.start_state.out2.to_state)

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test(''))
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('aaa'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('aab'))

class TestConcatStar(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('ab*')

    def test_constructs_correct_machine(self):
        self.assertFalse(self.regex.nfa.start_state.is_match)
        self.assertTrue(self.regex.nfa.start_state.out1.token.value == 'a')
        self.assertTrue(self.regex.nfa.start_state.out1.to_state.out1.token.value == '')
        self.assertTrue(self.regex.nfa.start_state.out1.to_state.out1.to_state.is_match)
        self.assertTrue(self.regex.nfa.start_state.out1.to_state.out1.to_state.out2.token.value == '')
        self.assertFalse(self.regex.nfa.start_state.out1.to_state.out1.to_state.out2.to_state.is_match)
        self.assertTrue(self.regex.nfa.start_state.out1.to_state.out1.to_state.out2.to_state.out1.token.value == 'b')
        self.assertTrue(self.regex.nfa.start_state.out1.to_state.out1.to_state.out2.to_state.out1.to_state.is_match)
        self.assertTrue(self.regex.nfa.start_state.out1.to_state.out1.to_state.out2.to_state.out1.to_state.out2.token.value ==
                        '')
        self.assertTrue(self.regex.nfa.start_state.out1.to_state.out1.to_state.out2.to_state.out1.to_state.out2.to_state ==
                        self.regex.nfa.start_state.out1.to_state.out1.to_state.out2.to_state)

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('ab'))
        self.assertTrue(self.regex.test('abb'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('aab'))

class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a?')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test(''))
        self.assertTrue(self.regex.test('a'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('aa'))
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('aab'))

class TestConcatQuestion(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('ab?')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('ab'))
        self.assertTrue(self.regex.test('ab'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('abb'))
        self.assertFalse(self.regex.test('aab'))

class TestPlus(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a+')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('aaa'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test(''))
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('aab'))

class TestParensStar(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('(ab)*')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test(''))
        self.assertTrue(self.regex.test('ab'))
        self.assertTrue(self.regex.test('abab'))
        self.assertTrue(self.regex.test('ababab'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('aba'))
        self.assertFalse(self.regex.test('ababc'))

class TestParensUnion(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('(a|b)*')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test(''))
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('abbbaaab'))
        self.assertTrue(self.regex.test('abbbaaab'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('abc'))
        self.assertFalse(self.regex.test('abbaac'))

class TestParensConcat(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('(ab)c')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('abc'))
        self.assertTrue(self.regex.test('abc'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test(''))
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('aab'))

class TestParensStarConcat(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('(ab)*a')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('aba'))
        self.assertTrue(self.regex.test('ababa'))
        self.assertTrue(self.regex.test('abababa'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('abc'))

class TestParensQuestionConcat(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('(ab)?a')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('aba'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('abc'))
        self.assertFalse(self.regex.test('ababa'))

class TestParensPlusConcat(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('(ab)+c')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('abc'))
        self.assertTrue(self.regex.test('ababc'))
        self.assertTrue(self.regex.test('abababc'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('a'))
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('aba'))
        self.assertFalse(self.regex.test('abab'))

class TesttRange(unittest.TestCase):

    def test_uppercase_letters_range(self):
        regex = Regex('[A-Z]')
        self.assertTrue(self.regex.test('A'))
        self.assertTrue(self.regex.test('M'))
        self.assertTrue(self.regex.test('Z'))
        self.assertFalse(self.regex.test('a'))
        self.assertFalse(self.regex.test('m'))
        self.assertFalse(self.regex.test('z'))

    def test_lowercase_letters_range(self):
        regex = Regex('[a-z]')
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('m'))
        self.assertTrue(self.regex.test('z'))
        self.assertFalse(self.regex.test('A'))
        self.assertFalse(self.regex.test('M'))
        self.assertFalse(self.regex.test('Z'))

if __name__ == '__main__':
    unittest.main()
