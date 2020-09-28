import unittest

import test_word
import test_dictionary
import test_game

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_word))
suite.addTests(loader.loadTestsFromModule(test_dictionary))
suite.addTests(loader.loadTestsFromModule(test_game))

runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)