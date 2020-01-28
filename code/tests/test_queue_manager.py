""" Tests for pymqi.QueueManager class.
"""

# stdlib
import os
import unittest
from uuid import uuid4

# nose
from nose.tools import eq_

# testfixtures
from testfixtures import Replacer

# test env, configuration & utilities
import config
import utils

# PyMQI
import pymqi
import pymqi.CMQC

    
class TestQueueManager(unittest.TestCase):
    
    qm_name = config.MQ.QM.NAME
    channel = config.MQ.QM.CHANNEL
    host = config.MQ.QM.HOST
    port = config.MQ.QM.PORT
    conn_info = "%s(%s)" % (host, port)

    queue_name = config.MQ.QUEUE.QUEUE_NAMES['TestQueueManager']

    user = config.MQ.QM.USER
    password = config.MQ.QM.PASSWORD
    
    def test_init_none(self):
        qmgr = pymqi.QueueManager(None)
        self.assertFalse(qmgr.is_connected)

    # __init__ with a name calls connect:
    # As the connect method provides no way to supply user & password, this
    # cannot work if the queue manager requires it
    @unittest.skipIf(
        config.MQ.QM.CONN_AUTH.SUPPORTED and
        config.MQ.QM.CONN_AUTH.USE_PW == 'REQUIRED',
        'Test not viable for user/password-requiring queue manager')
    @utils.with_env_complement('MQSERVER', config.MQ.MQSERVER)
    def test_init_name(self):
        # connecting with queue manager name needs MQSERVER set properly
        qmgr = pymqi.QueueManager(self.qm_name)
        self.assertTrue(qmgr.is_connected)
        qmgr.disconnect()

    # As the connect method provides no way to supply user & password, this
    # cannot work if the queue manager requires it
    @unittest.skipIf(
        config.MQ.QM.CONN_AUTH.SUPPORTED and
        config.MQ.QM.CONN_AUTH.USE_PW == 'REQUIRED',
        'Test not viable for user/password-requiring queue manager')
    @utils.with_env_complement('MQSERVER', config.MQ.MQSERVER)
    def test_connect(self):
        # connecting with queue manager name needs MQSERVER set properly
        print(os.environ['MQSERVER'])
        qmgr = pymqi.QueueManager(None)
        self.assertFalse(qmgr.is_connected)
        qmgr.connect(self.qm_name)
        self.assertTrue(qmgr.is_connected)
        qmgr.disconnect()
        
    def test_connect_tcp_client(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        qmgr.disconnect()

    def test_connect_tcp_client_conection_list(self):
        qmgr = pymqi.QueueManager(None)
        self.conn_info = '127.0.0.1(22),{0}'.format(self.conn_info)
        #self.conn_info = '127.0.0.1(1314)'
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        qmgr.disconnect()        

    # This test overlaps with
    # test_mq80.test_successful_connect_without_optional_credentials,
    # but hey, why not
    @unittest.skipIf(
        config.MQ.QM.CONN_AUTH.SUPPORTED and
        config.MQ.QM.CONN_AUTH.USE_PW == 'REQUIRED',
        'Test not viable with a user/password-requiring queue manager')
    def test_connect_tcp_client_no_credentials(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=None,
            password=None)
        self.assertTrue(qmgr.is_connected)
        qmgr.disconnect()

    def test_disconnect(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        qmgr.disconnect()
        self.assertFalse(qmgr.is_connected)

    def test_get_handle_unconnected(self):
        qmgr = pymqi.QueueManager(None)
        self.assertRaises(pymqi.PYIFError, qmgr.get_handle)

    def test_get_handle_connected(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        handle = qmgr.get_handle()
        # assertIsInstance is available >= Python2.7
        self.assertTrue(isinstance(handle, int))
        
    @unittest.skip('Not implemented yet')
    def test_begin(self):
        pass

    @unittest.skip('Not implemented yet')
    def test_commit(self):
        pass

    @unittest.skip('Not implemented yet')
    def test_backout(self):
        pass

    def test_put1(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        input_msg = b'Hello world!'
        qmgr.put1(self.queue_name, input_msg)
        # now get the message from the queue
        queue = pymqi.Queue(qmgr, self.queue_name)
        result_msg = queue.get()
        self.assertEqual(input_msg, result_msg)

    def test_inquire(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        attribute = pymqi.CMQC.MQCA_Q_MGR_NAME
        expected_value = utils.py3str2bytes(self.qm_name)
        attribute_value = qmgr.inquire(attribute)
        self.assertEqual(len(attribute_value), pymqi.CMQC.MQ_Q_MGR_NAME_LENGTH)  
        self.assertEqual(attribute_value.strip(), expected_value)
        
    def test_is_connected(self):
        """Makes sure the QueueManager's 'is_connected' property works as
        expected.
        """
        # uses a mock so no real connection to a queue manager will be
        # established - the parameters below are basically moot
        with Replacer() as r:
            queue_manager = uuid4().hex
            channel = uuid4().hex
            host = uuid4().hex
            port = "1431"
            conn_info = "%s(%s)" % (host, port)
            user = "myuser"
            password = "mypass"

            for expected in(True, False):

                # noinspection PyUnusedLocal
                def _connect_tcp_client(*ignored_args, **ignored_kwargs):
                    pass

                # noinspection PyUnusedLocal
                def _getattr(self2, name):
                    if expected:
                        class _DummyMethod(object):
                            pass
                        # The mere fact of not raising an exception will suffice
                        # for QueueManager._is_connected to understand it as an
                        # all's OK condition.
                        return _DummyMethod
                    else:
                        raise Exception()

                r.replace('pymqi.QueueManager.connect_tcp_client',
                          _connect_tcp_client)
                r.replace('pymqi.PCFExecute.__getattr__', _getattr)

                qmgr = pymqi.QueueManager(None)
                qmgr.connect_tcp_client(
                    queue_manager, pymqi.cd(), channel, conn_info, user,
                    password)

                eq_(qmgr.is_connected, expected)
        

if __name__ == '__main__':
    unittest.main()
