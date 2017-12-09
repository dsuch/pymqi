""" Tests for making sure MQ 8.0 features work properly.

Requires proper configuration in config.py or by setting the following
environment variables (which the config module respects) pointing to an MQ 8.0
queue managers and credentials.
Substitute values as required.

export PYMQI_TEST_QM_NAME=QM01
export PYMQI_TEST_QM_HOST=192.168.1.136
export PYMQI_TEST_QM_PORT=1434
export PYMQI_TEST_QM_CHANNEL=SVRCONN.1
export PYMQI_TEST_QM_USER=myuser
export PYMQI_TEST_QM_PASSWORD=mypassword
"""

# stdlib
import os
import unittest

# test config & env
import config
import env

# PyMQI
import pymqi
from pymqi import CMQC, CMQXC, CMQCFC


class TestMQ80(unittest.TestCase):

    def setUp(self):
        for key in ['NAME', 'HOST', 'PORT', 'CHANNEL', 'USER', 'PASSWORD']:
            setattr(self, key.lower(), getattr(config.MQ.QM, key))

    def get_conn(self):
        return pymqi.connect(self.name, self.channel, '{}({})'.format(
            self.host, self.port), self.user, self.password)

    # obviously this test can not work for a queue manager < 8.0
    @unittest.skipIf(
        int(config.MQ.QM.MIN_COMMAND_LEVEL) < 800,
        'Test only viable for a queue manager command level > 800.')
    def test_mq_level(self):
        """ We should be connecting to an MQ 8.0+ queue manager.
        """
        conn = self.get_conn()
        pcf = pymqi.PCFExecute(conn)
        command_level = pcf.MQCMD_INQUIRE_Q_MGR()[0][CMQC.MQIA_COMMAND_LEVEL]
        self.assertGreaterEqual(command_level, 800)
        conn.disconnect()

    def test_connect_with_credentials(self):
        """ Connecting with user credentials provided should succeed.
        """
        conn = self.get_conn()
        self.assertTrue(conn.is_connected)
        conn.disconnect()

    @unittest.skipUnless(
        config.MQ.QM.CONN_AUTH.SUPPORTED == '1',
        'Test only viable for a queue manager with user/password conn auth '
        'support')
    def test_connect_with_wrong_credentials(self):
        # Modify original valid password to some bogus value
        bogus_password = self.password + '_Wr0nG_Pa$$w0rd'
        with self.assertRaises(pymqi.MQMIError) as errorcontext:
            qmgr = pymqi.connect(self.name, self.channel, '{}({})'.format(
                self.host, self.port), self.user, bogus_password)
            exception = errorcontext.exception
            self.assertEqual(exception.reason, CMQC.MQRC_NOT_AUTHORIZED)
            self.assertFalse(qmgr.is_connected)

    # The following 2 tests test_connect_without_required_credentials and
    # test_connect_without_optional_credentials are mutually exclusive and
    # intend to provide workable tests for both a (>=MQ 8.0) queue manager
    # with or without equired user/password authentication and also a (<MQ 8.0)
    # queue manager that doesn't know about user/password conn auth, anyway 
    @unittest.skipUnless(
        config.MQ.QM.CONN_AUTH.SUPPORTED and
        config.MQ.QM.CONN_AUTH.USE_PW == 'REQUIRED',
        'Test needs a user/password-requiring queue manager')
    def test_failing_connect_without_required_credentials(self):
        """Connecting without user credentials provided should not succeed for
        a queue manager that requires user/password connection authentication.
        """

        with self.assertRaises(pymqi.MQMIError) as errorcontext:
            qmgr = pymqi.connect(self.name, self.channel, '{}({})'.format(
                self.host, self.port))
            exception = errorcontext.exception
            self.assertEqual(exception.reason, CMQC.MQRC_NOT_AUTHORIZED)
            self.assertFalse(qmgr.is_connected)
            
    @unittest.skipUnless(
        config.MQ.QM.CONN_AUTH.SUPPORTED != '1' or
        config.MQ.QM.CONN_AUTH.USE_PW != 'REQUIRED',
        'Test not viable for a user/password-requiring queue manager')
    def test_successful_connect_without_optional_credentials(self):
        """Connecting without user credentials should succeed for a queue
        manager that has optional user/password connection authentication. 
        """
        qmgr = pymqi.connect(self.name, self.channel, '{}({})'.format(
                self.host, self.port))
        self.assertTrue(qmgr.is_connected)
        qmgr.disconnect()
            

if __name__ == "__main__":
    unittest.main()
