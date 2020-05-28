# -*- coding: utf-8 -*-

import sys
from copy import copy

# skrpyt wyszukuje hasla z indeksu w pliku z haslami slownika XVII w. i dodaje odpowiednia kolumne z informacja o tym
# czy haslo znaleziono czy nie
# hasla ze slownika XVII w. ktorych nie znaleziono w indeksie sa wypisywane do osobnego pliku
# gloscheck PLIK_Z_INDEKSEM PLIK_Z_HASLAMI_ZE_SLOWNIKA PLIK_WYNIKOWY PLIK_Z_HASLAMI_ZE_SLOWNIKA_KTORYCH_NIE_MA_W_INDEKSIE
# obsluga pliku z haslami ze slownika XVII w.:
# - jako haslo traktujemy: wszystko w 1 kolumnie, wszystko w 4 kolumnie i rozdzielone przecinkami hasla w 3 kolumnie
# - przy sprawdzaniu czy trzecia kolumna zawiera cos nie bedace haslami jest blad (oznaczony "VVV...V"), nalezy sie temu
#   przyjrzec
# - wielkosc liter jest ignorowana

def loadlist(path):
	#res = {}
	res = []
	fin = open(path)
	for line in fin:
		line = unicode(line.decode("utf-8"))
		els = line.split(u";")
		word = els[0][1:-1].lower()
		res.append(word)
		ok = False
		for el in els[2][1:-1].split(u","):
			wrd = el.lstrip().rstrip()
			                                          #VVVVVVVVVVVVVVVVVVVV
			if wrd != u"" and wrd.find(u"X") == -1 and wrd.find(u"in. zn.") and wrd != u"?" and wrd != u"bez cyt.":
				res.append(wrd.lower())
		tmp = els[3][1:-2].lower()
		if tmp != u"":
			res.append(tmp)
	fin.close()
	return (res)

def ison(word, llist):
	return word in llist

def main(argv):
	fin = open(argv[1])
	llist = loadlist(argv[2])
	all = copy(llist)
	fout = open(argv[3], "w")
	fout2 = open(argv[4], "w")
	for line in fin:
		if line == "\n":
			fout.write("\n")
			continue
		line = unicode(line.decode("utf-8"))
		els = line.split(u";")
		els[12] = els[12].lower()
		res = ison(els[12], llist)
		if res == False:
			fout.write((u"0;" + line).encode("utf-8"))
		else:
			ok = False
			while not ok:
				try:
					all.remove(els[12])
				except ValueError:
					ok = True
			fout.write((u"1;" + line).encode("utf-8"))
	for el in all:
		fout2.write((el + u"\n").encode("utf-8"))
	fin.close()
	fout.close()
	fout2.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

