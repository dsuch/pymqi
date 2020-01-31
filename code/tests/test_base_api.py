# -*- coding: utf8 -*-
"""Test base API."""
from sys import version_info
#from sys.version_info import major as py_ver
import unittest

import config
import utils

from test_setup import Tests

import pymqi

class TestGet(Tests):
    """Test Qeueu.get() method."""

    def setUp(self):
        """Initialize test environment."""
        super(TestGet, self).setUp()

        self.create_queue(self.queue_name)

        self.message = b'12345'
        self.buffer_length = 3

        self.queue = pymqi.Queue(self.qmgr,
                                 self.queue_name,
                                 pymqi.CMQC.MQOO_INPUT_AS_Q_DEF | pymqi.CMQC.MQOO_OUTPUT)

    def tearDown(self):
        """Delete created objects."""
        if self.queue:
            self.queue.close()

        self.delete_queue(self.queue_name)

        super(TestGet, self).tearDown()

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
        self._put_message()

        md_get = pymqi.MD()
        message = self.queue.get(None, md_get)

        self.assertEqual(self.message, message)

    def test_get_nontruncated_0(self):
        """Test nontruncated with zerro buffer length."""
        self._put_message()

        md_get = pymqi.MD()
        try:
            self.queue.get(0, md_get)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_FAILED)
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_nontruncated_short(self):
        """Test nontruncated with short buffer."""
        md_put = self._put_message()

        md_get = pymqi.MD()
        try:
            self.queue.get(self.buffer_length, md_get)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_FAILED)
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_nontruncated_enough(self):
        """Test nontruncated with big enough buffer."""
        md_put = self._put_message()

        md_get = pymqi.MD()
        message = self.queue.get(len(self.message), md_get)

        self.assertEqual(self.message, message)

    def test_get_truncated(self):
        """Test truncated without buffer."""
        self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG

        md_get = pymqi.MD()
        try:
            self.queue.get(0, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_ACCEPTED)
            self.assertEqual(ex.message, b'')  # pylint: disable=no-member
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_truncated_0(self):
        """Test truncated with zero buffer length."""
        self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG

        md_get = pymqi.MD()
        try:
            self.queue.get(0, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_ACCEPTED)
            self.assertEqual(ex.message, b'')  # pylint: disable=no-member
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             len(self.message))

    def test_get_truncated_short(self):
        """Test truncated with short buffer."""
        self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG

        md_get = pymqi.MD()
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
        self._put_message()
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG

        md_get = pymqi.MD()
        message = self.queue.get(len(self.message), md_get, gmo)

        self.assertEqual(self.message, message)

    def test_get_nontruncated_big_msg(self):
        """Test get nontruncated big message"""
        md_put = pymqi.MD()
        if version_info.major >= 3:
            self.queue.put(bytes(4097), md_put)
        else:
            self.queue.put(bytes(b'\0'*4097), md_put)

        md_get = pymqi.MD()
        message = self.queue.get(None, md_get)

        self.assertEqual(len(message), 4097)
        self.assertEqual(md_put.PutDate, md_get.PutDate)

    def test_get_truncated_big_msg(self):
        """Test get nontruncated big message"""
        md_put = pymqi.MD()
        if version_info.major >= 3:
            self.queue.put(bytes(4097), md_put)
        else:
            self.queue.put(bytes(b'\0'*4097), md_put)
        gmo = pymqi.GMO()
        gmo.Options = pymqi.CMQC.MQGMO_ACCEPT_TRUNCATED_MSG

        md_get = pymqi.MD()
        try:
            message = self.queue.get(None, md_get, gmo)
        except pymqi.MQMIError as ex:
            self.assertEqual(ex.reason, pymqi.CMQC.MQRC_TRUNCATED_MSG_ACCEPTED)
            self.assertEqual(ex.original_length,  # pylint: disable=no-member
                             4097)
            self.assertEqual(len(ex.message), 0)
            self.assertEqual(md_put.PutDate, md_get.PutDate)

    def test_put_string(self):
        md = pymqi.MD()
        # file coding defined (utf-8)
        self.queue.put('тест', md)  # Cyrillic (non-ascii) characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        # In Python3 pymqi should put unicode string
        if version_info.major >= 3:
            self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
            self.assertEqual(md.CodedCharSetId, 1208)
        else:
            self.assertEqual(md.Format, pymqi.CMQC.MQFMT_NONE)

    def test_put_string_with_ccsid_and_format(self):
        md = pymqi.MD(
            CodedCharSetId=1208,  # coding: utf8 is set
            Format=pymqi.CMQC.MQFMT_STRING)

        self.queue.put('тест', md)  # Cyrillic (non-ascii) characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        # In Python3 pymqi should put unicode string
        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
        self.assertEqual(md.CodedCharSetId, 1208)

    def test_put_unicode(self):
        self.queue.put(u'\u0442\u0435\u0441\u0442')  # Unicode characters

        md = pymqi.MD()
        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
        self.assertEqual(md.CodedCharSetId, 1208)

    def test_put_unicode_with_ccsid_and_format(self):
        md = pymqi.MD(
            CodedCharSetId=1208,
            Format=pymqi.CMQC.MQFMT_STRING)

        self.queue.put(u'\u0442\u0435\u0441\u0442', md)  # Unicode characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
        self.assertEqual(md.CodedCharSetId, 1208)

    def test_put1_bytes(self):
        md = pymqi.MD()
        self.qmgr.put1(self.queue_name, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82', md)  # Non-ascii characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_NONE)

    def test_put1_string(self):
        md = pymqi.MD()
        # file coding defined (utf-8)
        self.qmgr.put1(self.queue_name, 'тест', md)  # Cyrillic (non-ascii) characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        # In Python3 pymqi should put unicode string
        if version_info.major >= 3:
            self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
            self.assertEqual(md.CodedCharSetId, 1208)
        else:
            self.assertEqual(md.Format, pymqi.CMQC.MQFMT_NONE)

    def test_put1_string_with_ccsid_and_format(self):
        md = pymqi.MD(
            CodedCharSetId=1208,  # coding: utf8 is set
            Format=pymqi.CMQC.MQFMT_STRING)

        self.qmgr.put1(self.queue_name, 'тест', md)  # Cyrillic (non-ascii) characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        # In Python3 pymqi should put unicode string
        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
        self.assertEqual(md.CodedCharSetId, 1208)

    def test_put1_unicode(self):
        self.qmgr.put1(self.queue_name, u'\u0442\u0435\u0441\u0442')  # Unicode characters

        md = pymqi.MD()
        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
        self.assertEqual(md.CodedCharSetId, 1208)

    def test_put1_unicode_with_ccsid_and_format(self):
        md = pymqi.MD(
            CodedCharSetId=1208,
            Format=pymqi.CMQC.MQFMT_STRING)

        self.qmgr.put1(self.queue_name, u'\u0442\u0435\u0441\u0442', md)  # Unicode characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_STRING)
        self.assertEqual(md.CodedCharSetId, 1208)

    def test_put1_bytes(self):
        md = pymqi.MD()
        self.qmgr.put1(self.queue_name, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82', md)  # Non-ascii characters

        gmo = pymqi.GMO()
        gmo.Options = gmo.Options & ~ pymqi.CMQC.MQGMO_CONVERT
        message = self.queue.get(None, md, gmo)

        self.assertEqual(message, b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')
        self.assertEqual(md.Format, pymqi.CMQC.MQFMT_NONE)

    def test_put1(self):
        input_msg = b'Hello world!'
        self.qmgr.put1(self.queue_name, input_msg)
        # now get the message from the queue
        queue = pymqi.Queue(self.qmgr, self.queue_name)
        result_msg = queue.get()
        self.assertEqual(input_msg, result_msg)

    def test_inquire(self):
        attribute = pymqi.CMQC.MQCA_Q_MGR_NAME
        expected_value = utils.py3str2bytes(self.queue_manager)
        attribute_value = self.qmgr.inquire(attribute)
        self.assertEqual(len(attribute_value), pymqi.CMQC.MQ_Q_MGR_NAME_LENGTH)
        self.assertEqual(attribute_value.strip(), expected_value)


if __name__ == "__main__":
    unittest.main()
