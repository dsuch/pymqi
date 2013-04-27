""" All sorts of tests related to making the API PEP-8 compliant.
"""

# stdlib
import sys

sys.path.insert(0, "..")

# nose
from nose.tools import eq_

# PyMQI
import pymqi

def test_backward_compatibility():
    """ Makes sure all the relevant classes and methods have backward-compatible
    replacements.
    """
    eq_(pymqi.gmo, pymqi.GMO)
    eq_(pymqi.pmo, pymqi.PMO)
    eq_(pymqi.od, pymqi.OD)
    eq_(pymqi.md, pymqi.MD)
    eq_(pymqi.cd, pymqi.CD)
    eq_(pymqi.sco, pymqi.SCO)
    eq_(pymqi.QueueManager.connectWithOptions, pymqi.QueueManager.connect_with_options)
    eq_(pymqi.QueueManager.connectTCPClient, pymqi.QueueManager.connect_tcp_client)
    eq_(pymqi.QueueManager.getHandle, pymqi.QueueManager.get_handle)
    eq_(pymqi.PCFExecute.stringifyKeys, pymqi.PCFExecute.stringify_keys)
