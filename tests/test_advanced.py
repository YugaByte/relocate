# -*- coding: utf-8 -*-

from .context import relocate

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(relocate.hmm())


if __name__ == '__main__':
    unittest.main()
