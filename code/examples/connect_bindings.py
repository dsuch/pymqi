# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import pymqi

queue_manager = 'QM1'
with pymqi.connect(queue_manager) as qmgr:
    pass
