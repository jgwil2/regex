import unittest

from regex import Regex

class TestLiteral(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('b'))

class TestConcatenation(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('ab')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('ab'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.regex.test('ac'))

class TestUnion(unittest.TestCase):

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

class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a?')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test(''))
        self.assertTrue(self.regex.test('a'))

    def test_fails_string_not_in_language(self):
        self.assertTrue(self.regex.test('aa'))
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('aab'))

class TestPlus(unittest.TestCase):

    def setUp(self):
        self.regex = Regex('a+')

    def test_passes_string_in_language(self):
        self.assertTrue(self.regex.test('a'))
        self.assertTrue(self.regex.test('aaa'))

    def test_fails_string_not_in_language(self):
        self.assertTrue(self.regex.test(''))
        self.assertFalse(self.regex.test('ab'))
        self.assertFalse(self.regex.test('aab'))

if __name__ == '__main__':
    unittest.main()
