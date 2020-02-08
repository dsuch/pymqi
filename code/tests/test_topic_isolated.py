import unittest
from unittest.mock import patch, ANY

from base_isolated_test import BaseIsolatedTest

class TestTopicIsolated(BaseIsolatedTest):
    
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

    def test_topic_connection_is_closed_opened_with_init(self):
        from pymqi import CMQC, Topic
        
        with Topic(self.qmgr_mock, b'topic.name', open_opts=CMQC.MQOO_OUTPUT):
            self.assertConnected()
        
        self.assertClosed()

    def assertConnected(self):
        return self.mocked_mqopen.assert_called_once_with(123, ANY, ANY)

    def assertClosed(self):
        return self.mocked_mqclose.assert_called_once_with(123, 124, ANY)

    def test_topic_connection_is_closed_opened_explicitly(self):
        from pymqi import CMQC, Topic
        
        topic = Topic(self.qmgr_mock)
        with topic.open(b'topic.name', open_opts=CMQC.MQOO_OUTPUT):
            self.assertConnected()
        
        self.assertClosed()

    def test_topic_connection_is_closed_opened_on_enter(self):
        from pymqi import CMQC, Topic
        
        topic = Topic(self.qmgr_mock)
        self.mocked_mqopen.assert_not_called()
        
        with topic.open(b'topic.name', open_opts=CMQC.MQOO_OUTPUT):
            self.assertConnected()
        
        self.assertClosed()

    def test_topic_connection_is_closed_exception_in_context_manager(self):
        from pymqi import CMQC, Topic
        
        with self.assertRaises(Exception):
            with Topic(self.qmgr_mock, b'topic.name', open_opts=CMQC.MQOO_OUTPUT):
                self.assertConnected()
                raise Exception('exception in with')
        
        self.assertClosed()

    def test_topic_raises_app_exception_first(self):
        from pymqi import CMQC, Topic
        
        self.mocked_mqclose.side_effect = Exception('mq close error')

        with self.assertRaises(Exception) as exception_context:
            with Topic(self.qmgr_mock, b'topic.name', open_opts=CMQC.MQOO_OUTPUT):
                self.assertConnected()
                raise Exception('exception in with')
        
        self.assertClosed()
        self.assertIn('exception in with', exception_context.exception.args)
        
    def test_topic_connection_is_closed_exception_in_close(self):
        from pymqi import CMQC, Topic
        
        self.mocked_mqclose.side_effect = Exception('mq close error')

        with self.assertRaises(Exception):
            with Topic(self.qmgr_mock, b'topic.name', open_opts=CMQC.MQOO_OUTPUT):
                self.assertConnected()
        
        self.assertClosed()
        
    def test_topic_connection_is_closed_error_code_on_close(self):
        from pymqi import CMQC, MQMIError, Topic

        self.mocked_mqclose.return_value = (-1, 2, 3)

        with self.assertRaises(MQMIError) as exception_context:        
            with Topic(self.qmgr_mock, b'topic.name', open_opts=CMQC.MQOO_OUTPUT):
                self.assertConnected()
        
        mq_error = exception_context.exception
        self.assertEqual(2, mq_error.comp)
        self.assertEqual(3, mq_error.reason)
        
        self.assertClosed()

if __name__ == "__main__":
    unittest.main()
