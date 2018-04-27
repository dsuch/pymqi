"""
Created on 15 Nov 2010

@author: hannes
"""

import os
import unittest
import pymqi
from pymqi import CMQC


class TestRFH2(unittest.TestCase):
    """This test case tests the RFH2 class and it's methods.
    """

    messages_dir = os.path.join(os.path.dirname(__file__), "messages")

    def setUp(self):
        """ Create a new queue manager (TESTPMQI).
        Must be run as a user that has 'mqm' access.

        """
        self.single_rfh2_message = open(
            os.path.join(self.messages_dir, "single_rfh2.dat"), "rb").read()
        self.single_rfh2_message_not_well_formed = \
            self.single_rfh2_message[0:117] + self.single_rfh2_message[121:]

    def test_parse_rfh2(self):
        """Test that a known correct 3rd party message parses correctly.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message)
            self.assertEqual(len(rfh2.get()), 14, "Number of attributes incorrect.  Should be %i? But is %s" % (14, str(len(rfh2.get()))))
            self.assertEqual(rfh2["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2["StrucId"])))
            self.assertEqual(rfh2["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2["Version"])))
            self.assertEqual(rfh2["StrucLength"], 284, "StrucLength has incorrect value. Should be: %i But is: %s" % (284, str(rfh2["StrucLength"])))
            self.assertEqual(rfh2["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2["Encoding"])))
            self.assertEqual(rfh2["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["CodedCharSetId"])))
            self.assertEqual(rfh2["Format"], CMQC.MQFMT_STRING, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_NONE, str(rfh2["Format"])))
            self.assertEqual(rfh2["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2["Flags"])))
            self.assertEqual(rfh2["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["NameValueCCSID"])))
            self.assertEqual(rfh2["pscLength"], 152, "pscLength has incorrect value. Should be: %i But is: %s" % (152, str(rfh2["pscLength"])))
            self.assertEqual(rfh2["psc"], b"<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2["psc"]) + "<"))
            self.assertEqual(rfh2["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2["testFolderLength"])))
            self.assertEqual(rfh2["testFolder"], b"<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2["testFolder"])))
            self.assertEqual(rfh2["mcdLength"], 28, "mcdLength has incorrect value. Should be: %i But is: %s" % (28, str(rfh2["mcdLength"])))
            self.assertEqual(rfh2["mcd"], b"<mcd><Msd>xmlnsc</Msd></mcd>", "mcd has incorrect value. Should be: %s But is: %s" % ("<mcd><Msd>xmlnsc</Msd></mcd>", str(rfh2["mcd"])))
        except Exception as e:
            self.fail(e)

    def test_parse_default_rfh2(self):
        """Test parsing of default RFH2 only.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message[0:36])
            self.assertEqual(len(rfh2.get()), 8, "Number of attributes incorrect.  Should be 8? But is %s" % str(len(rfh2.get())))
            self.assertEqual(rfh2["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2["StrucId"])))
            self.assertEqual(rfh2["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2["Version"])))
            self.assertEqual(rfh2["StrucLength"], 284, "StrucLength has incorrect value. Should be: %i But is: %s" % (284, str(rfh2["StrucLength"])))
            self.assertEqual(rfh2["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2["Encoding"])))
            self.assertEqual(rfh2["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["CodedCharSetId"])))
            self.assertEqual(rfh2["Format"], CMQC.MQFMT_STRING, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_NONE, str(rfh2["Format"])))
            self.assertEqual(rfh2["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2["Flags"])))
            self.assertEqual(rfh2["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["NameValueCCSID"])))
        except Exception as e:
            self.fail(e.message)

    def test_parse_rfh2_with_correct_encoding(self):
        """Parse known correct message with it's correct encoding.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message, 273)
            self.assertEqual(len(rfh2.get()), 14, "Number of attributes incorrect.  Should be 12? But is %s" % str(len(rfh2.get())))
            self.assertEqual(rfh2["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2["StrucId"])))
            self.assertEqual(rfh2["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2["Version"])))
            self.assertEqual(rfh2["StrucLength"], 284, "StrucLength has incorrect value. Should be: %i But is: %s" % (284, str(rfh2["StrucLength"])))
            self.assertEqual(rfh2["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2["Encoding"])))
            self.assertEqual(rfh2["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["CodedCharSetId"])))
            self.assertEqual(rfh2["Format"], CMQC.MQFMT_STRING, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_NONE, str(rfh2["Format"])))
            self.assertEqual(rfh2["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2["Flags"])))
            self.assertEqual(rfh2["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["NameValueCCSID"])))
            self.assertEqual(rfh2["pscLength"], 152, "pscLength has incorrect value. Should be: %i But is: %s" % (152, str(rfh2["pscLength"])))
            self.assertEqual(rfh2["psc"], b"<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2["psc"]) + "<"))
            self.assertEqual(rfh2["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2["testFolderLength"])))
            self.assertEqual(rfh2["testFolder"], b"<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2["testFolder"])))
            self.assertEqual(rfh2["mcdLength"], 28, "mcdLength has incorrect value. Should be: %i But is: %s" % (28, str(rfh2["mcdLength"])))
            self.assertEqual(rfh2["mcd"], b"<mcd><Msd>xmlnsc</Msd></mcd>", "mcd has incorrect value. Should be: %s But is: %s" % ("<mcd><Msd>xmlnsc</Msd></mcd>", str(rfh2["mcd"])))

        except Exception as e:
            self.fail(e)

    def test_parse_rfh2_with_incorrect_encoding(self):
        """Parse known correct message with it's incorrect encoding.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message, 546)
        except pymqi.PYIFError as e:
            self.assertEqual(str(e), "PYMQI Error: RFH2 - Buffer too short. Expected: 469827584 Buffer Length: 333", "Exception Does not mathc expected. Expected: %s But is: %s" % ("PYMQI Error: RFH2 - Buffer too short. Expected: 469827584 Buffer Length: 333", str(e)))

    def test_add_folder(self):
        """Test the addition of a XML folder.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message)
            self.assertEqual(len(rfh2.get()), 14, "Number of attributes incorrect.  Should be 12? But is %s" % str(len(rfh2.get())))
            self.assertEqual(rfh2["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2["StrucId"])))
            self.assertEqual(rfh2["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2["Version"])))
            self.assertEqual(rfh2["StrucLength"], 284, "StrucLength has incorrect value. Should be: %i But is: %s" % (284, str(rfh2["StrucLength"])))
            self.assertEqual(rfh2["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2["Encoding"])))
            self.assertEqual(rfh2["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["CodedCharSetId"])))
            self.assertEqual(rfh2["Format"], CMQC.MQFMT_STRING, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_NONE, str(rfh2["Format"])))
            self.assertEqual(rfh2["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2["Flags"])))
            self.assertEqual(rfh2["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["NameValueCCSID"])))
            self.assertEqual(rfh2["pscLength"], 152, "pscLength has incorrect value. Should be: %i But is: %s" % (152, str(rfh2["pscLength"])))
            self.assertEqual(rfh2["psc"], b"<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2["psc"]) + "<"))
            self.assertEqual(rfh2["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2["testFolderLength"])))
            self.assertEqual(rfh2["testFolder"], b"<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2["testFolder"])))
            self.assertEqual(rfh2["mcdLength"], 28, "mcdLength has incorrect value. Should be: %i But is: %s" % (28, str(rfh2["mcdLength"])))
            self.assertEqual(rfh2["mcd"], b"<mcd><Msd>xmlnsc</Msd></mcd>", "mcd has incorrect value. Should be: %s But is: %s" % ("<mcd><Msd>xmlnsc</Msd></mcd>", str(rfh2["mcd"])))

            rfh2.add_folder(b"<testFolder2><testVar>testValue</testVar></testFolder2>")

            self.assertEqual(len(rfh2.get()), 16, "Number of attributes incorrect.  Should be 12? But is %s" % str(len(rfh2.get())))
            self.assertEqual(rfh2["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2["StrucId"])))
            self.assertEqual(rfh2["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2["Version"])))
            self.assertEqual(rfh2["StrucLength"], 344, "StrucLength has incorrect value. Should be: %i But is: %s" % (344, str(rfh2["StrucLength"])))
            self.assertEqual(rfh2["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2["Encoding"])))
            self.assertEqual(rfh2["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["CodedCharSetId"])))
            self.assertEqual(rfh2["Format"], CMQC.MQFMT_STRING, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_NONE, str(rfh2["Format"])))
            self.assertEqual(rfh2["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2["Flags"])))
            self.assertEqual(rfh2["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["NameValueCCSID"])))
            self.assertEqual(rfh2["pscLength"], 152, "pscLength has incorrect value. Should be: %i But is: %s" % (152, str(rfh2["pscLength"])))
            self.assertEqual(rfh2["psc"], b"<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2["psc"]) + "<"))
            self.assertEqual(rfh2["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2["testFolderLength"])))
            self.assertEqual(rfh2["testFolder"], b"<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2["testFolder"])))
            self.assertEqual(rfh2["mcdLength"], 28, "mcdLength has incorrect value. Should be: %i But is: %s" % (28, str(rfh2["mcdLength"])))
            self.assertEqual(rfh2["mcd"], b"<mcd><Msd>xmlnsc</Msd></mcd>", "mcd has incorrect value. Should be: %s But is: %s" % ("<mcd><Msd>xmlnsc</Msd></mcd>", str(rfh2["mcd"])))
            self.assertEqual(rfh2["testFolder2Length"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2["testFolderLength"])))
            self.assertEqual(rfh2["testFolder2"], b"<testFolder2><testVar>testValue</testVar></testFolder2> ", "testFolder2 has incorrect value. Should be: %s But is: %s" % ("<testFolder2><testVar>testValue</testVar></testFolder2> ", str(rfh2["testFolder2"])))

        except Exception as e:
            self.fail(e)

    def test_rfh2_pack(self):
        """Test pack() by comparing output of pack() against original message.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message)
            self.assertEqual(len(rfh2.get()), 14, "Number of attributes incorrect.  Should be 12? But is %s" % str(len(rfh2.get())))
            self.assertEqual(rfh2["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2["StrucId"])))
            self.assertEqual(rfh2["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2["Version"])))
            self.assertEqual(rfh2["StrucLength"], 284, "StrucLength has incorrect value. Should be: %i But is: %s" % (284, str(rfh2["StrucLength"])))
            self.assertEqual(rfh2["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2["Encoding"])))
            self.assertEqual(rfh2["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["CodedCharSetId"])))
            self.assertEqual(rfh2["Format"], CMQC.MQFMT_STRING, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_NONE, str(rfh2["Format"])))
            self.assertEqual(rfh2["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2["Flags"])))
            self.assertEqual(rfh2["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2["NameValueCCSID"])))
            self.assertEqual(rfh2["pscLength"], 152, "pscLength has incorrect value. Should be: %i But is: %s" % (152, str(rfh2["pscLength"])))
            self.assertEqual(rfh2["psc"], b"<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2["psc"]) + "<"))
            self.assertEqual(rfh2["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2["testFolderLength"])))
            self.assertEqual(rfh2["testFolder"], b"<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2["testFolder"])))
            self.assertEqual(rfh2["mcdLength"], 28, "mcdLength has incorrect value. Should be: %i But is: %s" % (28, str(rfh2["mcdLength"])))
            self.assertEqual(rfh2["mcd"], b"<mcd><Msd>xmlnsc</Msd></mcd>", "mcd has incorrect value. Should be: %s But is: %s" % ("<mcd><Msd>xmlnsc</Msd></mcd>", str(rfh2["mcd"])))
            self.assertEqual(self.single_rfh2_message[0:rfh2["StrucLength"]], rfh2.pack(), "result of RFH2.pack() not equal to original buffer used in unpack?")
        except Exception as e:
            self.fail(e)

    def test_rfh2_create(self):
        """Test the creation of a brand new RFH2.  Compare the resulting byte array against identical known correct message.
        """

        rfh2 = pymqi.RFH2()
        new_rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message)
            new_rfh2["StrucId"] = CMQC.MQRFH_STRUC_ID
            new_rfh2["Version"] = CMQC.MQRFH_VERSION_2
            new_rfh2["StrucLength"] = 188
            new_rfh2["Encoding"] = 273
            new_rfh2["CodedCharSetId"] = 1208
            new_rfh2["Format"] = CMQC.MQFMT_STRING
            new_rfh2["Flags"] = 0
            new_rfh2["NameValueCCSID"] = 1208
            new_rfh2.add_folder(b"<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc>")
            new_rfh2.add_folder(b"<testFolder><testVar>testValue</testVar></testFolder>")
            new_rfh2.add_folder(b"<mcd><Msd>xmlnsc</Msd></mcd>")
            self.assertEqual(self.single_rfh2_message[0:rfh2["StrucLength"]], new_rfh2.pack(encoding=273), "New RFH2 Header does not match publishmessage?")
        except Exception as e:
            self.fail(e)

    def test_incorrect_strucid_exception(self):
        """Test exception that occurs if StrucId is incorrect.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message[116:])
        except pymqi.PYIFError as e:
            self.assertEqual(str(e),
                             "PYMQI Error: RFH2 - StrucId not MQRFH_STRUC_ID. Value: b'ame>'",
                             "StrucId not = '%s'" % CMQC.MQRFH_STRUC_ID)

    def test_buffer_too_short_for_default_rfh2_exception(self):
        """Test exception occurs when buffer is too short for default RFH2.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message[0:32])
        except pymqi.PYIFError as e:
            self.assertEqual(str(e),
                             "PYMQI Error: RFH2 - Buffer too short. Should be 36 bytes or longer.  Buffer Length: 32",
                             "Not Buffer to short exception?")

    def test_buffer_too_short_for_complete_rfh2_exception(self):
        """Test exception occurs when buffer is too short for complete RFH2.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message[0:188])
        except pymqi.PYIFError as e:
            self.assertEqual(str(e),
                             "PYMQI Error: RFH2 - Buffer too short. Expected: 284 Buffer Length: 188",
                             "Not Buffer to short to parse complete RFH2 exception?")

    def test_folder_not_well_formed_exception_on_parse(self):
        """Test exception when parsing a message that contains not well formed XML folder.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.unpack(self.single_rfh2_message_not_well_formed)
        except pymqi.PYIFError as e:
            self.assertEqual(str(e).count("XML Folder not well formed"), 1)

    def test_folder_not_well_formed_exception_on_add(self):
        """Test exception when adding a not well formed XML folder.
        """

        rfh2 = pymqi.RFH2()
        try:
            rfh2.add_folder(b"<a><b>c</a>")
        except pymqi.PYIFError as e:
            # Don't depend on the actual XML library getting used (lxml or
            # minidom produce different error messages)
            self.assertTrue(
                str(e).startswith("PYMQI Error: RFH2 - XML Folder not well formed. Exception:"),
                "Not 'XML Folder not well formed' exception (add_folder): %s" % (e, ))

    def test_encoding_on_pack_big_endian(self):
        """Test that pack() creates numeric fields with correct encoding. Big endian Test.
        """

        try:
            rfh2 = pymqi.RFH2()
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_FLOAT_S390)[4:8], b"\x00\x00\x00\x02")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_INTEGER_NORMAL)[4:8], b"\x00\x00\x00\x02")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_DECIMAL_NORMAL)[4:8], b"\x00\x00\x00\x02")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_FLOAT_IEEE_NORMAL)[4:8], b"\x00\x00\x00\x02")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_INTEGER_NORMAL + CMQC.MQENC_DECIMAL_NORMAL)[4:8], b"\x00\x00\x00\x02")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_INTEGER_NORMAL + CMQC.MQENC_FLOAT_IEEE_NORMAL)[4:8], b"\x00\x00\x00\x02")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_DECIMAL_NORMAL + CMQC.MQENC_FLOAT_IEEE_NORMAL)[4:8], b"\x00\x00\x00\x02")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_INTEGER_NORMAL + CMQC.MQENC_DECIMAL_NORMAL + CMQC.MQENC_FLOAT_IEEE_NORMAL)[4:8], b"\x00\x00\x00\x02")
        except Exception as e:
            self.fail(e)

    def test_encoding_on_pack_small_endian(self):
        """Test that pack() creates numeric fields with correct encoding. Small endian Test.
        """

        try:
            rfh2 = pymqi.RFH2()
            self.assertEqual(rfh2.pack()[4:8], b"\x02\x00\x00\x00")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_NATIVE)[4:8], b"\x02\x00\x00\x00")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_INTEGER_REVERSED)[4:8], b"\x02\x00\x00\x00")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_DECIMAL_REVERSED)[4:8], b"\x02\x00\x00\x00")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_FLOAT_IEEE_REVERSED)[4:8], b"\x02\x00\x00\x00")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_INTEGER_REVERSED + CMQC.MQENC_DECIMAL_REVERSED)[4:8], b"\x02\x00\x00\x00")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_INTEGER_REVERSED + CMQC.MQENC_FLOAT_IEEE_REVERSED)[4:8], b"\x02\x00\x00\x00")
            self.assertEqual(rfh2.pack(encoding=CMQC.MQENC_DECIMAL_REVERSED + CMQC.MQENC_FLOAT_IEEE_REVERSED)[4:8], b"\x02\x00\x00\x00")
        except Exception as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()
