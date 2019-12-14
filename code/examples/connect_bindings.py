# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = 'QM1'
qmgr = pymqi.connect(queue_manager)

qmgr.disconnect()
