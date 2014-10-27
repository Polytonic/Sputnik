import unittest

class Test_Sample(unittest.TestCase):
    def setUp(self):
        self.simple_list = [1, 2, 3]

    def test_first(self):
        self.assertEqual(self.simple_list[0], 1)

    def test_length(self):
        self.assertEqual(len(self.simple_list), 3)

    @unittest.expectedFailure
    def test_failure(self):
        self.assertEqual(1, 2)

if __name__ == '__main__':
    unittest.main()
