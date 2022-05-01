""" Tests for pymqi.QueueManager class.
"""

import os
import unittest
from uuid import uuid4

from testfixtures import Replacer

import config  # noqa
import utils  # noqa

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
        if qmgr.is_connected:
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
        if qmgr.is_connected:
            qmgr.disconnect()

    def test_connect_tcp_client(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        if qmgr.is_connected:
            qmgr.disconnect()

    @unittest.skipIf(
         config.MQ.QM.CONN_AUTH.SUPPORTED and
         config.MQ.QM.CONN_AUTH.USE_PW == 'OPTIONAL',
         'Test only viable with a user/password requiring queue manager')
    def test_connect_tcp_client_without_cred(self):
        qmgr = pymqi.QueueManager(None)
        with self.assertRaises(pymqi.MQMIError) as ex_ctx:
            qmgr.connect_tcp_client(
                self.qm_name, pymqi.cd(), self.channel, self.conn_info)
            self.assertEqual(ex_ctx.exception.reason, pymqi.CMQC.MQRC_NOT_AUTHORIZED)
        if qmgr.is_connected:
            qmgr.disconnect()

    def test_connect_tcp_client_conection_list(self):
        qmgr = pymqi.QueueManager(None)
        self.conn_info = '127.0.0.1(22),{0}'.format(self.conn_info)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        if qmgr.is_connected:
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
        if qmgr.is_connected:
            qmgr.disconnect()

    def test_disconnect(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.qm_name, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        if qmgr.is_connected:
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


if __name__ == '__main__':
    unittest.main()
