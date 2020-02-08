import unittest
from unittest.mock import patch, ANY, call

from base_isolated_test import BaseIsolatedTest

class TestSubscriptionIsolated(BaseIsolatedTest):

    def setUp(self):
        from pymqi import SD
        BaseIsolatedTest.setUp(self)
        
        self.qmgr_patcher = patch('pymqi.QueueManager')
        self.qmgr_mock = self.qmgr_patcher.start()
        self.qmgr_mock.getHandle.return_value = 123
        
        self.mqsub_patcher = patch('pymqi.pymqe.MQSUB')
        self.mocked_mqsub = self.mqsub_patcher.start()
        self.mocked_mqsub.return_value = (SD().pack(), 124, 125, None, None)
        
        self.mqclose_patcher = patch('pymqi.pymqe.MQCLOSE') 
        self.mocked_mqclose = self.mqclose_patcher.start()
        self.mocked_mqclose.return_value = (None, None, None)
        
    def tearDown(self):
        self.qmgr_patcher.stop()
        self.mqsub_patcher.stop()
        self.mqclose_patcher.stop()
        
        BaseIsolatedTest.tearDown(self)

    def test_subscription_connection_is_closed_opened_with_init(self):
        from pymqi import SD, Subscription
        
        with Subscription(self.qmgr_mock, sub_desc=SD()):
            self.assertSubscribed()
        
        self.assertSubscriptionAndSubQueueAreClosed()

    def assertSubscribed(self, queue_handle = 0):
        return self.mocked_mqsub.assert_called_once_with(123, ANY, queue_handle)


    def assertSubscriptionAndSubQueueAreClosed(self):
        return self.mocked_mqclose.assert_has_calls([call(123, 124, ANY), call(123, 125, ANY)], any_order=True)

    def test_subscription_connection_is_closed_opened_explicitly(self):
        from pymqi import SD, Subscription
        
        subscription = Subscription(self.qmgr_mock)
        self.mocked_mqsub.assert_not_called()

        with subscription.sub(sub_desc=SD()):
            self.assertSubscribed()
        
        self.assertSubscriptionAndSubQueueAreClosed()

    def test_subscription_connection_is_closed_opened_on_enter(self):
        from pymqi import SD, Subscription
        
        subscription = Subscription(self.qmgr_mock)
        self.mocked_mqsub.assert_not_called()
        
        with subscription.sub(sub_desc=SD()):
            self.assertSubscribed()
        
        self.assertSubscriptionAndSubQueueAreClosed()

    def test_subscription_connection_is_closed_exception_in_context_manager(self):
        from pymqi import SD, Subscription

        with self.assertRaises(Exception):
            with Subscription(self.qmgr_mock, sub_desc=SD()):
                raise Exception('exception in with')
        
        self.assertSubscriptionAndSubQueueAreClosed()
        
        
    def test_subscription_connection_is_closed_exception_in_close(self):
        from pymqi import SD, Subscription
        
        self.mocked_mqclose.side_effect = Exception('mq close error')

        with self.assertRaises(Exception):
            with Subscription(self.qmgr_mock, sub_desc=SD()):
                self.assertSubscribed()
        
        self.mocked_mqclose.assert_has_calls([call(123, 125, ANY)], any_order=True)
    
    def test_subscription_raises_app_exception_first(self):
        from pymqi import SD, Subscription
        
        self.mocked_mqclose.side_effect = Exception('mq close error')

        with self.assertRaises(Exception) as exception_context:
            with Subscription(self.qmgr_mock, sub_desc=SD()):
                self.assertSubscribed()
                raise Exception('exception in with')

        self.assertSubscriptionAndSubQueueAreClosed()        
        self.assertIn('exception in with', exception_context.exception.args)
        
    def test_subscription_connection_is_closed_error_code_on_close(self):
        from pymqi import MQMIError, SD, Subscription
        
        self.mocked_mqclose.return_value = (-1, 2, 3)

        with self.assertRaises(MQMIError) as exception_context:        
            with Subscription(self.qmgr_mock, sub_desc=SD()):
                self.assertSubscribed()
        
        mq_error = exception_context.exception
        self.assertEqual(2, mq_error.comp)
        self.assertEqual(3, mq_error.reason)
        
        self.mocked_mqclose.assert_has_calls([call(123, 125, ANY)], any_order=True)
        # FIXME code not closing sub queue if first close fails

if __name__ == "__main__":
    unittest.main()
