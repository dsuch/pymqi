import unittest
from unittest.mock import Mock

class BaseIsolatedTest(unittest.TestCase):
    """ Test utility class to write unit tests without relying on pymqe and an MQ client """
    
    MQ_LEVELS = ('7.0')
        
    @classmethod
    def setUpClass(cls):
        super(BaseIsolatedTest, cls).setUpClass()
        
        # avoids loading C libs in unit tests 
        cls.mqe_mock = Mock()
        cls.mqe_mock.__mqlevels__ = cls.MQ_LEVELS
        cls.mqe_mock.__mqbuild__ = None
        
        import sys
        cls.original_mqe_module = sys.modules.get('pymqe') 
        sys.modules['pymqe'] = cls.mqe_mock

    @classmethod
    def tearDownClass(cls):
        import sys
        sys.modules['pymqe'] = cls.original_mqe_module
        
        super(BaseIsolatedTest, cls).tearDownClass()