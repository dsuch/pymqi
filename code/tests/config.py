import os
import os.path


class PATHS:
    TESTS_DIR = os.path.normpath(os.path.dirname(__file__))


class MQ:

    # Queue manager connection setup
    class QM:
        NAME = os.environ.get('PYMQI_TEST_QM_NAME', 'QM01')
        HOST = os.environ.get('PYMQI_TEST_QM_HOST', '127.0.0.1')
        PORT = os.environ.get('PYMQI_TEST_QM_PORT', '31414')
        CHANNEL = os.environ.get('PYMQI_TEST_QM_CHANNEL', 'SVRCONN.1')
        USER = os.environ.get('PYMQI_TEST_QM_USER', 'myuser')
        PASSWORD = os.environ.get('PYMQI_TEST_QM_PASSWORD', 'mypassword')

    # Queue naming setup
    class QUEUE:
        PREFIX = os.environ.get('PYMQI_TEST_QUEUE_PREFIX', '')
        QUEUE_NAMES = {
            'TestRFH2PutGet': PREFIX + 'TEST.PYMQI.RFH2PUTGET',
            }

