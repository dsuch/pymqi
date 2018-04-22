'''
Created on 15 Nov 2010

@author: hannes
'''

import unittest
import os.path
import config
import env
import pymqi
from pymqi import CMQC


class TestRFH2PutGet(unittest.TestCase):
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

        self.multiple_rfh2_message = open(
            os.path.join(self.messages_dir, "multiple_rfh2.dat"), "rb").read()
        self.multiple_rfh2_message_not_well_formed = \
            self.multiple_rfh2_message[0:117] + self.multiple_rfh2_message[121:]

        queue_manager = config.MQ.QM.NAME
        channel = config.MQ.QM.CHANNEL
        conn_info = "%s(%s)" % (config.MQ.QM.HOST, config.MQ.QM.PORT)
        queue_name = config.MQ.QUEUE.QUEUE_NAMES['TestRFH2PutGet']

        self.qmgr = None
        if pymqi.__mqbuild__ == 'server':
            self.qmgr = pymqi.QueueManager(queue_manager)
        else:
            self.qmgr = pymqi.QueueManager(None)
            self.qmgr.connect_tcp_client(
                queue_manager, pymqi.cd(), channel, conn_info,
                user=config.MQ.QM.USER, password=config.MQ.QM.PASSWORD)
        self.put_queue = pymqi.Queue(self.qmgr, queue_name)
        self.get_queue = pymqi.Queue(self.qmgr, queue_name)
        self.clear_queue(self.get_queue)

    def tearDown(self):
        """ Delete queue manager (TESTPMQI).

        """
        self.put_queue.close()
        self.get_queue.close()
        self.qmgr.disconnect()

    def clear_queue(self, queue):
        try:
            while(1):
                queue.get()
        except Exception as e:
            if e.reason == 2033:
                return
            else:
                raise e


    def test_get_rfh2_single(self):
        """Use get_rfh2 to get a known correct 3rd party message that contains a single RFH2 header.
        """
        try:

            put_mqmd = pymqi.md()
            put_mqmd["Format"] = CMQC.MQFMT_RF_HEADER_2
            put_mqmd["Encoding"] = 273
            put_mqmd["CodedCharSetId"] = 1208
            self.put_queue.put(self.single_rfh2_message, put_mqmd)

            get_mqmd = pymqi.md()
            get_opts = pymqi.gmo()
            rfh2_list = []
            msg = self.get_queue.get_rfh2(None, get_mqmd, get_opts, rfh2_list)

            self.assertEqual(len(rfh2_list), 1, "Number of RFH2's incorrect.  Should be one.  But is %i" % len(rfh2_list))

            rfh2 = rfh2_list[0]
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
            self.assertEqual(rfh2["psc"], "<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2["psc"]) + "<"))
            self.assertEqual(rfh2["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2["testFolderLength"])))
            self.assertEqual(rfh2["testFolder"], "<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2["testFolder"])))
            self.assertEqual(rfh2["mcdLength"], 28, "mcdLength has incorrect value. Should be: %i But is: %s" % (28, str(rfh2["mcdLength"])))
            self.assertEqual(rfh2["mcd"], "<mcd><Msd>xmlnsc</Msd></mcd>", "mcd has incorrect value. Should be: %s But is: %s" % ("<mcd><Msd>xmlnsc</Msd></mcd>", str(rfh2["mcd"])))

            self.assertEqual(msg, self.single_rfh2_message[rfh2["StrucLength"]:], "Message Payloads do not match?")
        except Exception as e:
            self.fail(e)


    def test_get_rfh2_multiple(self):
        """Use get_rfh2 to get a known correct 3rd party message containing Multiples RFH2 headers.
        """

        try:

            put_mqmd = pymqi.md()
            put_mqmd["Format"] = CMQC.MQFMT_RF_HEADER_2
            put_mqmd["Encoding"] = 273
            put_mqmd["CodedCharSetId"] = 1208
            self.put_queue.put(self.multiple_rfh2_message, put_mqmd)

            get_mqmd = pymqi.md()
            get_opts = pymqi.gmo()
            rfh2_list = []
            msg = self.get_queue.get_rfh2(None, get_mqmd, get_opts, rfh2_list)

            self.assertEqual(len(rfh2_list), 2, "Number of RFH2's incorrect.  Should be 2.  But is %i" % len(rfh2_list))

            rfh2_1 = rfh2_list[0]
            self.assertEqual(len(rfh2_1.get()), 12, "Number of attributes incorrect.  Should be 12? But is %s" % str(len(rfh2_1.get())))
            self.assertEqual(rfh2_1["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2_1["StrucId"])))
            self.assertEqual(rfh2_1["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2_1["Version"])))
            self.assertEqual(rfh2_1["StrucLength"], 252, "StrucLength has incorrect value. Should be: %i But is: %s" % (284, str(rfh2_1["StrucLength"])))
            self.assertEqual(rfh2_1["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2_1["Encoding"])))
            self.assertEqual(rfh2_1["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2_1["CodedCharSetId"])))
            self.assertEqual(rfh2_1["Format"], CMQC.MQFMT_RF_HEADER_2, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_RF_HEADER_2, str(rfh2_1["Format"])))
            self.assertEqual(rfh2_1["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2_1["Flags"])))
            self.assertEqual(rfh2_1["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2_1["NameValueCCSID"])))
            self.assertEqual(rfh2_1["pscLength"], 152, "pscLength has incorrect value. Should be: %i But is: %s" % (152, str(rfh2_1["pscLength"])))
            self.assertEqual(rfh2_1["psc"], "<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2_1["psc"]) + "<"))
            self.assertEqual(rfh2_1["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2_1["testFolderLength"])))
            self.assertEqual(rfh2_1["testFolder"], "<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2_1["testFolder"])))

            rfh2_2 = rfh2_list[1]
            self.assertEqual(len(rfh2_2.get()), 14, "Number of attributes incorrect.  Should be 14? But is %s" % str(len(rfh2_2.get())))
            self.assertEqual(rfh2_2["StrucId"], CMQC.MQRFH_STRUC_ID, "StrucId has incorrect value. Should be: %s But is: %s" % (CMQC.MQRFH_STRUC_ID, str(rfh2_2["StrucId"])))
            self.assertEqual(rfh2_2["Version"], CMQC.MQRFH_VERSION_2, "Version has incorrect value. Should be: %i But is: %s" % (CMQC.MQRFH_VERSION_2, str(rfh2_2["Version"])))
            self.assertEqual(rfh2_2["StrucLength"], 284, "StrucLength has incorrect value. Should be: %i But is: %s" % (284, str(rfh2_2["StrucLength"])))
            self.assertEqual(rfh2_2["Encoding"], 273, "Encoding has incorrect value. Should be: %i But is: %s" % (273, str(rfh2_2["Encoding"])))
            self.assertEqual(rfh2_2["CodedCharSetId"], 1208, "CodedCharSetId has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2_2["CodedCharSetId"])))
            self.assertEqual(rfh2_2["Format"], CMQC.MQFMT_STRING, "Format has incorrect value. Should be: %s But is: %s" % (CMQC.MQFMT_STRING, str(rfh2_2["Format"])))
            self.assertEqual(rfh2_2["Flags"], 0, "Flags has incorrect value. Should be: %i But is: %s" % (0, str(rfh2_2["Flags"])))
            self.assertEqual(rfh2_2["NameValueCCSID"], 1208, "NameValueCCSID has incorrect value. Should be: %i But is: %s" % (1208, str(rfh2_2["NameValueCCSID"])))
            self.assertEqual(rfh2_2["pscLength"], 152, "pscLength has incorrect value. Should be: %i But is: %s" % (152, str(rfh2_2["pscLength"])))
            self.assertEqual(rfh2_2["psc"], "<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", "psc has incorrect value. Should be: %s But is: %s" % ("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc> ", ">" + str(rfh2_2["psc"]) + "<"))
            self.assertEqual(rfh2_2["testFolderLength"], 56, "testFolderLength has incorrect value. Should be: %i But is: %s" % (56, str(rfh2_2["testFolderLength"])))
            self.assertEqual(rfh2_2["testFolder"], "<testFolder><testVar>testValue</testVar></testFolder>   ", "testFolder has incorrect value. Should be: %s But is: %s" % ("<testFolder><testVar>testValue</testVar></testFolder>   ", str(rfh2_2["testFolder"])))
            self.assertEqual(rfh2_2["mcdLength"], 28, "mcdLength has incorrect value. Should be: %i But is: %s" % (28, str(rfh2_2["mcdLength"])))
            self.assertEqual(rfh2_2["mcd"], "<mcd><Msd>xmlnsc</Msd></mcd>", "mcd has incorrect value. Should be: %s But is: %s" % ("<mcd><Msd>xmlnsc</Msd></mcd>", str(rfh2_2["mcd"])))


            self.assertEqual(msg, self.multiple_rfh2_message[rfh2_1["StrucLength"] + rfh2_2["StrucLength"]:], "Message Payloads do not match?")

        except Exception as e:
            self.fail(e)

    def test_put_rfh2_single(self):
        """Create and put a new rfh2 and use get to get it from the queue.  Compare it against know correct message.
        """
        try:

            put_mqmd = pymqi.md()
            put_mqmd["Format"] = CMQC.MQFMT_RF_HEADER_2
            put_mqmd["Encoding"] = 273
            put_mqmd["CodedCharSetId"] = 1208

            put_opts = pymqi.pmo()

            put_rfh2 = pymqi.RFH2()
            put_rfh2["StrucId"] = CMQC.MQRFH_STRUC_ID
            put_rfh2["Version"] = CMQC.MQRFH_VERSION_2
            put_rfh2["StrucLength"] = 188
            put_rfh2["Encoding"] = 273
            put_rfh2["CodedCharSetId"]= 1208
            put_rfh2["Format"] =  CMQC.MQFMT_STRING
            put_rfh2["Flags"] = 0
            put_rfh2["NameValueCCSID"] = 1208
            put_rfh2.add_folder("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc>")
            put_rfh2.add_folder("<testFolder><testVar>testValue</testVar></testFolder>")
            put_rfh2.add_folder("<mcd><Msd>xmlnsc</Msd></mcd>")
            put_msg = "<testData><testVar>testValue</testVar></testData>"
            self.put_queue.put_rfh2(put_msg, put_mqmd, put_opts, [put_rfh2])

            get_mqmd = pymqi.md()
            get_opts = pymqi.gmo()
            get_msg = self.get_queue.get(None, get_mqmd, get_opts)

            self.assertEqual(get_msg, self.single_rfh2_message, "Message got from Queue does not match known correct RFH2 message.")
        except Exception as e:
            self.fail(e)

    def test_put_rfh2_multiple(self):
        """Create and put a new RFH2 message containing multiple RFH2 headers and use get to get it from the queue.  Compare it against know correct message.
        """
        try:

            put_mqmd = pymqi.md()
            put_mqmd["Format"] = CMQC.MQFMT_RF_HEADER_2
            put_mqmd["Encoding"] = 273
            put_mqmd["CodedCharSetId"] = 1208

            put_opts = pymqi.pmo()

            put_rfh2_1 = pymqi.RFH2()
            put_rfh2_1["StrucId"] = CMQC.MQRFH_STRUC_ID
            put_rfh2_1["Version"] = CMQC.MQRFH_VERSION_2
            put_rfh2_1["StrucLength"] = 188
            put_rfh2_1["Encoding"] = 273
            put_rfh2_1["CodedCharSetId"]= 1208
            put_rfh2_1["Format"] =  CMQC.MQFMT_RF_HEADER_2
            put_rfh2_1["Flags"] = 0
            put_rfh2_1["NameValueCCSID"] = 1208
            put_rfh2_1.add_folder("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc>")
            put_rfh2_1.add_folder("<testFolder><testVar>testValue</testVar></testFolder>")

            put_rfh2_2 = pymqi.RFH2()
            put_rfh2_2["StrucId"] = CMQC.MQRFH_STRUC_ID
            put_rfh2_2["Version"] = CMQC.MQRFH_VERSION_2
            put_rfh2_2["StrucLength"] = 188
            put_rfh2_2["Encoding"] = 273
            put_rfh2_2["CodedCharSetId"]= 1208
            put_rfh2_2["Format"] =  CMQC.MQFMT_STRING
            put_rfh2_2["Flags"] = 0
            put_rfh2_2["NameValueCCSID"] = 1208
            put_rfh2_2.add_folder("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc>")
            put_rfh2_2.add_folder("<testFolder><testVar>testValue</testVar></testFolder>")
            put_rfh2_2.add_folder("<mcd><Msd>xmlnsc</Msd></mcd>")

            put_msg = "<testData><testVar>testValue</testVar></testData>"
            self.put_queue.put_rfh2(put_msg, put_mqmd, put_opts, [put_rfh2_1, put_rfh2_2])

            get_mqmd = pymqi.md()
            get_opts = pymqi.gmo()

            get_msg = self.get_queue.get(None, get_mqmd, get_opts)

            self.assertEqual(get_msg, self.multiple_rfh2_message, "Message got from Queue does not match known correct RFH2 message.")

        except Exception as e:
            self.fail(e)

    def test_put_get_rfh2_single(self):
        """Create and put a new rfh2 with put_rfh2 and use get_rfh2 to get it from the queue.  Compare it against know correct message.
        """
        try:

            put_mqmd = pymqi.md()
            put_mqmd["Format"] = CMQC.MQFMT_RF_HEADER_2
            put_mqmd["Encoding"] = 273
            put_mqmd["CodedCharSetId"] = 1208

            put_opts = pymqi.pmo()

            put_rfh2 = pymqi.RFH2()
            put_rfh2["StrucId"] = CMQC.MQRFH_STRUC_ID
            put_rfh2["Version"] = CMQC.MQRFH_VERSION_2
            put_rfh2["StrucLength"] = 188
            put_rfh2["Encoding"] = 273
            put_rfh2["CodedCharSetId"]= 1208
            put_rfh2["Format"] =  CMQC.MQFMT_STRING
            put_rfh2["Flags"] = 0
            put_rfh2["NameValueCCSID"] = 1208
            put_rfh2.add_folder("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc>")
            put_rfh2.add_folder("<testFolder><testVar>testValue</testVar></testFolder>")
            put_rfh2.add_folder("<mcd><Msd>xmlnsc</Msd></mcd>")
            put_msg = b"<testData><testVar>testValue</testVar></testData>"

            put_rfh2_list = [put_rfh2]
            self.put_queue.put_rfh2(put_msg, put_mqmd, put_opts, put_rfh2_list)

            get_mqmd = pymqi.md()
            get_opts = pymqi.gmo()
            get_rfh2_list = []
            get_msg = self.get_queue.get_rfh2(None, get_mqmd, get_opts, get_rfh2_list)

            self.assertEqual(len(get_rfh2_list), len(put_rfh2_list), "Number of RFH2's incorrect.  Should be %i.  But is %i" % (len(get_rfh2_list), len(put_rfh2_list)))
            self.assertEqual(get_rfh2_list[0].get(), put_rfh2_list[0].get()), "Put and Get RFH2 Lists do not match."
            self.assertEqual(get_msg, put_msg, "Put and Get messages do not match.")

        except Exception as e:
            self.fail(e)

    def test_put_get_rfh2_multiple(self):
        """Create and put a new RFH2 message containing multiple RFH2 headers with put_rfh2 and use get_rfh2 to get it from the queue.  Compare it against know correct message.
        """

        try:
            put_mqmd = pymqi.md()
            put_mqmd["Format"] = CMQC.MQFMT_RF_HEADER_2
            put_mqmd["Encoding"] = 273
            put_mqmd["CodedCharSetId"] = 1208

            put_opts = pymqi.pmo()

            put_rfh2_1 = pymqi.RFH2()
            put_rfh2_1["StrucId"] = CMQC.MQRFH_STRUC_ID
            put_rfh2_1["Version"] = CMQC.MQRFH_VERSION_2
            put_rfh2_1["StrucLength"] = 188
            put_rfh2_1["Encoding"] = 273
            put_rfh2_1["CodedCharSetId"]= 1208
            put_rfh2_1["Format"] =  CMQC.MQFMT_RF_HEADER_2
            put_rfh2_1["Flags"] = 0
            put_rfh2_1["NameValueCCSID"] = 1208
            put_rfh2_1.add_folder("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc>")
            put_rfh2_1.add_folder("<testFolder><testVar>testValue</testVar></testFolder>")

            put_rfh2_2 = pymqi.RFH2()
            put_rfh2_2["StrucId"] = CMQC.MQRFH_STRUC_ID
            put_rfh2_2["Version"] = CMQC.MQRFH_VERSION_2
            put_rfh2_2["StrucLength"] = 188
            put_rfh2_2["Encoding"] = 273
            put_rfh2_2["CodedCharSetId"]= 1208
            put_rfh2_2["Format"] =  CMQC.MQFMT_STRING
            put_rfh2_2["Flags"] = 0
            put_rfh2_2["NameValueCCSID"] = 1208
            put_rfh2_2.add_folder("<psc><Command>RegSub</Command><Topic>$topictree/topiccat/topic</Topic><QMgrName>DebugQM</QMgrName><QName>PUBOUT</QName><RegOpt>PersAsPub</RegOpt></psc>")
            put_rfh2_2.add_folder("<testFolder><testVar>testValue</testVar></testFolder>")
            put_rfh2_2.add_folder("<mcd><Msd>xmlnsc</Msd></mcd>")
            put_rfh2_list = [put_rfh2_1, put_rfh2_2]
            put_msg = b"<testData><testVar>testValue</testVar></testData>"

            self.put_queue.put_rfh2(put_msg, put_mqmd, put_opts, put_rfh2_list)

            get_mqmd = pymqi.md()
            get_opts = pymqi.gmo()
            get_rfh2_list = []
            get_msg = self.get_queue.get_rfh2(None, get_mqmd, get_opts, get_rfh2_list)

            self.assertEqual(len(get_rfh2_list), len(put_rfh2_list), "Number of RFH2's incorrect.  Should be %i.  But is %i" % (len(get_rfh2_list), len(put_rfh2_list)))
            self.assertEqual(get_rfh2_list[0].get(), put_rfh2_list[0].get()), "Put and Get RFH2 Lists do not match."
            self.assertEqual(get_rfh2_list[1].get(), put_rfh2_list[1].get()), "Put and Get RFH2 Lists do not match."
            self.assertEqual(get_msg, put_msg, "Put and Get messages do not match.")

        except Exception as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()
