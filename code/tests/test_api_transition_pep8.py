""" All sorts of tests related to making the API PEP-8 compliant.
"""
import unittest

# PyMQI
import pymqi


class TestApiTransitionPEP8(unittest.TestCase):
    """All sorts of tests related to making the API PEP-8 compliant."""

    def test_backward_compatibility(self):
        """Test backward-compatible.

        Makes sure all the relevant classes and methods have
        backward-compatible replacements.
        """
        self.assertEqual(pymqi.gmo, pymqi.GMO)
        self.assertEqual(pymqi.pmo, pymqi.PMO)
        self.assertEqual(pymqi.od, pymqi.OD)
        self.assertEqual(pymqi.md, pymqi.MD)
        self.assertEqual(pymqi.cd, pymqi.CD)
        self.assertEqual(pymqi.sco, pymqi.SCO)
        self.assertEqual(pymqi.QueueManager.connectWithOptions, pymqi.QueueManager.connect_with_options)
        self.assertEqual(pymqi.QueueManager.connectTCPClient, pymqi.QueueManager.connect_tcp_client)
        self.assertEqual(pymqi.QueueManager.getHandle, pymqi.QueueManager.get_handle)
        self.assertEqual(pymqi.PCFExecute.stringifyKeys, pymqi.PCFExecute.stringify_keys)
