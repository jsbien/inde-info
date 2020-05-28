#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Autor: Jan Chęć (277635)
# Licencja: Creative Commons 3.0 CC-BY (uznanie autorstwa)
# Wersja: 1.1

import unittest, sys

from downloader import downloadDescription
from xelatexPdf import generateXelatex, printToFile, makePDF

XETEX_OUTPUT_FILE = "slownik.tex"
PDF_OUTPUT_FILE = "slownik.pdf"


def UI():
  """
  Main function with UI.
  """
  # Printing initial usage info
  print "Wpisz słowa, jakie chcesz, aby zostały ściągnięte z wikisources i pojawiły się w słowniku."
  print "Zakończ wpisywanie poprzez Ctrl-D."
  print "Rada: zawsze możesz zapisać hasła w pliku i przekierować go do programu poprzez %s < plikZHasłami\n" % (sys.argv[0])

  # Locale for unicode purposes
  import locale, urllib2
  locale.setlocale(locale.LC_ALL, "")

  # Getting words from input, word/sentence per line ("words" can be sentences
  # in case of being parts of introduction)
  words = []
  try:
    while True:
      word = raw_input("")
      if len(word) > 0:
        word = unicode(word, "UTF-8")
        word = unicode.upper(word)
        word = word.replace(' ', '_')
        word = word.replace('.', '')
        words += [word]
  except EOFError:
    pass

  print "\nOtrzymano hasła. Ściąganie istniejących z Wikiźródeł..."

  # Sorting words (removed, because of the existence of introduction)
  # words.sort(cmp=locale.strcoll)

  # Generating dictionary
  dictionary = []
  for word in words:
    try:
      dictionary += [(word, downloadDescription(word))]
      sys.stdout.write(".")
      sys.stdout.flush()
    except urllib2.HTTPError:
      print u"Hasło: " + word + u" nie istnieje w SJP w Wikiźródłach."

  print "\nGenerowanie pliku " + XETEX_OUTPUT_FILE + "..."
  printToFile(generateXelatex(dictionary), XETEX_OUTPUT_FILE)

  if len(sys.argv) > 1 and sys.argv[1] == "--tex-only":
    print "\n Użyto opcji generowania jedynie pliku .tex - kończenie programu."
    return

  print "\nTworzenie pliku " + PDF_OUTPUT_FILE + "..."
  out = makePDF(XETEX_OUTPUT_FILE)
  if out == 0:
    out = makePDF(XETEX_OUTPUT_FILE) # Repeating for Table of Contents
  if out == 0:
    print "\nZakończono działanie sukcesem. Wygenerowano " + PDF_OUTPUT_FILE
  else:
    print "\nZakończono działanie z błędem. Sprawdź instalację XeLaTeX'a i uzupełnij o brakujące pakiety."

UI()

# Unittests
class TestDownloadingPages(unittest.TestCase):
  def test_good_pages(self):
    page = downloadDescription(u"adam")
    desc = u'<span><span class="PageNumber" id="Strona_93" style="color:#666666; display:none; margin:0px; padding:0px;">[<b><a href="/wiki/Strona:PL_Linde-Slownik_Jezyka_Polskiego_T.1_Cz.1_A-F_093.jpg" title="Strona:PL Linde-Slownik Jezyka Polskiego T.1 Cz.1 A-F 093.jpg">93</a></b>]</span></span>ADAM, JADAM, a. m. (<i>Arab.</i> adem = człowiek) pierwszy człowiek, Adam; <i>Sorab, inf.</i> Hadam, Hodam; <i>Ross.</i> праотéцъ, прародитель. - Zakon S. Adama. <i>Teat.</i> 7 c.. 7. = stan małżeński, der Ehestand, (<i>oppos.</i> bezżeństwo.- <i>Theol.</i> stary Adam = grzech pierworodny, grzechy stare, der alte Adam, Erbsünde, alte Sünden. Złóżcie tego Adama starego. <i>W. Post. w.</i> 9. Trzeba zwłóczyć starego Jadama odzienie. <i>Biał. Pst.</i> 14. Ostatni Adam, nowy Adam = Chrystus Jezus. <i>Kuczb. Kat.</i> 85. der neue Adam, Jesus. § <i>tr.</i> od Adama, od stworzenia świata, von Adam her, von Erschaffung der Welt. Wchodzi z rzeczą swą w dziwne labirynty, oracyą wszystko od Adama ią począwszy, rozwlecze. <i>Gór. Dw.</i> 386. 2., Adam, u nas imię zwyczayne, Taufname Adam. J. O. X. Generał <i>Adam Czartoryski</i>. X. Biskup <i>Adam Naruszewicz.</i> - <i>Alluzya:</i> Znam to do siebie, móy zacny Korwinie (Kossakowski), żem od Adama wziął imię i ciało. <i>Zab.</i> 7, 325. <i>Nar.</i> - <i>Lusus verborum:</i> Byś na mnie rzekł o Tomasz, abo na się Jadam. <i>Jag. Gr. B.</i> 8. (oto masz, naści! - ia dam). <i>Prov.</i> Na święty Adam. <i>Rys. Ad.</i> 42. (= na S. Nigdy, na S. Bóg wie, na zielone Swięta) auf den Nimmerstag. § <i>Anat.</i> Jabłko Adam, pagórek przy gardle, grdycze, <i>pomum Adami</i>. <i>Kirch. Anat.</i> 44. <i>Boh.</i> Adamowo gablko; <i>Vind.</i> Adamovu jabuku, Adamska jabuka; <i>Ross.</i> кадыкъ, der Adamsapfel an der Kehle (der Kröbs, der Gröbschel). <i>Deriv.</i> <a href="/wiki/SJP:ADAMEK" title="SJP:ADAMEK">Adamek</a>, <a href="/wiki/SJP:ADAS" title="SJP:ADAS">Adaś</a>, <a href="/wiki/SJP:ADAMITA" title="SJP:ADAMITA">Adamita</a>, <a href="/wiki/SJP:ADAMOWY" title="SJP:ADAMOWY">Adamowy</a>.'
    #self.assertEquals(page, desc)

  def test_bad_pages(self):
    import urllib2
    self.assertRaises(urllib2.HTTPError, downloadDescription, u"rzyć")

# Running unittests
if __name__ == '__main__s':
  import doctest
  doctest.testmod()
  unittest.main()
