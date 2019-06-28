import unittest

from regex import Regex

class TestExpressionParser(unittest.TestCase):

    def test_inserts_literal_concat_operator(self):
        self.assertEqual(Regex.insert_concat_operator('abc'), 'a.b.c')
        self.assertEqual(Regex.insert_concat_operator('a((abc)*c)*'), 'a.((a.b.c)*.c)*')
        self.assertEqual(Regex.insert_concat_operator('(ab)*(cd)*'), '(a.b)*.(c.d)*')

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

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('ab'))
        self.assertTrue(self.regex.test('abb'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('ab'))
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

if __name__ == '__main__':
    unittest.main()
