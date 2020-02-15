# More examples are at https://dsuch.github.io/pymqi/examples.html
# or in code/examples in the source distribution.

import logging

import rpm

logging.basicConfig(level=logging.INFO)

package_name = 'MQSeriesClient'

ts = rpm.TransactionSet()
mi = ts.dbMatch('name', package_name)

if not mi.count():
    logging.info('Did not find package `%s` in RPM database.' % package_name)
else:
    for header in mi:
        version = header['version']
        msg = 'Found package `%s`, version `%s`.' % (package_name, version)
        logging.info(msg)
