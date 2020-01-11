"""Test base API."""
import unittest

import config
import utils

import pymqi


class TestGet(unittest.TestCase):
    """Test Qeueu.get() method."""

    def setUp(self):
        """Initialize test environment."""
        # max length of queue names is 48 characters
        self.queue_name = "{prefix}GET.QUEUE".format(prefix=config.MQ.QUEUE.PREFIX)
        self.queue_manager = config.MQ.QM.NAME
        self.channel = config.MQ.QM.CHANNEL
        self.host = config.MQ.QM.HOST
        self.port = config.MQ.QM.PORT
        self.user = config.MQ.QM.USER
        self.password = config.MQ.QM.PASSWORD

        self.message = b'12345'
        self.buffer_length = 3

        self.conn_info = "{0}({1})".format(self.host, self.port)

        self.qmgr = pymqi.QueueManager(None)
        self.qmgr.connectTCPClient(self.queue_manager,
                                   pymqi.CD(),
                                   self.channel,
                                   self.conn_info,
                                   self.user,
                                   self.password)

        self._create_queue(self.queue_name)
        self.queue = pymqi.Queue(self.qmgr,
                                 self.queue_name,
                                 pymqi.CMQC.MQOO_INPUT_AS_Q_DEF | pymqi.CMQC.MQOO_OUTPUT)

    def tearDown(self):
        """Delete created objects."""
        if self.queue:
            self.queue.close()

        if self.queue_name:
            self._delete_queue(self.queue_name)
        self.qmgr.disconnect()

    def _create_queue(self, queue_name):
        queue_type = pymqi.CMQC.MQQT_LOCAL
        max_depth = 5000

        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQC.MQIA_Q_TYPE: queue_type,
                pymqi.CMQC.MQIA_MAX_Q_DEPTH: max_depth,
                pymqi.CMQCFC.MQIACF_REPLACE: pymqi.CMQCFC.MQRP_YES}
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_Q(args)

        if pcf.is_connected:
            pcf.disconnect()

    def _delete_queue(self, queue_name):

        pcf = pymqi.PCFExecute(self.qmgr)
        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQCFC.MQIACF_PURGE: pymqi.CMQCFC.MQPO_YES}
        pcf.MQCMD_DELETE_Q(args)

    def _put_message(self):
        md = pymqi.MD()
        self.queue.put(self.message, md)

        return md

    ###########################################################################
    #
    # Real Tests start here
    #
    ###########################################################################

    def test_get_nontruncated(self):
        """Test nontruncated without buffer."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        message = self.queue.get(None, md_get, gmo)

        self.assertEqual(self.message, message)

    def test_get_nontruncated_0(self):
        """Test nontruncated with zerro buffer length."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        try:
            self.queue.get(0, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_FAILED)
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_nontruncated_short(self):
        """Test nontruncated with short buffer."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        try:
            self.queue.get(self.buffer_length, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_FAILED)
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_nontruncated_enough(self):
        """Test nontruncated with big buffer."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        message = self.queue.get(len(self.message), md_get, gmo)

        self.assertEqual(self.message, message)

    def test_get_truncated(self):
        """Test truncated without buffer."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        try:
            self.queue.get(0, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_ACCEPTED)
            self.assertEqual(ex.message, b'')  # pylint: disable=no-member
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_truncated_0(self):
        """Test truncated with zero buffer length."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        try:
            self.queue.get(0, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_ACCEPTED)
            self.assertEqual(ex.message, b'')  # pylint: disable=no-member
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_truncated_short(self):
        """Test truncated with short buffer."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        try:
            self.queue.get(self.buffer_length, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_ACCEPTED)
            self.assertEqual(ex.message,  # pylint: disable=no-member
                             self.message[:self.buffer_length])
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_truncated_enough(self):
        """Test truncated with big buffer."""
        md_put = self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG
        gmo.MatchOptions = pymqi.CMQC.MQMO_MATCH_MSG_ID

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        message = self.queue.get(len(self.message), md_get, gmo)

        self.assertEqual(self.message, message)


if __name__ == "__main__":
    unittest.main()
