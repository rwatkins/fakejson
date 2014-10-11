import unittest
from unittest import TestCase

import fakejson


class ParseArrayTest(TestCase):
    def test(self):
        self.assertEqual(fakejson.loads('["Hi"]'), ['Hi'])


if __name__ == '__main__':
    unittest.main()
