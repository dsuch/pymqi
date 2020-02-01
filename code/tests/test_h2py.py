""" Tests for making sure modules generated automatically by h2py have no
unwanted duplicate entries.
"""

# stdlib
import inspect
import unittest
from struct import calcsize

# PyMQI
from pymqi import CMQC, CMQXC, CMQCFC

ignore_dups = []

class Testh2py(unittest.TestCase):
    """ Test that modules generated automatically by h2py have no unwanted duplicate entries.
    """

    def test_h2py(self):
        """ Test that modules generated automatically by h2py have no unwanted duplicate entries.
        """

        errors = []
        test_passed = False

        for mod in CMQC, CMQXC, CMQCFC:
            mq_attrs = []
            mq_attrs_count = {}

            source_lines = inspect.getsourcelines(mod)
            if mod == CMQC:
                source_lines[0].append('MQ_DUMMY_1 = 1')
                source_lines[0].append('MQ_DUMMY_1 = 1')
                source_lines[0].append('if calcsize("P") == 8:')
                source_lines[0].append('    MQ_DUMMY_2 = 1')
                source_lines[0].append('else:')
                source_lines[0].append('    MQ_DUMMY_2 = 1')
            process = True
            in_if = False
            indent = 0
            for line in source_lines[0]:
                len_line = len(line)
                len_line_lstrip = len(line.lstrip(' '))
                line = line.strip()

                if line:
                    if "".join(line.split()) == ''.join('if calcsize("P") == 8:'.split()):
                        in_if = True
                        process = calcsize("P") == 8
                    elif "".join(line.split()) == 'else:' and in_if:
                        process = not process
                    else:
                        if in_if and not indent:
                            indent = len_line - len_line_lstrip
                        elif (len_line - len_line_lstrip) < indent and line[0] != '#':
                            in_if = False
                            process = True
                            indent = 0

                        if line.startswith("MQ") and process:
                            line_split = line.split()
                            mq_attr = line_split[0].split(",")[0]
                            if len(line_split) > 1 and line_split[1] == '=':
                                mq_attrs.append(mq_attr)

            for mq_attr in mq_attrs:
                if mq_attr not in mq_attrs_count:
                    mq_attrs_count[mq_attr] = 1
                else:
                    mq_attrs_count[mq_attr] += 1

            for mq_attr, count in mq_attrs_count.items():
                if count == 1 or(count == 2 and mq_attr in ignore_dups):
                    continue
                elif mq_attr.startswith('MQ_DUMMY'):
                    test_passed = True
                else:
                    item = "%s is defined %d times in %s" % (mq_attr, count, mod)
                    errors.append(item)

        if errors:
            msg = "\n" + "\n".join(errors)
            self.fail(msg)
        
        self.assertTrue(test_passed, 'Test does not found DUMMY duplicate entries!')

if __name__ == "__main__":
    unittest.main()