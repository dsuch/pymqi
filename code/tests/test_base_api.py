# -*- coding: utf8 -*-
"""Test base API."""
from sys import version_info
#from sys.version_info import major as py_ver
import unittest

import config
import os
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
        """Test nontruncated with big enough buffer."""
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

    def test_get_nontruncated_big_msg(self):
        """Test get nontruncated big message"""
        tbl = bytes.maketrans(bytearray(range(256)),
                              bytearray([ord(b'a') + b % 26 for b in range(256)]))

        self.message = os.urandom(1024*1024*3).translate(tbl)
        md_put = self._put_message()
        gmo = pymqi.GMO()

        md_get = pymqi.MD()
        md_get.MsgId = md_put.MsgId

        message = self.queue.get(None, md_get, gmo)

        self.assertEqual(self.message, message)
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

if __name__ == "__main__":
    unittest.main()
