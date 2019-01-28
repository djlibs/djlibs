__author__ = 'Ishayahu'

import unittest
from text_utils import htmlize
__version__ = '0.0.1'

class MyTestCase(unittest.TestCase):
    def test_bold (self):
        self.assertEqual( htmlize("*bold*"), "<b>bold</b>")

    def test_italic (self):
        self.assertEqual( htmlize("**bold**"), "<i>bold</i>")

    def test_link_http (self):
        self.assertEqual( htmlize("http://site.com"),
                          '<a href="http://site.com">'
                          'http://site.com</a>')

    def test_link_https (self):
        self.assertEqual( htmlize("https://site.com"),
                          '<a href="https://site.com">'
                          'https://site.com</a>')

    def test_basic_1(self):
        self.assertEqual( htmlize("*bold* **italic**"
                                  " http://site.com"
                                  " https://site.com"
                                  " https://site.com/page.php"),
                          u'<b>bold</b>'
                          u' <i>italic</i>'
                          u' <a href="http://site.com">'
                          u'http://site.com</a>'
                          u' <a href="https://site.com">'
                          u'https://site.com</a>'
                          u' <a href="https://site.com/page.php">'
                          u'https://site.com/page.php</a>')

    def test_basic_2(self):
        a=r'*bold* **italic** < http://site.com \\ https://site.com ' \
          r'&>\* **sdfadf** *dfs* https://site.com/page.php ' \
          r'https://site.com/page.php&got=cot'
        b = r'<b>bold</b> <i>italic</i> &lt ' \
            r'<a href="http://site.com">http://site.com</a> \ ' \
            r'<a href="https://site.com">https://site.com</a>' \
            r' &amp&gt* <i>sdfadf</i> <b>dfs</b> ' \
            r'<a href="https://site.com/page.php">' \
            r'https://site.com/page.php</a> ' \
            r'<a href="https://site.com/page.php&got=cot">' \
            r'https://site.com/page.php&got=cot</a>'
        self.assertEqual(htmlize(a),b)

    def test_winpath(self):
        a=r'C:\\Documents and Settings\\mira.MEOC0>' \
          r'dir \\\\docsrv\\secretar-test'
        self.assertEqual(htmlize(a),
                         ur'C:\Documents and Settings\mira.MEOC0&gt'
                         ur'dir \\docsrv\secretar-test')
    def test_table(self):
        self.maxDiff = None
        a="""||h1||h2||
            ||r1||r2||

            neflsflk

            ||h1||h2||h1||h2||
            ||r1||r2||r1||r2||"""
        self.assertEqual(htmlize(a),
                         u'<table border=1>'
                         u'<tr><td>h1</td><td>h2</td></tr>'
                         u'<tr><td>r1</td><td>r2</td></tr>'
                         u'</table>'
                         u'neflsflk'
                         u'<table border=1>'
                         u'<tr><td>h1</td><td>h2</td><td>h1</td>'
                         u'<td>h2</td></tr>'
                         u'<tr><td>r1</td><td>r2</td><td>r1</td>'
                         u'<td>r2</td></tr>'
                         u'</table>')

    def test_abzatz(self):
        a="""Absatz1

        Abzats2

        Abz3
        Abz3"""

        self.assertEqual(htmlize(a),
                         u'Absatz1<p>Abzats2<p>Abz3 Abz3')

    def test_lists(self):
        a="""
        Title of list

        +     1
        + 2
        + 3

        Title of two lists

        + 1
        + 1
        - 2
        - 2

        End of lists
        """

        self.assertEqual(htmlize(a),
                u'Title of list<p><ol><li>1</li><li>2</li><li>3</li></ol>Title of two lists<p><ol><li>1</li><li>1</li><ul><li>2</li><li>2</li></ul></ol>End of lists'
                         )

    def test_lists_2(self):
        a="""+ ghbdtn
+ geibcnsq
- ,tutvjn

rnj

+ y.[fk
- ndjq
+ vbksq
- hjn
9"""

        self.assertEqual(htmlize(a),
                u'<ol><li>ghbdtn</li><li>geibcnsq</li><ul><li>,tutvjn</li></ul></ol>rnj<p><ol><li>y.[fk</li><ul><li>ndjq</li><ol><li>vbksq</li><ul><li>hjn</li></ul></ol></ul></ol>9'
                         )

    def test_lists_3(self):
        a="""+ git+pycharm
+ razvyorty`vanie na servere
+ tar-progressbar
+ BD
+ Bakup i proverka vsekh fai`lov cherez md5
+ bakup vsekh nuzhny`kh fai`lov dlia BD
+ instruktcii` po razvyorty`vaniiu
+ pereimenovy`vat` proverenny`e kopii
+ Viki
+ Timex
+ AD replikatciia
+ naladit` testirovanie na moyom PK
+ bakup na udalyonny`i` server
+ udaliat` bakupy` starshe 15 dnei`
+ nastroit` plan

- bakupit` udalyonno bazu i proveriat` vlozhiv v matryoshku
- AD bakup
- Sistema zaiavok
- Serverov?
- avtoobnovlenie
- zapusk s tai`mautom"""

        self.assertEqual(htmlize(a),
                u'<ol><li>git+pycharm</li><li>razvyorty`vanie na servere</li><li>tar-progressbar</li><li>BD</li><li>Bakup i proverka vsekh fai`lov cherez md5</li><li>bakup vsekh nuzhny`kh fai`lov dlia BD</li><li>instruktcii` po razvyorty`vaniiu</li><li>pereimenovy`vat` proverenny`e kopii</li><li>Viki</li><li>Timex</li><li>AD replikatciia</li><li>naladit` testirovanie na moyom PK</li><li>bakup na udalyonny`i` server</li><li>udaliat` bakupy` starshe 15 dnei`</li><li>nastroit` plan</li></ol><ul><li>bakupit` udalyonno bazu i proveriat` vlozhiv v matryoshku</li><li>AD bakup</li><li>Sistema zaiavok</li><li>Serverov?</li><li>avtoobnovlenie</li><li>zapusk s tai`mautom</li></ul>'
                         )



    def test_escape(self):
        a=r"""\*bold\* \\backslash\\ {yesterday}"""

        self.assertEqual(htmlize(a),
                         r'*bold* \backslash\ {yesterday}')


    def test_error_1(self):
        a=r"""5651651
            http://172.22.0.138:8080/task/one_time/479/

            *sdfs*

            ||1||1||
            ||2||2||"""

        self.assertEqual(htmlize(a),
                         u'5651651 '
                         u'<a href="http://172.22.0.138:8080/'
                         u'task/one_time/479/">http://172.22.0'
                         u'.138:8080/task/one_time/479/</a>'
                         u'<p><b>sdfs</b>'
                         u'<table border=1>'
                         u'<tr><td>1</td><td>1</td></tr>'
                         u'<tr><td>2</td><td>2</td></tr>'
                         u'</table>'
                         )

if __name__ == '__main__':
    unittest.main()
