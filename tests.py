import unittest

from regex import NFA, RegEx

class TestConcatenation(unittest.TestCase):

    def setUp(self):
        self.nfa = NFA('abc')

    def test_passes_string_in_language(self):
        self.assertTrue(self.nfa.simulate('abc'))

    def test_fails_string_not_in_language(self):
        self.assertFalse(self.nfa.simulate('abd'))

if __name__ == '__main__':
    unittest.main()
