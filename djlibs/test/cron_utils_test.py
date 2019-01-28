__author__ = 'Ishayahu'

import unittest
from cron_utils import *
__version__ = '0.0.1'

class MyTestCase(unittest.TestCase):
    def test_crontab_to_russian (self):
        self.assertEqual( crontab_to_russian(u'00\t09\t\t\t'),
                          u'\u0412 9 \u0447\u0430\u0441\u043e\u0432 0 \u043c\u0438\u043d\u0443\u0442 \u043a\u0430\u0436\u0434\u044b\u0439 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31] \u0434\u0435\u043d\u044c \u043c\u0435\u0441\u044f\u0446\u0430 \u0438\u043b\u0438 \u043a\u0430\u0436\u0434\u044b\u0439 [0, 1, 2, 3, 4, 5, 6] \u0434\u0435\u043d\u044c \u043d\u0435\u0434\u0435\u043b\u0438 \u0432 \u043c\u0435\u0441\u044f\u0446\u0430\u0445 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]'
                          )

if __name__ == '__main__':
    unittest.main()
