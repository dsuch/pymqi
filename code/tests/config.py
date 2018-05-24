import os.path
import utils


class PATHS:
    TESTS_DIR = os.path.normpath(os.path.dirname(__file__))


class MQ:

    # Queue manager connection setup
    class QM:
        NAME = os.environ.get('PYMQI_TEST_QM_NAME', 'MQTEST')
        HOST = os.environ.get('PYMQI_TEST_QM_HOST', '127.0.0.1')
        PORT = os.environ.get('PYMQI_TEST_QM_PORT', '8887')
        CHANNEL = os.environ.get('PYMQI_TEST_QM_CHANNEL', 'CH1')
        TRANSPORT = os.environ.get('PYMQI_TEST_QM_TRANSPORT', 'TCP')
        USER = os.environ.get('PYMQI_TEST_QM_USER', '')
        PASSWORD = os.environ.get('PYMQI_TEST_QM_PASSWORD', '')

        MIN_COMMAND_LEVEL = os.environ.get(
            'PYMQI_TEST_QM_MIN_COMMAND_LEVEL', '800')

        class CONN_AUTH:
            # user/password connection authentication is a MQ >= 8.0 feature
            SUPPORTED = os.environ.get('PYMQI_TEST_QM_CONN_AUTH_SUPPORTED',
                                       '1')
            # Set to OPTIONAL or REQUIRED
            # OPTIONAL: If a user ID and password are provided by a client
            # application then they must be a valid pair. It is not mandatory
            # to provide user + password, though.
            # REQUIRED: A valid user ID and password are mandatory.
            USE_PW = os.environ.get(
                'PYMQI_TEST_QM_CONN_AUTH_USE_PW', 'OPTIONAL')

            # Delay time in seconds for API call returns in case of auth
            # failures (some DoS-countermeasure). For testing purposes we
            # usually want this as fast as possible. This value gets used in
            # create_mq_objects.py for the creation of the queue manager conn
            # auth.
            FAIL_DELAY = os.environ.get(
                'PYMQI_TEST_QM_CONN_AUTH_FAIL_DELAY', '0')
            
    # Queue naming setup
    class QUEUE:
        PREFIX = os.environ.get('PYMQI_TEST_QUEUE_PREFIX', '')
        QUEUE_NAMES = {
            'TestRFH2PutGet': PREFIX + 'TEST.PYMQI.RFH2PUTGET',
            'TestQueueManager': PREFIX + 'TEST.PYMQI.QUEUEMANAGER',
            }

    # convenience attribute derived from above settings, may be used for tests
    # that mandate the MQSERVER environment variable
    # E.g. MQSERVER="SVRCONN.1/TCP/mq.example.org(1777)"
    MQSERVER = '%(channel)s/%(transport)s/%(host)s(%(port)s)' % {
        'channel': QM.CHANNEL,
        'transport': QM.TRANSPORT,
        'host': QM.HOST,
        'port': QM.PORT,
        }


if __name__ == '__main__':
    utils.print_config(PATHS, MQ)
