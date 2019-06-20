import unittest

from regex import NFA, RegEx

class TestConcatenation(unittest.TestCase):

    def setUp(self):
        self.nfa = NFA('ab')

    def test_passes_string_in_language(self):
        self.assertTrue(self.nfa.simulate('ab'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.nfa.simulate('ac'))

class TestUnion(unittest.TestCase):

    def setUp(self):
        self.nfa = NFA('a|b')

    def test_passes_string_in_language(self):
        self.assertTrue(self.nfa.simulate('a'))
        self.assertTrue(self.nfa.simulate('b'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.nfa.simulate('c'))

class TestStar(unittest.TestCase):

    def setUp(self):
        self.nfa = NFA('a*')

    def test_passes_string_in_language(self):
        self.assertTrue(self.nfa.simulate(''))
        self.assertTrue(self.nfa.simulate('a'))
        self.assertTrue(self.nfa.simulate('aaa'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.nfa.simulate('ab'))
        self.assertFalse(self.nfa.simulate('aab'))

class TestPlus(unittest.TestCase):

    def setUp(self):
        self.nfa = NFA('a+')

    def test_passes_string_in_language(self):
        self.assertTrue(self.nfa.simulate('a'))
        self.assertTrue(self.nfa.simulate('aaa'))

    def test_fails_string_not_in_language(self):
        self.assertTrue(self.nfa.simulate(''))
        self.assertFalse(self.nfa.simulate('ab'))
        self.assertFalse(self.nfa.simulate('aab'))

if __name__ == '__main__':
    unittest.main()
