# -*- coding: utf-8 -*-

import sys

# skrypt poprawia podhasla w nastepujacy sposob:
# - usuwa "!" i "@" (bo nie powinny sie znalezc w podhaslach) - w takim przypadku dopisuje poprzednia wartosc
#   w komentarzu z numerem przebiegu w nawiasach
# - ustawia haslo glowne na ostatnie haslo glowne przed podhaslem (cos sie moglo po drodze rozjechac np
#   przy poprawianiu recznym)
# subcheck PLIK_WEJSCIOWY PLIK_WYNIKOWY NUMER_PRZEBIEGU

def main(argv):
	fin = open(argv[1])
	fout = open(argv[2], "w")
	passnum = int(argv[3])
	last = None
	for line in fin:
		if line == "\n":
			fout.write("\n")
			continue
		line = unicode(line.decode("utf-8"))
		els = line.split(u";")
		
		if (els[13] == els[14]):
			last = els[13]
		else:
			line = line.replace(els[13] + u";" + els[14], els[13] + u";" + last)
			ln = len(els[0]) + 1 + len(els[1])
			head = line[:ln]
			tail = line[ln:-1]
			app = u"\n"
			if head.find(u"!") != -1 or head.find(u"@") != -1:
				app = u"; " + els[1] + u" (" + unicode(passnum) + u")\n"
			head = head.replace(u"!", u"+")
			head = head.replace(u"+?", u"?")
			head = head.replace(u"@", u"")
			line = head + tail + app
		
		fout.write(line.encode("utf-8"))
	fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

