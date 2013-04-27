'''
Created on 17 Nov 2010

@author: hannes
'''

import unittest

import test_rfh2
import test_h2py
import test_rfh2_put_get

h2py_suite =  unittest.TestLoader().loadTestsFromTestCase(test_h2py.Testh2py)

rfh2_suite = unittest.TestLoader().loadTestsFromTestCase(test_rfh2.TestRFH2)
rfh2_put_get_suite = unittest.TestLoader().loadTestsFromTestCase(test_rfh2_put_get.TestRFH2PutGet)

all_suite = unittest.TestSuite([h2py_suite, rfh2_suite])

mq_not_required_tests = [h2py_suite, rfh2_suite]
mq_required_tests = [rfh2_put_get_suite]

mq_not_required_suite = unittest.TestSuite(mq_not_required_tests)
mq_required_suite = unittest.TestSuite(mq_required_tests)

unittest.TextTestRunner(verbosity=2).run(mq_not_required_suite)
unittest.TextTestRunner(verbosity=2).run(mq_required_suite)
