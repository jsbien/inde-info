# -*- coding: utf-8 -*-

import sys

# skrypt sprawdza poprawnosc hasel (dozwolone znaki i kolejnosc alfabetczyna)
# check4 PLIK_WEJSCIOWY PLIK_WYNIKOWY NUMER_PRZEBIEGU
# poprawiona wersja check4
# zmiany:
# - hasla z "?" pomijamy
# - hasla zawierajace myslnik pomijamy (w wersjach uzywanych do stworzenia indeksu byl blad taki, ze jezeli byl i
#   myslnik i gwiazdka to poprawnosc byla sprawdzana i haslo dostawali "-", ale takich hasel (myslnik i gwiazdka) chyba
#   nie ma)
# - warunki na "#" sa sprawdzane dopiero wtedy gdy sprawdzono wszystkie warunki na "-"
# - nie ma specjalnego zachowania merge na poczatku pliku w celu zignorowania smieci
# - "@!" jest zamieniana na "!@"
# - dawna wartosc kolumny z poprawnoscia jest zapisywana w komentarzu na koncu wiersza (z numerem przebiegu w nawiasie)
#   wtedy gdy cos w wierszu zmienilo sie
# - poprawiono bledy z NOTS i IMPS w TODO 1 i 2 z check4
# UWAGA: problemem tego skryptu jest to, ze generuje ciagle te same "#" (tzn. jezeli sprawdzilismy rrcznie ze dany "#"
# jest OK i wstawilismy tam "+" to w nastepnym przebiegu skrypt z powrotem wpisze "#"), rozwiazywalem to w ten sposob ze
# przegladalem plik kdiffem i poprawialem te "#" recznie przed udostepnieniem pliku ale dobrze by bylo rozwiazac to lepiej

a = [u' ', u'a', u'ą', u'b', u'B', u'c', u'ć', u'd', u'e', u'ę', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'ł', u'm', u'n', u'ń',
		u'o', u'ó', u'p', u'P', u'r', u's', u'ś', u't', u'u', u'v', u'w', u'W', u'x', u'y', u'z', u'ź', u'ż']

def lt(fst, snd):
	global a
	try:
		i = a.index(fst)
	except ValueError:
		raise Exception()
	j = a.index(snd)
	return i < j

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
	strange = snd.find(u'(') != -1 or snd.find(u')') != -1
	if strange:
		return "PASS"
	if snd.find(u'-') != -1:
		return "PASS"
	if snd.find(u'*') != -1:
		return "BAD"
	if snd.find(u'.') != -1:
		return "BAD"
	if snd[:-1].find(u'\'') != -1:
		return "BAD"
	fst = fst.lower()
	snd = snd.lower()
	fst = fst.replace(u"@", u"")
	snd = snd.replace(u"@", u"")
	if snd[-1] == u' ':
		return "BAD"
	i = len(fst) - 1
	j = len(snd) - 1
	try:
		if snd[-1] == u'\'':
			snd = snd[:-2] + soft(snd[-2])
			j -= 1
	except Exception:
		return "BAD"
	imp = False
	if fst[-1] == u' ':
		imp = True
	if fst.find(u'*') != -1:
		imp = True
	if fst.find(u'-') != -1:
		imp = True
	if fst.find(u'.') != -1:
		imp = True
	if fst[:-1].find(u'\'') != -1:
		imp = True
	try:
		if fst[-1] == u'\'':
			fst = fst[:-2] + soft(fst[-2])
			i -= 1
	except Exception:
		imp = True
	fst = fst.replace(u'é', u'e')
	snd = snd.replace(u'é', u'e')
	ok = False
	notok = False
	while i >= 0 and j >= 0:
		while i >= 0 and fst[i] in [u',', u'(', u')', u'\'']: i -= 1
		while j >= 0 and snd[j] in [u',', u'(', u')', u'\'']: j -= 1
		#if snd == u"aloesowy":
		#	print i, j, fst[i], snd[j]
		if i < 0 or j < 0:
			break
		try:
			if lt(fst[i], snd[j]):
				if not notok:
					#if snd == u"aloesowy":
					#	print "::", i, j, fst[i], snd[j]
					ok = True
			elif lt(snd[j], fst[i]):
				#print fst, snd, i, j
				#exit()
				if not ok:
					#if snd == u"aloesowy":
					#	print "::", i, j, fst[i], snd[j]
					notok = True
		except ValueError:
			return "BAD"
		except Exception:
			imp = True
		i -= 1
		j -= 1
	if imp:
		return "IMP"
	if ok:
		return "OK"
	if notok:
		return "NOT"
	if len(fst) <= len(snd):
		return "OK"
	else:
		#print fst, snd
		#exit()
		return "NOT"

