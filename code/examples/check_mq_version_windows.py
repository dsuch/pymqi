# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import logging
import _winreg

logging.basicConfig(level=logging.INFO)

key_name = 'Software\\IBM\\MQSeries\\CurrentVersion'

try:
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_name)
except WindowsError:
    logging.info('Could not find IBM MQ-related information in Windows registry.')
else:
    version = _winreg.QueryValueEx(key, 'VRMF')[0]
    logging.info('IBM MQ version is `%s`.' % version)
