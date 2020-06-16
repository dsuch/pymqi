"""Test PCF usage."""
import os
from unittest import skip
from ddt import data
from ddt import ddt

from test_setup import Tests  # noqa
from test_setup import main  # noqa

import pymqi

@ddt
class TestPCF(Tests):
    """Class for MQ PCF testing."""

    pcf = None
    messages_dir = os.path.join(os.path.dirname(__file__), "messages")

    @classmethod
    def setUpClass(cls):
        """Initialize test environment."""
        super(TestPCF, cls).setUpClass()

        # max length of queue names is 48 characters
        cls.queue_name = "{prefix}PCF.QUEUE".format(prefix=cls.prefix)
        cls.pcf = pymqi.PCFExecute(cls.qmgr, response_wait_interval=600)

    @classmethod
    def tearDownClass(cls):
        """Tear down test environment."""
        cls.pcf.disconnect()

        super(TestPCF, cls).tearDownClass()

    def setUp(self):
        """Set up tesing environment."""
        super(TestPCF, self).setUp()

        self.create_queue(self.queue_name)

    def tearDown(self):
        """Delete the created objects."""
        if self.queue_name:
            self.delete_queue(self.queue_name)

        super(TestPCF, self).tearDown()

    @skip('Not implemented')
    def test_mqcfbf(self):
        """Test MQCFBF PCF byte string filter parameter."""

    def test_mqcfbs(self):
        """Test MQCFBS PCF byte string parameter.

        Also uses MQCFIN and MQCFIL as parameters
        """
        attrs = []
        attrs.append(pymqi.CFBS(Parameter=pymqi.CMQCFC.MQBACF_GENERIC_CONNECTION_ID,
                                String=b''))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQCFC.MQIACF_CONN_INFO_TYPE,
                                Value=pymqi.CMQCFC.MQIACF_CONN_INFO_CONN))
        attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_CONNECTION_ATTRS,
                                Values=[pymqi.CMQCFC.MQIACF_ALL]))

        object_filters = []
        object_filters.append(
            pymqi.CFIF(Parameter=pymqi.CMQC.MQIA_APPL_TYPE,
                       Operator=pymqi.CMQCFC.MQCFOP_EQUAL,
                       FilterValue=pymqi.CMQC.MQAT_USER))

        results = self.pcf.MQCMD_INQUIRE_CONNECTION(attrs, object_filters)

        self.assertGreater(len(results), 0)

    def test_mqcfif(self):
        """Test string filter MQCFIF.

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

        results = self.pcf.MQCMD_INQUIRE_Q(attrs, object_filters)

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH] > 0,
                            'Found Queue with depth {}'.format(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]))
    def test_mqcfsf(self):
        """Test string filter MQCFSF.

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

        results = self.pcf.MQCMD_INQUIRE_Q(attrs, object_filters)

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(not result[pymqi.CMQC.MQCA_Q_DESC].startswith(b'MQ'),
                            'Found Queue with description {}'.format(result[pymqi.CMQC.MQCA_Q_DESC]))
            self.assertTrue(pymqi.CMQC.MQCA_Q_DESC in result,
                            'Attribute {} is not returned'.format(result[pymqi.CMQC.MQCA_Q_DESC]))

    @data([], [b'One'], [b'One', b'Two', b'Three'])
    def test_mqcfsl(self, value):
        """Test MQCFSL PCF string list parameter.

        Also uses MQCFST and MQCFIN as parameters
        """
        attrs = []
        attrs.append(pymqi.CFST(Parameter=pymqi.CMQC.MQCA_NAMELIST_NAME,
                                String='{}NAMELIST'.format(self.prefix).encode()))
        attrs.append(pymqi.CFSL(Parameter=pymqi.CMQC.MQCA_NAMES,
                                Strings=value))
        attrs.append(pymqi.CFIN(Parameter=pymqi.CMQCFC.MQIACF_REPLACE,
                                Value=pymqi.CMQCFC.MQRP_YES))

        try:
            self.pcf.MQCMD_CREATE_NAMELIST(attrs)
        except Exception:  # pylint: disable=broad-except
            self.fail('Exception occurs!')
        else:
            attrs = []
            attrs.append(pymqi.CFST(Parameter=pymqi.CMQC.MQCA_NAMELIST_NAME,
                                    String='{}NAMELIST'.format(self.prefix).encode()))
            attrs.append(pymqi.CFIL(Parameter=pymqi.CMQCFC.MQIACF_NAMELIST_ATTRS,
                                    Values=[pymqi.CMQC.MQCA_NAMES, pymqi.CMQC.MQIA_NAME_COUNT]))

            results = self.pcf.MQCMD_INQUIRE_NAMELIST(attrs)

            self.assertEqual(results[0][pymqi.CMQC.MQIA_NAME_COUNT], len(value))

            if results[0][pymqi.CMQC.MQIA_NAME_COUNT] > 0:
                for item in results[0][pymqi.CMQC.MQCA_NAMES]:
                    item = item.strip()
                    self.assertTrue(item in value, '{} value not in values list'.format(item))
                    value.remove(item)

            attrs = []
            attrs.append(pymqi.CFST(Parameter=pymqi.CMQC.MQCA_NAMELIST_NAME,
                                    String='{}NAMELIST'.format(self.prefix).encode()))
            self.pcf.MQCMD_DELETE_NAMELIST(attrs)


    @data([], [1], [1, 2, 3, 4, 5])
    def test_arbitrary_message_with_mqcfil(self, value):
        """Test arbitrary message with MQCFIL."""
        message = pymqi.CFH(Version=pymqi.CMQCFC.MQCFH_VERSION_1,
                            Type=pymqi.CMQCFC.MQCFT_USER,
                            ParameterCount=1).pack()
        message = message + pymqi.CFIL(Parameter=1,
                                       Values=value).pack()

        queue = pymqi.Queue(self.qmgr, self.queue_name,
                            pymqi.CMQC.MQOO_INPUT_AS_Q_DEF + pymqi.CMQC.MQOO_OUTPUT)

        put_md = pymqi.MD(Format=pymqi.CMQC.MQFMT_PCF)
        queue.put(message, put_md)

        get_opts = pymqi.GMO(
            Options=pymqi.CMQC.MQGMO_NO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING,
            Version=pymqi.CMQC.MQGMO_VERSION_2,
            MatchOptions=pymqi.CMQC.MQMO_MATCH_CORREL_ID)
        get_md = pymqi.MD(MsgId=put_md.MsgId)  # pylint: disable=no-member
        message = queue.get(None, get_md, get_opts)
        queue.close()
        message = pymqi.PCFExecute.unpack(message)

        self.assertTrue(isinstance(message[0][1], list),
                        'Returned value is not list: {}'.format(type(message[0][1])))

        self.assertTrue(len(message[0][1]) == len(value), 'List length is different!')

        for item in message[0][1]:
            self.assertTrue(item in value, '{} value not in values list'.format(item))
            value.remove(item)

    def test_mqcfgr_mqcfin64_mqcfil64(self):
        """Test arbitrary message with MQCFIL."""
        message = pymqi.CFH(Version=pymqi.CMQCFC.MQCFH_VERSION_1,
                            Type=pymqi.CMQCFC.MQCFT_USER,
                            ParameterCount=4).pack()
        message += pymqi.CFST(Parameter=pymqi.CMQC.MQCA_Q_MGR_NAME,
                                    String=b'QM1').pack()
        # group1
        message += pymqi.CFGR(Parameter=pymqi.CMQCFC.MQGACF_Q_STATISTICS_DATA,
                                    ParameterCount=3).pack()
        message += pymqi.CFST(Parameter=pymqi.CMQC.MQCA_Q_NAME,
                                    String=b'SYSTEM.ADMIN.COMMAND.QUEUE').pack()
        message += pymqi.CFIN64(Parameter=pymqi.CMQCFC.MQIAMO_Q_MIN_DEPTH,
                                    Value=10).pack()
        message += pymqi.CFIL64(Parameter=pymqi.CMQCFC.MQIAMO64_AVG_Q_TIME,
                                    Values=[1, 2, 3]).pack()
        # group2
        message += pymqi.CFGR(Parameter=pymqi.CMQCFC.MQGACF_Q_STATISTICS_DATA,
                                    ParameterCount=3).pack()
        message += pymqi.CFST(Parameter=pymqi.CMQC.MQCA_Q_NAME,
                                    String=b'SYSTEM.ADMIN.COMMAND.QUEUE2').pack()
        message += pymqi.CFIN64(Parameter=pymqi.CMQCFC.MQIAMO_Q_MIN_DEPTH,
                                    Value=20).pack()
        message += pymqi.CFIL64(Parameter=pymqi.CMQCFC.MQIAMO64_AVG_Q_TIME,
                                    Values=[111, 222]).pack()

        message += pymqi.CFST(Parameter=pymqi.CMQCFC.MQCAMO_START_TIME,
                              String=b'10.41.58').pack()

        queue = pymqi.Queue(self.qmgr, self.queue_name,
                            pymqi.CMQC.MQOO_INPUT_AS_Q_DEF + pymqi.CMQC.MQOO_OUTPUT)

        put_md = pymqi.MD(Format=pymqi.CMQC.MQFMT_PCF)
        queue.put(message, put_md)

        get_opts = pymqi.GMO(
            Options=pymqi.CMQC.MQGMO_NO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING,
            Version=pymqi.CMQC.MQGMO_VERSION_2,
            MatchOptions=pymqi.CMQC.MQMO_MATCH_CORREL_ID)
        get_md = pymqi.MD(MsgId=put_md.MsgId)  # pylint: disable=no-member
        message = queue.get(None, get_md, get_opts)
        queue.close()
        message, _ = pymqi.PCFExecute.unpack(message)

        self.assertEqual(b'QM1\x00', message[pymqi.CMQC.MQCA_Q_MGR_NAME])
        self.assertEqual(b'10.41.58', message[pymqi.CMQCFC.MQCAMO_START_TIME])
        item1 = message[pymqi.CMQCFC.MQGACF_Q_STATISTICS_DATA][0]
        item2 = message[pymqi.CMQCFC.MQGACF_Q_STATISTICS_DATA][1]
        self.assertEqual(b'SYSTEM.ADMIN.COMMAND.QUEUE\x00\x00', item1[pymqi.CMQC.MQCA_Q_NAME])
        self.assertEqual(10, item1[pymqi.CMQCFC.MQIAMO_Q_MIN_DEPTH])
        self.assertEqual([1, 2, 3], item1[pymqi.CMQCFC.MQIAMO64_AVG_Q_TIME])

        self.assertEqual(b'SYSTEM.ADMIN.COMMAND.QUEUE2\x00', item2[pymqi.CMQC.MQCA_Q_NAME])
        self.assertEqual(20, item2[pymqi.CMQCFC.MQIAMO_Q_MIN_DEPTH])
        self.assertEqual([111, 222], item2[pymqi.CMQCFC.MQIAMO64_AVG_Q_TIME])

    def test_unpack_group(self):
        binary_message = open(os.path.join(self.messages_dir, "statistics_q.dat"), "rb").read()

        message, _ = pymqi.PCFExecute.unpack(binary_message)

        self.assertEqual(message[pymqi.CMQC.MQCA_Q_MGR_NAME].strip(), b'mq_mgr1')
        self.assertEqual(message[pymqi.CMQCFC.MQCAMO_START_DATE], b'2020-06-15\x00\x00')
        self.assertEqual(len(message[pymqi.CMQCFC.MQGACF_Q_STATISTICS_DATA]), 16)

        item = message[pymqi.CMQCFC.MQGACF_Q_STATISTICS_DATA][0]
        self.assertEqual(item[pymqi.CMQC.MQCA_Q_NAME].strip(), b'SYSTEM.ADMIN.COMMAND.QUEUE')
        self.assertEqual(item[pymqi.CMQCFC.MQIAMO_PUTS], [14, 0])

    def test_mqcfbs_old(self):
        """Test byte string MQCFBS with old style."""
        attrs = {
            pymqi.CMQCFC.MQBACF_GENERIC_CONNECTION_ID: pymqi.ByteString(''),
            pymqi.CMQCFC.MQIACF_CONN_INFO_TYPE: pymqi.CMQCFC.MQIACF_CONN_INFO_CONN,
            pymqi.CMQCFC.MQIACF_CONNECTION_ATTRS: [pymqi.CMQCFC.MQIACF_ALL]
        }
        fltr = pymqi.Filter(pymqi.CMQC.MQIA_APPL_TYPE).equal(pymqi.CMQC.MQAT_USER)

        results = self.pcf.MQCMD_INQUIRE_CONNECTION(attrs, [fltr])

        self.assertGreater(len(results), 0)

    @data(pymqi.CMQCFC.MQIACF_ALL, [pymqi.CMQCFC.MQIACF_ALL],
          pymqi.CMQC.MQCA_Q_DESC, [pymqi.CMQC.MQCA_Q_DESC],
          [pymqi.CMQC.MQIA_CURRENT_Q_DEPTH, pymqi.CMQC.MQCA_Q_DESC])
    def test_object_filter_int_old_queue(self, value):
        """Test object filter with integer attribute. Old style."""
        attrs = {
            pymqi.CMQC.MQCA_Q_NAME: b'*',
            pymqi.CMQCFC.MQIACF_Q_ATTRS: value
            }

        filter_depth = pymqi.Filter(pymqi.CMQC.MQIA_CURRENT_Q_DEPTH).greater(0)

        results = self.pcf.MQCMD_INQUIRE_Q(attrs, [filter_depth])

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH] > 0,
                            'Found Queue with depth {}'.format(result[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]))

    @skip('https://stackoverflow.com/questions/62250844/ibm-mq-pcf-parameters-order')
    @data(pymqi.CMQCFC.MQIACF_ALL, [pymqi.CMQCFC.MQIACF_ALL],
          pymqi.CMQCFC.MQCACH_DESC, [pymqi.CMQCFC.MQCACH_DESC],
          [pymqi.CMQCFC.MQCACH_DESC, pymqi.CMQCFC.MQIACH_CHANNEL_TYPE])
    def test_object_filter_int_old_channel(self, value):
        """Test object filter with integer attribute. Old style."""
        attrs = {
            pymqi.CMQCFC.MQCACH_CHANNEL_NAME: b'*',
            pymqi.CMQCFC.MQIACF_CHANNEL_ATTRS: value}

        filter_type = pymqi.Filter(pymqi.CMQCFC.MQIACH_CHANNEL_TYPE).equal(pymqi.CMQC.MQCHT_SVRCONN)

        results = self.pcf.MQCMD_INQUIRE_CHANNEL(attrs, [filter_type])

        self.assertTrue(results, 'Channel not found')
        for result in results:
            self.assertTrue(result[pymqi.CMQCFC.MQIACH_CHANNEL_TYPE] == pymqi.CMQC.MQCHT_SVRCONN,
                            'Found Channel with type {}'.format(result[pymqi.CMQCFC.MQIACH_CHANNEL_TYPE]))

    def test_object_filter_str_old(self):
        """Test object filter with string attribute. Old style."""
        attrs = {
            pymqi.CMQC.MQCA_Q_NAME: b'*',
            pymqi.CMQCFC.MQIACF_Q_ATTRS: [pymqi.CMQC.MQIA_CURRENT_Q_DEPTH, pymqi.CMQC.MQCA_Q_DESC]
            }

        filter_depth = pymqi.Filter(pymqi.CMQC.MQCA_Q_DESC).like(b'IBM MQ *')

        results = self.pcf.MQCMD_INQUIRE_Q(attrs, [filter_depth])

        self.assertTrue(results, 'Queue not found')
        for result in results:
            self.assertTrue(not result[pymqi.CMQC.MQCA_Q_DESC].startswith(b'MQ'),
                            'Found Queue with description {}'.format(result[pymqi.CMQC.MQCA_Q_DESC]))

    def test_disconnect(self):
        """Test disconnect for PCF object."""
        # pylint: disable=protected-access

        pcf = pymqi.PCFExecute(self.qmgr)

        self.assertTrue(pcf._reply_queue)
        self.assertTrue(pcf._reply_queue_name)

        pcf.disconnect()

        self.assertTrue(self.qmgr)
        self.assertFalse(pcf._reply_queue)
        self.assertFalse(pcf._reply_queue_name)

if __name__ == "__main__":
    main(module="test_pcf")
