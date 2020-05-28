"""Test PCF usage
"""

import unittest

import config
import utils
import env

import pymqi

class TestPCF(unittest.TestCase):
    def setUp(self):
        # max length of queue names is 48 characters
        self.queue_name = "{prefix}PCF.QUEUE".format(prefix=config.MQ.QUEUE.PREFIX)
        self.queue_manager = config.MQ.QM.NAME
        self.channel = config.MQ.QM.CHANNEL
        self.host = config.MQ.QM.HOST
        self.port = config.MQ.QM.PORT
        self.user = config.MQ.QM.USER
        self.password = config.MQ.QM.PASSWORD

        self.conn_info = "{0}({1})".format(self.host, self.port)

        self.qmgr = pymqi.QueueManager(None)
        try:
            self.qmgr.connectTCPClient(self.queue_manager, pymqi.CD(), self.channel, self.conn_info, self.user, self.password)
        except pymqi.MQMIError as ex:
            if ex.comp == 2:
                raise ex

        self.create_queue(self.queue_name)

    def tearDown(self):
        """Delete the created objects.
        """
        if self.queue_name:
            self.delete_queue(self.queue_name)
        self.qmgr.disconnect()

    def create_queue(self, queue_name):
        queue_type = pymqi.CMQC.MQQT_LOCAL
        max_depth = 5000

        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQC.MQIA_Q_TYPE: queue_type,
                pymqi.CMQC.MQCA_Q_DESC: utils.py3str2bytes('PCF testing'),
                pymqi.CMQCFC.MQIACF_REPLACE: pymqi.CMQCFC.MQRP_YES}
        pcf = pymqi.PCFExecute(self.qmgr)
        pcf.MQCMD_CREATE_Q(args)
        pcf.disconnect()

    def delete_queue(self, queue_name):

        pcf = pymqi.PCFExecute(self.qmgr)
        args = {pymqi.CMQC.MQCA_Q_NAME: utils.py3str2bytes(queue_name),
                pymqi.CMQCFC.MQIACF_PURGE: pymqi.CMQCFC.MQPO_YES}
        pcf.MQCMD_DELETE_Q(args)
        pcf.disconnect()

    @unittest.skip('Not implemented')
    def test_mqcfbs(self):
        pass

    def test_mqcfbf(self):
        """Test byte string MQCFBF
        Also uses MQCFST, MQCFIN and MQCFIL as parameters
        """
        attrs = []
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQCFC.MQCACF_SUB_NAME,
                                String=b'SYSTEM.DEFAULT.SUB'))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQCFC.MQIACF_SUB_TYPE,
                                Value=pymqi.CMQCFC.MQSUBTYPE_ADMIN))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_SUB_ATTRS,
                                Values=[pymqi.CMQCFC.MQBACF_DESTINATION_CORREL_ID]))

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_SUBSCRIPTION(attrs)
        pcf.disconnect()

        self.assertTrue(results, 'Subscription not found')
        for result in results:
            self.assertTrue(len(result[pymqi.CMQCFC.MQBACF_DESTINATION_CORREL_ID]) == 24,
                            'Correlation ID has wrong size ({})'.format(len(result[pymqi.CMQCFC.MQBACF_DESTINATION_CORREL_ID])))

    def test_mqcfif(self):
        """Test string filter MQCFIF
        Also uses MQCFST, MQCFIN and MQCFIL as parameters
        """
        attrs = []
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQC.MQCA_Q_NAME,
                                String=b'*'))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQC.MQIA_Q_TYPE,
                                Value=pymqi.CMQC.MQQT_LOCAL))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_Q_ATTRS,
                                Values=[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH, pymqi.CMQC.MQCA_Q_DESC]))

        object_filters = []
        object_filters.append(
            pymqi.CFIF(Parameter=pymqi.CMQC.MQIA_CURRENT_Q_DEPTH,
                       Operator=pymqi.CMQCFC.MQCFOP_GREATER,
                       FilterValue=0))

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_Q(attrs, object_filters)
        pcf.disconnect()

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH] > 0,
                            'Found Queue with depth {}'.format(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]))

    def test_mqcfsf(self):
        """Test string filter MQCFSF
        Also uses MQCFST, MQCFIN and MQCFIL as parameters
        """
        attrs = []
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQC.MQCA_Q_NAME,
                                String=b'*'))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQC.MQIA_Q_TYPE,
                                Value=pymqi.CMQC.MQQT_LOCAL))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_Q_ATTRS,
                                Values=[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH, pymqi.CMQC.MQCA_Q_DESC]))

        object_filters = []
        object_filters.append(
            pymqi.CFSF(Parameter=pymqi.CMQC.MQCA_Q_DESC,
                       Operator=pymqi.CMQCFC.MQCFOP_LIKE,
                       FilterValue=b'IBM MQ*'))

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_Q(attrs, object_filters)
        pcf.disconnect()

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(not result[pymqi.CMQC.MQCA_Q_DESC].startswith(b'MQ'),
                            'Found Queue with description {}'.format(result[pymqi.CMQC.MQCA_Q_DESC]))
            self.assertTrue(pymqi.CMQC.MQCA_Q_DESC in result,
                            'Attribute {} is not returned'.format(result[pymqi.CMQC.MQCA_Q_DESC]))

    def test_mqcfsl(self):
        """Test string filter MQCFSL
        Also uses MQCFST as parameters
        """
        attrs = []
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQC.MQCA_TOPIC_NAME,
                                String=b'*'))

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_TOPIC_NAMES(attrs)
        pcf.disconnect()

        self.assertTrue(results, 'Topics not found')
        for result in results:
            self.assertTrue(isinstance(result[pymqi.CMQCFC.MQCACF_TOPIC_NAMES], list),
                            'Returned value is not list: {}'.format(type(result[pymqi.CMQCFC.MQCACF_TOPIC_NAMES])))

    def test_arbitrary_message_with_mqcfil(self):
        """Test arbitrary message with MQCFIL
        """
        message = pymqi.CFH(Version=pymqi.CMQCFC.MQCFH_VERSION_1,
                    Type=pymqi.CMQCFC.MQCFT_USER,
                    ParameterCount=1).pack()
        message = message + pymqi.CFIL(Parameter=1,
                                       Values=[1,2,3,4,5]).pack()

        queue = pymqi.Queue(self.qmgr, self.queue_name,
                            pymqi.CMQC.MQOO_INPUT_AS_Q_DEF + pymqi.CMQC.MQOO_OUTPUT)

        put_md = pymqi.MD(Format=pymqi.CMQC.MQFMT_PCF)
        queue.put(message, put_md)

        get_opts = pymqi.GMO(
                    Options=pymqi.CMQC.MQGMO_NO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING,
                    Version=pymqi.CMQC.MQGMO_VERSION_2,
                    MatchOptions=pymqi.CMQC.MQMO_MATCH_CORREL_ID)
        get_md = pymqi.MD(MsgId=put_md.MsgId)
        message = queue.get(None, get_md, get_opts)
        queue.close()
        message = pymqi.PCFExecute.unpack(message)

        self.assertTrue(isinstance(message[1], list),
                        'Returned value is not list: {}'.format(type(message[1])))


    def test_object_filter_int_old(self):
        attrs = {
            pymqi.CMQC.MQCA_Q_NAME : b'*',
            pymqi.CMQCFC.MQIACF_Q_ATTRS : [pymqi.CMQC.MQIA_CURRENT_Q_DEPTH, pymqi.CMQC.MQCA_Q_DESC]
            }

        filter_depth = pymqi.Filter(pymqi.CMQC.MQIA_CURRENT_Q_DEPTH).greater(0)

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_Q(attrs, [filter_depth])
        pcf.disconnect()

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH] > 0,
                            'Found Queue with depth {}'.format(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]))

    def test_object_filter_str_old(self):
        attrs = {
            pymqi.CMQC.MQCA_Q_NAME : b'*',
            pymqi.CMQCFC.MQIACF_Q_ATTRS : [pymqi.CMQC.MQIA_CURRENT_Q_DEPTH, pymqi.CMQC.MQCA_Q_DESC]
            }

        filter_depth =  pymqi.Filter(pymqi.CMQC.MQCA_Q_DESC).like(b'IBM MQ *')

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_Q(attrs, [filter_depth])
        pcf.disconnect()

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(not result[pymqi.CMQC.MQCA_Q_DESC].startswith(b'MQ'),
                            'Found Queue with description {}'.format(result[pymqi.CMQC.MQCA_Q_DESC]))

    def test_disconnect(self):
        pcf = pymqi.PCFExecute(self.qmgr)

        self.assertTrue(pcf._reply_queue)
        self.assertTrue(pcf._reply_queue_name)

        pcf.disconnect()

        self.assertTrue(self.qmgr)
        self.assertFalse(pcf._reply_queue)
        self.assertFalse(pcf._reply_queue_name)

    def test_connections(self):
        attrs = {
            pymqi.CMQCFC.MQBACF_GENERIC_CONNECTION_ID: pymqi.ByteString(''),
            pymqi.CMQCFC.MQIACF_CONN_INFO_TYPE: pymqi.CMQCFC.MQIACF_CONN_INFO_CONN,
            pymqi.CMQCFC.MQIACF_CONNECTION_ATTRS: [pymqi.CMQCFC.MQIACF_ALL]
        }
        fltr = pymqi.Filter(pymqi.CMQC.MQIA_APPL_TYPE).equal(pymqi.CMQC.MQAT_USER)

        pcf = pymqi.PCFExecute(self.qmgr)
        results = pcf.MQCMD_INQUIRE_CONNECTION(attrs, [fltr])
        pcf.disconnect

        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()
