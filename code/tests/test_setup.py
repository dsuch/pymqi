"""Setup tests environment."""
import os.path
from unittest import TestCase  # noqa
from unittest import main # pylint: disable=unused-import

import pymqi

import config  # noqa
import utils  # noqa


class Tests(TestCase):
    """Setup and tearsdown tests environment."""

    version = '0000000'

    queue_name = ''
    queue_manager = ''
    channel = ''
    host = ''
    port = ''
    user = ''
    password = ''

    prefix = ''

    qmgr = None


    @classmethod
    def setUpClass(cls):
        """Initialize test environment."""
        cls.prefix = os.environ.get('PYMQI_TEST_OBJECT_PREFIX', 'PYMQI.')

        # max length of queue names is 48 characters
        cls.queue_name = "{prefix}MSG.QUEUE".format(prefix=config.MQ.QUEUE.PREFIX)
        cls.queue_manager = config.MQ.QM.NAME
        cls.channel = config.MQ.QM.CHANNEL
        cls.host = config.MQ.QM.HOST
        cls.port = config.MQ.QM.PORT
        cls.user = config.MQ.QM.USER
        cls.password = config.MQ.QM.PASSWORD

        cls.conn_info = "{0}({1})".format(cls.host, cls.port)

        cls.qmgr = pymqi.QueueManager(None)
        try:
            cls.qmgr.connectTCPClient(cls.queue_manager, pymqi.CD(), cls.channel, cls.conn_info, cls.user, cls.password)
        except pymqi.MQMIError as ex:
            if ex.comp == pymqi.CMQC.MQCC_FAILED:
                raise ex

        cls.version = cls.inquire_qmgr_version().decode()

    @classmethod
    def tearDownClass(cls):
        """Clear test environment."""
        cls.qmgr.disconnect()

    def setUp(self):
        """Set up tesing environment."""

    def tearDown(self):
        """Clear test environment."""

    @classmethod
    def inquire_qmgr_version(cls):
        """Inqure Queue Manager version."""
        return cls.qmgr.inquire(pymqi.CMQC.MQCA_VERSION)

    def create_queue(self, queue_name, max_depth=5000, args=None):
        """Create queue."""
        if args:
            args[pymqi.CMQC.MQCA_Q_NAME] = utils.py3str2bytes(queue_name)
        else:
            args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                    pymqi.CMQC.MQIA_Q_TYPE: pymqi.CMQC.MQQT_LOCAL,
                    pymqi.CMQC.MQIA_MAX_Q_DEPTH: max_depth,
                    pymqi.CMQCFC.MQIACF_REPLACE: pymqi.CMQCFC.MQRP_YES}
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_Q(args)

    def delete_queue(self, queue_name):
        """Delete queue."""
        pcf = pymqi.PCFExecute(self.qmgr)
        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQCFC.MQIACF_PURGE: pymqi.CMQCFC.MQPO_YES}
        pcf.MQCMD_DELETE_Q(args)

    def create_channel(self, channel_name, args=None):
        """Create channle."""
        if args:
            args[pymqi.CMQCFC.MQCACH_CHANNEL_NAME] = utils.py3str2bytes(channel_name)
        else:
            args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: utils.py3str2bytes(channel_name),
                    pymqi.CMQCFC.MQIACH_CHANNEL_TYPE: pymqi.CMQC.MQCHT_SVRCONN,
                    pymqi.CMQCFC.MQIACF_REPLACE: pymqi.CMQCFC.MQRP_YES}
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_CHANNEL(args)

    def delete_channel(self, channel_name):
        """Delete channel."""
        pcf = pymqi.PCFExecute(self.qmgr)
        args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: utils.py3str2bytes(channel_name)}
        pcf.MQCMD_DELETE_CHANNEL(args)

    def create_auth_rec(self, args):
        """Create authentication recoed."""
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_SET_CHLAUTH_REC(args)

    def delete_auth_rec(self, args):
        """Delete authentication recoed."""
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_SET_CHLAUTH_REC(args)

    @classmethod
    def edit_qmgr(cls, args):
        """Edit connected Queue Manager."""
        pcf = pymqi.PCFExecute(cls.qmgr)
        pcf.MQCMD_CHANGE_Q_MGR(args)

