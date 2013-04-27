""" Tests for pymqi.QueueManager class.
"""

# stdlib
import sys
from uuid import uuid4

sys.path.insert(0, "..")

# nose
from nose.tools import eq_

# testfixtures
from testfixtures import Replacer

# PyMQI
import pymqi


def test_is_connected():
    """ Makes sure the QueueManager's 'is_connected' property works as expected.
    """
    with Replacer() as r:
        queue_manager = uuid4().hex
        channel = uuid4().hex
        host = uuid4().hex
        port = "1431"
        conn_info = "%s(%s)" % (host, port)

        for expected in(True, False):

            def _connectTCPClient(*ignored_args, **ignored_kwargs):
                pass

            def _getattr(self, name):
                if expected:
                    class _DummyMethod(object):
                        pass
                    # The mere fact of not raising an exception will suffice
                    # for QueueManager._is_connected to understand it as an
                    # all's OK condition.
                    return _DummyMethod
                else:
                    raise Exception()

            r.replace('pymqi.QueueManager.connectTCPClient', _connectTCPClient)
            r.replace('pymqi.PCFExecute.__getattr__', _getattr)

            qmgr = pymqi.QueueManager(None)
            qmgr.connectTCPClient(queue_manager, pymqi.cd(), channel, conn_info)

            eq_(qmgr.is_connected, expected)
