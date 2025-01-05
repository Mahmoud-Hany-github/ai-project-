import unittest

class TestBasic(unittest.TestCase):
    def test_example(self):
        # A simple test case
        self.assertEqual(1 + 1, 2)

if __name__ == "__main__":
    unittest.main()