def merge(line, res, ok=True):
	global passnum
	#print line[0] == "u"
#	if not ok:
#		line = line[1:]
	#print "[" + line[0] + "]"
	head = line[:2]
	#assert(head == line[:2])
	#print line[:1], line[:2], line[:3], line[:4], head
	#assert(len(head) == 2)
	#print "[" + head + "]" + line
	assert(head[1] == u';')
	tail = line[2:]
	i = tail.find(";")
	old = tail[:i]
	at = u""
	if old.find(u"@") != -1:
		at = u"@"
	new = u""
	if old.replace(u"@", u"") == u"+":
		if res == "OK":
			new = u"+"
		elif res == "NOT":
			new = u"!"
		elif res == "BAD":
			new = u"-"
		elif res == "IMP":
			new = u"#"
	elif old.replace(u"@", u"") == u"-":
		if res == "OK":
			new = u"+"
		elif res == "NOT":
			new = u"!"
		elif res == "BAD":
			new = u"-"
		elif res == "IMP":
			new = u"#"
	elif old.replace(u"@", u"") == u"!":
		if res == "OK":
			new = u"+"
			#if line.find(u"aloesowy") != -1:
			#	print new
		elif res == "NOT":
			new = u"!"
		elif res == "BAD":
			new = u"-"
		elif res == "IMP":
			new = u"#"
	elif old.replace(u"@", u"") == u"?":
		if res == "OK":
			new = u"?"
		elif res == "NOT":
			new = u"!?"
		elif res == "BAD":
			new = u"-?"
		elif res == "IMP":
			new = u"#?"
	if new == u"":
		print res, old, line
		assert(False)
	#app = u""
	#if old.replace(u"@", u"") != u"+":
	app = u"; " + old
	#if (u"" + line.split(u";")[-1][:-1].replace(u"@!", u"!@") == app) and (line.replace(u"@!", u"!@") == head + new + at + tail[i:]):
	if line == head + new + at + tail[i:]:
		#if new != old.replace(u"@", u""):
		#	print new, old, line
		return line
	else:
		#if line.find(u"wymaślnica") != -1:
		#	print u"" + line.split(u";")[-1][:-1].replace(u"@!", u"!@"), app
		#	print line.replace(u"@!", u"!@"), head + new + at + tail[i:]
		#	exit()
		if app != u"":
			app += u" (" + unicode(passnum) + u")";
		#if app != u"":
		#	print u"[;" + line.split(u";")[-1][:-1] + u"]"
		#	print u"[" + app + u"]"
		#	print u"[" + line + u"]"
		#	print u"[" + head + u"" + new + u"" + at + u"" + tail[i:-1] + u"]"
		#	exit()
		return u"" + head + u"" + new + u"" + at + u"" + tail[i:-1] + u"" + app + u"\n"

passnum = 0

def main(argv):
	global passnum
	fin = open(argv[1])
	fout = open(argv[2], "w")
	passnum = int(argv[3])
	prev = None
	for line in fin:
		if line == "\n":
			fout.write(u"\n".encode("utf-8"))
			continue
		line = unicode(line.decode("utf-8"))
		#line = line.replace(u"@!", u"!@")
		els = line.split(u";")
		if els[13] != els[14]:
			#if els[3] == u"1" and els[4] == u"1":
			#	print line
			res = ok(prev, els[13])
			#if els[13] == u"wnątrz":
			#	print res, line
			if res == "PASS":
				#line = line[:-1] + u";&\n"
				pass
			elif res == "BAD":
				line = merge(line, "BAD")
			else:
				line = merge(line, "OK")
			fout.write(line.encode("utf-8"))
		else:
			if prev == None:
				res = ok(u"napisktoregonapewnoniema", els[13])
				if res == "PASS":
					pass
				elif res == "BAD":
					line = merge(line, "BAD", ok=False)
				else:
					line = merge(line, "OK", ok=False)
			else:
				res = ok(prev, els[13])
				if res != "PASS":
					line = merge(line, res)
			prev = els[13]
			fout.write(line.encode("utf-8"))
	fin.close()
	fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

