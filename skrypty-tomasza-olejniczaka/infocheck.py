# -*- coding: utf-8 -*-

import sys
from pagex import okk

# skrypt sprawdza zgodnosc z pagina i jeszcze raz poprawnosc hasel (dozwolone znaki i kolejnosc alfabetczyna)
# infocheck PLIK_WEJSCIOWY PLIK_WYJSCIOWY
# uwagi:
# - informacje o niezgodnosci z pagina sa umieszczane w komentarzach i poprzedzone znakiem %
# - sprawdzana jest poprawnosc hasel glownych, przyjeto przy tym nastepujace zalozenia
#   - UWAGA:
#     - niedozwolone znaki sa oznaczane jako blad w kolejnosc alfabetycznej ("!" a nie "-")!!!
#     - dlatego musi to byc potem zweryfikowane recznie!!!
#     - "!" moze nadpisac "?" i "-"!!!
#   - wszyskie przecinki, nawiasy, kropki i apostrofy (poza tymi na koncu po p, b i w) sa ignorowane
#   - wielkosc liter jest ignorowana
#   - "p'", "w'" i "b'" wystepuja po "p", "w" i "b"
#   - "é" traktujemy jak "e"
#   - " " jest na poczatku porzadku alfabetycznego
#   - "*" lub "-" w sprawdzanym hasle lub hasle je poprzedzajacym powoduje stwierdzenie niepoprawnosci hasla

a = [u' ', u'a', u'ą', u'b', u'B', u'c', u'ć', u'd', u'e', u'ę', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'ł', u'm', u'n', u'ń',
		u'o', u'ó', u'p', u'P', u'r', u's', u'ś', u't', u'u', u'v', u'w', u'W', u'x', u'y', u'z', u'ź', u'ż']

def lt(fst, snd):
	global a
	try:
		i = a.index(fst)
		j = a.index(snd)
		return i < j
	except ValueError:
		print fst, snd
		assert(False)

def soft(char):
	if char == u'p':
		return u'P'
	elif char == u'b':
		return u'B'
	elif char == u'w':
		return u'W'
	else:
		raise Exception()

def ok(fst, snd):
	if fst.find(u'*') != -1 or snd.find(u'*') != -1:
		return False
	if fst.find(u'-') != -1 or snd.find(u'-') != -1:
		return False
	fst = fst.lower()
	snd = snd.lower()
	if snd[-1] == u' ':
		return False
	i = len(fst) - 1
	j = len(snd) - 1
	try:
		if fst[-1] == u'\'':
			fst = fst[:-2] + soft(fst[-2])
			i -= 1
		if snd[-1] == u'\'':
			snd = snd[:-2] + soft(snd[-2])
			j -= 1
	except Exception:
		return False
	fst = fst.replace(u'é', u'e')
	snd = snd.replace(u'é', u'e')
	while i >= 0 and j >= 0:
		while i >= 0 and fst[i] in [u',', u'(', u')', u'.', u'\'']: i -= 1
		while j >= 0 and snd[j] in [u',', u'(', u')', u'.', u'\'']: j -= 1
		if i < 0 or j < 0:
			break
		if lt(fst[i], snd[j]):
			return True
		elif lt(snd[j], fst[i]):
			#print fst, snd, i, j
			#exit()
			return False
		else:
			i -= 1
			j -= 1
	if len(fst) <= len(snd):
		return True
	else:
		#print fst, snd
		#exit()
		return False

def loadPagination(path):
	res = [None, None, None, None, None, None, None, None, None]
	file = open(path)
	pop = None
	for line in file:
		els = line.split(",")
		els[1] = unicode(els[1][1:].decode("utf-8"))
		if pop != None and (not okk(pop, u"-" + els[1])):
			print els[1], pop
			assert(False)
		els[2] = unicode(els[2][1:-1].decode("utf-8"))
		res.append((els[1], els[2]))
		pop = u"-" + els[2]
	return res

def main(argv):
	fin = open(argv[1])
	pagination = loadPagination(argv[2])
	fout = open(argv[3], "w")
	prev = None
	lastpage = 8
	buffer = []
	for line in fin:
		if line == "\n":
			buffer.append(u"\n")
			continue
		line = unicode(line.decode("utf-8"))[:-1]
		els = line.split(u";")
		if els[12] != els[13]:
			buffer.append(line)
		else:
			#print line.encode("utf-8")
			#if els[12] == u"esz":
			#	print prev, ok(prev, els[12])
			if prev == None or ok(prev, els[12]):
				buffer.append(line)
				prev = els[12]
			else:
				buffer.append(u'!' + line[1:])
		if int(els[1]) != lastpage:
			lastpage = int(els[1])
			#print lastpage, len(pagination)
			assert(els[12] == els[13])
			if not els[12].endswith(pagination[lastpage][0]):
				buffer.append(u";% -" + pagination[lastpage][0] + u", -" + pagination[lastpage][1] + u"\n")
			else:
				buffer.append(u"\n")
			i = len(buffer) - 3
			while i >= 0 and buffer[i] == u"\n":
				i -= 1
			if i >= 0:
				els = buffer[i].split(u";")
				if not els[13].endswith(pagination[int(els[1])][1]):
					buffer[i] += u";% -" + pagination[int(els[1])][0] + u", -" + pagination[int(els[1])][1] + u"\n"
			if i > 0 and els[12] != els[13]:
				while i >= 0 and (buffer[i] == u"\n" or els[12] != els[13]):
					i -= 1
					if buffer[i] != u"\n":
						els = buffer[i].split(u";")
				if i >= 0:
					if not els[12].endswith(pagination[int(els[1])][1]):
						buffer[i] += u";% -" + pagination[int(els[1])][0] + u", -" + pagination[int(els[1])][1]
			for el in buffer:
				fout.write(el.encode("utf-8"))
			buffer = []
		else:
			buffer.append(u"\n")
	if len(buffer) > 0:
		for el in buffer:
			fout.write(el.encode("utf-8"))
	fin.close()
	fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

