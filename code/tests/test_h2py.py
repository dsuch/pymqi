""" Tests for making sure modules generated automatically by h2py have no
unwanted duplicate entries.
"""

# stdlib
import sys
import inspect
import unittest

sys.path.insert(0, "..")

# PyMQI
from pymqi import CMQC, CMQXC, CMQCFC

ignore_dups = ["MQOD_CURRENT_LENGTH", "MQPMO_CURRENT_LENGTH", "MQRC_NONE",
               "MQACH_CURRENT_LENGTH", "MQCD_CURRENT_LENGTH", "MQCD_LENGTH_4",
               "MQCD_LENGTH_5", "MQCD_LENGTH_6", "MQCD_LENGTH_7", "MQCD_LENGTH_8",
               "MQCD_LENGTH_9", "MQCFIF_STRUC_LENGTH", "MQCFGR_STRUC_LENGTH",
               "MQCFIN64_STRUC_LENGTH", "MQCFIN_STRUC_LENGTH", "MQACH_LENGTH_1"]

class Testh2py(unittest.TestCase):

    def test_h2py(self):
        """ Test that modules generated automatically by h2py have no unwanted duplicate entries.
        """

        errors = []

        for mod in CMQC, CMQXC, CMQCFC:
            mq_attrs = []
            mq_attrs_count = {}
            dups = {}
            source_lines = inspect.getsourcelines(mod)
            for line in source_lines[0]:
                if line:
                    line = line.strip()
                    if line.startswith("MQ"):
                        mq_attr = line.split()[0].split(",")[0]
                        mq_attrs.append(mq_attr)

            for mq_attr in mq_attrs:
                if mq_attr not in mq_attrs_count:
                    mq_attrs_count[mq_attr] = 1
                else:
                    mq_attrs_count[mq_attr] += 1

            for mq_attr, count in mq_attrs_count.items():
                if count == 1 or(count == 2 and mq_attr in ignore_dups):
                    continue
                else:
                    item = "%s is defined %d times in %s" % (mq_attr, count, mod)
                    errors.append(item)

        if errors:
            msg = "\n" + "\n".join(errors)
            self.fail(msg)

if __name__ == "__main__":
    unittest.main()
