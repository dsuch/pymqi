import unittest
from unittest.mock import patch, ANY

from base_isolated_test import BaseIsolatedTest


class TestQueue(BaseIsolatedTest):
      
    def setUp(self):
        from pymqi import OD
        BaseIsolatedTest.setUp(self)
        
        self.qmgr_patcher = patch('pymqi.QueueManager')
        self.qmgr_mock = self.qmgr_patcher.start()
        self.qmgr_mock.getHandle.return_value = 123
        
        self.mqopen_patcher = patch('pymqi.pymqe.MQOPEN')
        self.mocked_mqopen = self.mqopen_patcher.start()
        self.mocked_mqopen.return_value = (124, OD().pack(), None, None)
        
        self.mqclose_patcher = patch('pymqi.pymqe.MQCLOSE')
        self.mocked_mqclose = self.mqclose_patcher.start()
        self.mocked_mqclose.return_value = (None, None, None)
        
        
    def tearDown(self):
        self.qmgr_patcher.stop()
        self.mqopen_patcher.stop()
        self.mqclose_patcher.stop()
        
        BaseIsolatedTest.tearDown(self)


    def test_queue_connection_is_closed_open_with_init(self):
        from pymqi import Queue

        with Queue(self.qmgr_mock, 'queue.name'):
            self.assertOpened()
        
        self.assertClosed()

    def assertOpened(self):
        return self.mocked_mqopen.assert_called_once_with(123, ANY, ANY)

    def assertClosed(self):
        return self.mocked_mqclose.assert_called_once_with(123, 124, ANY)

    def test_queue_connection_is_closed_explicit_open(self):
        from pymqi import OD, Queue

        queue = Queue(self.qmgr_mock)
        od = OD()
        od.ObjectName = b'queue.name'
        
        with queue.open(od):
            self.assertOpened()
        
        self.assertClosed()
        
        
    def test_queue_connection_is_closed_opened_in_enter(self):
        from pymqi import Queue

        queue = Queue(self.qmgr_mock).open('queue.name')
        self.mocked_mqopen.assert_not_called()
        
        with queue:
            self.assertOpened()
        
        self.assertClosed()

    def test_exception_in_context_manager(self):
        from pymqi import Queue
        
        with self.assertRaises(Exception):
            with Queue(self.qmgr_mock, 'queue.name'):
                raise Exception('some exception')
        
        self.assertClosed()
        
    
    def test_exception_on_close(self):
        from pymqi import Queue

        self.mocked_mqclose.side_effect = Exception('exception on close')
        
        with self.assertRaises(Exception):
            with Queue(self.qmgr_mock, 'queue.name'):
                self.assertOpened()
        
        self.assertClosed()
        
        
    def test_queue_raises_app_exception_first(self):
        from pymqi import Queue
        
        self.mocked_mqclose.side_effect = Exception('mq close error')

        with self.assertRaises(Exception) as exception_context:
            with Queue(self.qmgr_mock, b'queue.name'):
                self.assertOpened()
                raise Exception('exception in with')
        
        self.assertClosed()       
        self.assertIn('exception in with', exception_context.exception.args)

    def test_error_code_on_close(self):
        from pymqi import Queue, MQMIError

        self.mocked_mqclose.return_value = (-1, 2, 3)
        
        with self.assertRaises(MQMIError) as exception_context:
            with Queue(self.qmgr_mock, 'queue.name'):
                self.assertOpened()
        
        mq_error = exception_context.exception
        self.assertEqual(2, mq_error.comp)
        self.assertEqual(3, mq_error.reason)
        
        self.assertClosed()
        
    def test_multiple_parameters(self):
        from pymqi import CMQC, Queue
        
        with Queue(self.qmgr_mock, 'queue.name', CMQC.MQOO_INPUT_EXCLUSIVE):
            self.mocked_mqopen.assert_called_once_with(123, ANY, CMQC.MQOO_INPUT_EXCLUSIVE)
        
        self.assertClosed()

if __name__ == "__main__":
    unittest.main()
