""" Tests for pymqi.QueueManager class.
"""

import os
import unittest
from uuid import uuid4

import config  # noqa
import utils  # noqa

try:
    from typing import List
except ImportError:
    pass

from test_setup import Tests  # noqa
from test_setup import main  # noqa

import pymqi
import pymqi.CMQC


class TestQueueManager(Tests):

    CHCKLOCL = None  # type: int

    @classmethod
    def setUpClass(cls):
        """Initialize test environment."""
        super(TestQueueManager, cls).setUpClass()

        # Get CHCKLOCL value
        attrs = []  # type: List[pymqi.MQOpts]
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_Q_MGR_ATTRS,
                                Values=[pymqi.CMQC.MQCA_CONN_AUTH]))
        results = cls.pcf.MQCMD_INQUIRE_Q_MGR(attrs)
        connAuthName = results[0][pymqi.CMQC.MQCA_CONN_AUTH]

        attrs = []  # type: List[pymqi.MQOpts]

        attrs.append(pymqi.CFST(Parameter=pymqi.CMQC.MQCA_AUTH_INFO_NAME,
                                String=connAuthName))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQC.MQIA_AUTH_INFO_TYPE,
                                Value=pymqi.CMQC.MQAIT_IDPW_OS))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_AUTH_INFO_ATTRS,
                                Values=[pymqi.CMQC.MQIA_CHECK_LOCAL_BINDING]))

        results = cls.pcf.MQCMD_INQUIRE_AUTH_INFO(attrs)
        cls.CHCKLOCL = results[0][pymqi.CMQC.MQIA_CHECK_LOCAL_BINDING]

        # Add required rights for pinging QMGR
        attrs = []  # type: List[pymqi.MQOpts]
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQCFC.MQCACF_AUTH_PROFILE_NAME,
                                String=b'SYSTEM.DEFAULT.MODEL.QUEUE'))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQCFC.MQIACF_OBJECT_TYPE,
                                Value=pymqi.CMQC.MQOT_Q))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_AUTH_ADD_AUTHS,
                                Values=[pymqi.CMQCFC.MQAUTH_DISPLAY,
                                        pymqi.CMQCFC.MQAUTH_INPUT]))
        attrs.append(pymqi.CFSL(Parameter=pymqi.CMQCFC.MQCACF_PRINCIPAL_ENTITY_NAMES,
                                Strings=[utils.py3str2bytes(cls.app_user)]))
        cls.pcf.MQCMD_SET_AUTH_REC(attrs)

        attrs = []  # type: List[pymqi.MQOpts]
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQCFC.MQCACF_AUTH_PROFILE_NAME,
                                String=b'SYSTEM.ADMIN.COMMAND.QUEUE'))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQCFC.MQIACF_OBJECT_TYPE,
                                Value=pymqi.CMQC.MQOT_Q))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_AUTH_ADD_AUTHS,
                                Values=[pymqi.CMQCFC.MQAUTH_OUTPUT]))
        attrs.append(pymqi.CFSL(Parameter=pymqi.CMQCFC.MQCACF_PRINCIPAL_ENTITY_NAMES,
                                Strings=[utils.py3str2bytes(cls.app_user)]))
        cls.pcf.MQCMD_SET_AUTH_REC(attrs)

        attrs = []  # type: List[pymqi.MQOpts]
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQCFC.MQCACF_AUTH_PROFILE_NAME,
                                String=utils.py3str2bytes(cls.queue_manager)))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQCFC.MQIACF_OBJECT_TYPE,
                                Value=pymqi.CMQC.MQOT_Q_MGR))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_AUTH_ADD_AUTHS,
                                Values=[pymqi.CMQCFC.MQAUTH_DISPLAY]))
        attrs.append(pymqi.CFSL(Parameter=pymqi.CMQCFC.MQCACF_PRINCIPAL_ENTITY_NAMES,
                                Strings=[utils.py3str2bytes(cls.app_user)]))
        results = cls.pcf.MQCMD_SET_AUTH_REC(attrs)

        if cls.pcf.is_connected:
            cls.pcf.disconnect()
        if cls.qmgr.is_connected:
            cls.qmgr.disconnect()

    def test_init_none(self):
        qmgr = pymqi.QueueManager(None)
        self.assertFalse(qmgr.is_connected)

    @utils.with_env_complement('MQSERVER', config.MQ.APP_MQSERVER)
    def test_init_name(self):
        # As the connect method provides no way to supply user & password, this
        # cannot work if the queue manager requires it
        if self.CHCKLOCL == pymqi.CMQCFC.MQCHK_REQUIRED:
            self.skipTest('Test not viable for user/password-requiring queue manager')
            return

        # connecting with queue manager name needs MQSERVER set properly
        qmgr = pymqi.QueueManager(self.queue_manager)
        self.assertTrue(qmgr.is_connected)

        if qmgr.is_connected:
            qmgr.disconnect()

    @utils.with_env_complement('MQSERVER', config.MQ.APP_MQSERVER)
    def test_connect(self):
        # As the connect method provides no way to supply user & password, this
        # cannot work if the queue manager requires it
        if self.CHCKLOCL == pymqi.CMQCFC.MQCHK_REQUIRED:
            self.skipTest('Test not viable for user/password-requiring queue manager')
            return

        qmgr = pymqi.QueueManager(None)
        self.assertFalse(qmgr.is_connected)
        qmgr.connect(self.queue_manager)
        self.assertTrue(qmgr.is_connected)
        if qmgr.is_connected:
            qmgr.disconnect()

    def test_connect_tcp_client(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.queue_manager, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        if qmgr.is_connected:
            qmgr.disconnect()

    def test_connect_tcp_client_without_cred(self):
        if self.CHCKLOCL == pymqi.CMQCFC.MQCHK_REQUIRED:
            self.skipTest('Test not viable for user/password-requiring queue manager')
            return

        qmgr = pymqi.QueueManager(None)
        with self.assertRaises(pymqi.MQMIError) as ex_ctx:
            qmgr.connect_tcp_client(
                self.queue_manager, pymqi.cd(), self.channel, self.conn_info)
            self.assertEqual(ex_ctx.exception.reason, pymqi.CMQC.MQRC_NOT_AUTHORIZED)
        if qmgr.is_connected:
            qmgr.disconnect()

    # This test should be run last
    # ConnectionName list with unaccessible QM affects on channel name of the next test if MQSERVER used
    # changing the order of ConnectionName entries does not affect to issue occurrence
    def test_zzz_connect_tcp_client_conection_list(self):
        qmgr = pymqi.QueueManager(None)
        conn_info = '127.0.0.1(22),{0}'.format(self.conn_info)
        qmgr.connect_tcp_client(
            self.queue_manager, pymqi.cd(), self.channel, conn_info, user=self.user,
            password=self.password)
        self.assertTrue(qmgr.is_connected)
        if qmgr.is_connected:
            qmgr.disconnect()

    # This test overlaps with
    # test_mq80.test_successful_connect_without_optional_credentials,
    # but hey, why not
    def test_connect_tcp_client_with_none_credentials(self):
        if self.CHCKLOCL == pymqi.CMQCFC.MQCHK_REQUIRED:
            self.skipTest('Test not viable for user/password-requiring queue manager')
            return

        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.queue_manager, pymqi.cd(), self.app_channel, self.conn_info, user=None,
            password=None)
        self.assertTrue(qmgr.is_connected)
        if qmgr.is_connected:
            qmgr.disconnect()

    def test_disconnect(self):
        qmgr = pymqi.QueueManager(None)
        qmgr.connect_tcp_client(
            self.queue_manager, pymqi.cd(), self.channel, self.conn_info, user=self.user,
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
            self.queue_manager, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        handle = qmgr.get_handle()
        self.assertTrue(isinstance(handle, int))

        if qmgr.is_connected:
            qmgr.disconnect()

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
            self.queue_manager, pymqi.cd(), self.channel, self.conn_info, user=self.user,
            password=self.password)
        attribute = pymqi.CMQC.MQCA_Q_MGR_NAME
        expected_value = utils.py3str2bytes(self.queue_manager)
        attribute_value = qmgr.inquire(attribute)
        self.assertEqual(len(attribute_value), pymqi.CMQC.MQ_Q_MGR_NAME_LENGTH)
        self.assertEqual(attribute_value.strip(), expected_value)

        if qmgr.is_connected:
            qmgr.disconnect()
            self.assertFalse(qmgr.is_connected)


if __name__ == '__main__':
    main(module="test_queue_manager")
