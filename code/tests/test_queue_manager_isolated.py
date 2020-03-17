import unittest
try:
    from unittest.mock import patch, ANY  # >= Python 3.3
except ImportError:
    from mock import patch, ANY

from base_isolated_test import BaseIsolatedTest


class TestQueueManager(BaseIsolatedTest):

    def setUp(self):
        from pymqi import CMQC
        
        self.mqconn_patcher = patch('pymqi.pymqe.MQCONN')
        
        self.mocked_mqconn = self.mqconn_patcher.start()
        self.mocked_mqconn.return_value = (123, CMQC.MQCC_OK)
        
        self.mqdisc_patcher = patch('pymqi.pymqe.MQDISC')
        self.mocked_mqdisc = self.mqdisc_patcher.start()
        
    def tearDown(self):
        self.mqconn_patcher.stop()
        self.mqdisc_patcher.stop()

    def test_connection_is_closed_with_autoconnect(self):
        from pymqi import QueueManager
        
        with QueueManager(name = 'QMGR'):
            self.assertConnected()
        
        self.assertDisconnected()

    def assertConnected(self):
        return self.mocked_mqconn.assert_called_once_with(b'QMGR')
    
    def assertDisconnected(self):
        return self.mocked_mqdisc.assert_called_once_with(123)

    def test_connection_is_closed_without_autoconnect(self):
        from pymqi import QueueManager
        
        qm = QueueManager(name = None)
        with qm.connect(b'QMGR'):
            self.assertConnected()
        
        self.assertDisconnected()
    
    def test_connection_reopens_if_closed(self):
        from pymqi import QueueManager
        
        qm = QueueManager(name = 'QMGR')
        qm.disconnect()
        self.mocked_mqconn.reset_mock()
        self.mocked_mqdisc.reset_mock()
        
        with qm:
            self.assertConnected()
        
        self.assertDisconnected()
    
    def test_connection_is_closed_on_exception(self):
        from pymqi import QueueManager
        
        with self.assertRaises(Exception):
            with QueueManager(name = 'QMGR'):
                self.assertConnected()
                raise Exception('some errors')
        
        self.assertDisconnected()
    
    def test_connection_is_closed_on_exit_exception(self):
        from pymqi import QueueManager
        
        self.raiseOnDisconnect()
        
        with self.assertRaises(Exception):
            with QueueManager(name = 'QMGR'):
                self.assertConnected()
        
        self.assertDisconnected()

    def raiseOnDisconnect(self):
        self.mocked_mqdisc.side_effect = Exception('Error on disconnect')
        
    def test_connect_exception_cause_is_set(self):
        from pymqi import QueueManager
        
        self.raiseOnDisconnect()
        
        with self.assertRaises(Exception) as exception_context:
            with QueueManager(name = 'QMGR'):
                self.assertConnected()
                raise Exception('some errors')
        
        exc = exception_context.exception
        self.assertEqual(('some errors', ), exc.args)
                
        self.mocked_mqdisc.assert_called_once_with(123)

    @patch('pymqi.pymqe.MQCONNX')
    def test_connect_with_options_is_closed_on_exit(self, mocked_mqconnx):
        from pymqi import CMQC, QueueManager
        
        mocked_mqconnx.return_value = (123, CMQC.MQCC_OK)
        
        qm = QueueManager(None)
        with qm.connect_with_options('QMGR'):
            mocked_mqconnx.assert_called_once_with(b'QMGR', ANY, ANY, ANY, ANY)
        
        self.assertDisconnected()


    @patch('pymqi.pymqe.MQCONNX')
    def test_connect_with_tcp_is_closed_on_exit(self, mocked_mqconnx):
        from pymqi import CD, CMQC, QueueManager
        
        mocked_mqconnx.return_value = (123, CMQC.MQCC_OK)
        
        qm = QueueManager(None)
        with qm.connect_tcp_client('QMGR', CD(), 'channel', 'connection', 'user', 'pass'):
            mocked_mqconnx.assert_called_once_with(b'QMGR',ANY, ANY,
                                                   { 'user' : b'user', 'password': b'pass' }, ANY)
        
        self.assertDisconnected()

    @patch('pymqi.pymqe.MQINQ')
    @patch('pymqi.pymqe.MQCLOSE')
    @patch('pymqi.pymqe.MQOPEN')
    def test_mqclosed_if_inquired(self, mocked_mqopen, mocked_mqclose, mocked_mqinq):
        from pymqi import QueueManager
        
        mocked_mqopen.return_value = (124, None, None)
        mocked_mqinq.return_value = ('value', None, None)
        
        with QueueManager(name = 'QMGR') as qm:
            value = qm.inquire('attribute')
            self.assertEqual(value, 'value')
            mocked_mqinq.assert_called_once_with(123, 124, ANY)
        
        mocked_mqclose.assert_called_once_with(123, 124, ANY)
        self.assertDisconnected()
        
    @patch('pymqi.pymqe.MQINQ')
    @patch('pymqi.pymqe.MQCLOSE')
    @patch('pymqi.pymqe.MQOPEN')
    def test_disconnected_if_inquired_close_error_on_exit(self, mocked_mqopen, mocked_mqclose, mocked_mqinq):
        from pymqi import QueueManager
        
        mocked_mqopen.return_value = (124, None, None)
        mocked_mqinq.return_value = ('value', None, None)
        
        mocked_mqclose.side_effect = Exception('close failed')
        
        with self.assertRaises(Exception):
            with QueueManager(name = 'QMGR') as qm:
                value = qm.inquire('attribute')
                self.assertEqual(value, 'value')
                mocked_mqinq.assert_called_once_with(123, 124, ANY)
        
        mocked_mqclose.assert_called_once_with(123, 124, ANY)
        self.assertDisconnected()
                
    @patch('pymqi.pymqe.MQINQ')
    @patch('pymqi.pymqe.MQCLOSE')
    @patch('pymqi.pymqe.MQOPEN')
    def test_inquire_exception_cause_is(self, mocked_mqopen, mocked_mqclose, mocked_mqinq):
        from pymqi import QueueManager
        
        mocked_mqopen.return_value = (124, None, None)
        mocked_mqinq.return_value = ('value', None, None)
        
        mocked_mqclose.side_effect = Exception('close failed')
        self.raiseOnDisconnect()
        
        with self.assertRaises(Exception) as exception_context:
            with QueueManager(name = 'QMGR') as qm:
                value = qm.inquire('attribute')
                self.assertEqual(value, 'value')
                mocked_mqinq.assert_called_once_with(123, 124, ANY)
        
        exc = exception_context.exception
        self.assertEqual(('Error on disconnect', ), exc.args)
        
        mocked_mqclose.assert_called_once_with(123, 124, ANY)
        self.assertDisconnected()
                        
    @patch('pymqi.pymqe.MQINQ')
    @patch('pymqi.pymqe.MQCLOSE')
    @patch('pymqi.pymqe.MQOPEN')
    def test_inquire_exception_cause_is_set_close_exception_dropped(self, mocked_mqopen, mocked_mqclose, mocked_mqinq):
        from pymqi import QueueManager
        
        mocked_mqopen.return_value = (124, None, None)
        mocked_mqinq.return_value = ('value', None, None)
        
        mocked_mqclose.side_effect = Exception('close failed')
        self.raiseOnDisconnect()
        
        with self.assertRaises(Exception) as exception_context:
            with QueueManager(name = 'QMGR') as qm:
                value = qm.inquire('attribute')
                self.assertEqual(value, 'value')
                mocked_mqinq.assert_called_once_with(123, 124, ANY)
                raise Exception('some errors')
        
        exc = exception_context.exception
        self.assertEqual(('some errors', ), exc.args)
        
        mocked_mqclose.assert_called_once_with(123, 124, ANY)
        self.assertDisconnected()

if __name__ == "__main__":
    unittest.main()
