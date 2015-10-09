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

env_prefix = 'PYMQI_TEST_QM_'
env_vars = ['NAME', 'HOST', 'PORT', 'CHANNEL', 'USER', 'PASSWORD']

#TODO: Remove this? It's not used anymore, and invalid configuration should
# lead to proper operation errors, anyway.
def ensure_env_vars():
    missing = []
    for key in env_vars:
        full_name = env_prefix + key
        if not os.environ.get(full_name):
            missing.append(full_name)

    if missing:
        raise Exception('Cannot proceed. Environment variables missing: {}'.format(sorted(missing)))

class TestMQ80(unittest.TestCase):

    def setUp(self):
        for key in env_vars:
            setattr(self, key.lower(), getattr(config.MQ.QM, key))

    def get_conn(self):
        return pymqi.connect(self.name, self.channel, '{}({})'.format(self.host, self.port), self.user, self.password)

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
        conn.disconnect()

    def test_connect_without_credentials(self):
        """ Connecting without user credentials provided should not succeed.
        """
        try:
            pymqi.connect(self.name, self.channel, '{}({})'.format(self.host, self.port))
        except pymqi.MQMIError, e:
            if e.reason == CMQC.MQRC_NOT_AUTHORIZED:
                pass # That's OK, we actually expect it
            else:
                raise
        else:
            raise Exception('Excepted for the test to fail without user credentials')

if __name__ == "__main__":
    unittest.main()
