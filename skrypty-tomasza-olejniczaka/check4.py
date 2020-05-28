# -*- coding: utf-8 -*-

import sys

# skrypt sprawdza poprawnosc hasel (dozwolone znaki i kolejnosc alfabetczyna)
# check4 PLIK_WEJSCIOWY PLIK_WYNIKOWY
# skrypt ma wartosc archiwalna, jego udoskonalona wersja jest check5 i to ona powinna byc uzywana
# skrypt jest modyfikacja infochecka, reguly zmienily sie nastepujaco:
# - sprawdzana jest takze poprawnosc podhasel, ale jest tutaj pewien blad (patrz komentarz z TODO (1) ponizej)
# - "?" jest traktowany osobno od "+", "#", "-" i "!" - jezeli wystepowal w hasle w pliku wejsciowym to "+", "#", "-"
#   i "!" jest dodawane do "?"
#   UWAGA: "+?" oznaczamy w skrócie przez "?"
# - pojawienie sie "*", ".", "'" (poza koncem wyrazu po "p", "b", "w"), "-", " " (na koncu wyrazu) w sprawdzanym hasle
#   traktowane jest jako blad ("-")
# - (*) takie same problemy (z wyjatkiem " " na koncu wyrazu) w poprzednim hasle powoduja niemoznosc spradzenia kolejnosci
#   alfabetycznej ("#")
# - (**) wystapienie znaku spoza ponizszej tablicy ("P" oznacza "p": itd.) powoduje "-" lub "#" w zaleznosci od tego czy
#   problem pojawil sie w sprawdzanym hasle czy w poprzednim hasle - jezeli jest i tu i tu to "-" lub "#" jest wybierane
#   w zaleznosci od tego w ktorym zostal znaleziony pierwszy (to i ponizsza UWAGA powoduja ze czasami jest "#" tam gdzie
#   powinno byc "-" - trzeba to recznie sprawdzac)
# - UWAGA: jezeli wczesniej wystapil problem (*) to (**) nie jest juz sprawdzane
# - przecinki i nawiasy sa ignorowane
# - "@" jest ignorowana i przepisywana do wyniku
# - jezeli oznaczenie poprawnosci w pliku wejsciowym bylo rozne od "+" to zapisujemy je w komentarzu
# WAZNE: zobacz komentarz do uzycia ok w merge ponizej

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
		strange = "S"
	else:
		strange = ""
	if snd.find(u'*') != -1:
		return "BAD" + strange
	if snd.find(u'-') != -1:
		return "BAD" + strange
	if snd.find(u'.') != -1:
		return "BAD" + strange
	if snd[:-1].find(u'\'') != -1:
		return "BAD" + strange
	fst = fst.lower()
	snd = snd.lower()
	fst = fst.replace(u"@", u"")
	snd = snd.replace(u"@", u"")
	if snd[-1] == u' ':
		return "BAD" + strange
	i = len(fst) - 1
	j = len(snd) - 1
	try:
		if snd[-1] == u'\'':
			snd = snd[:-2] + soft(snd[-2])
			j -= 1
	except Exception:
		return "BAD" + strange
	if fst[-1] == u' ':
		return "IMP" + strange
	if fst.find(u'*') != -1:
		return "IMP" + strange
	if fst.find(u'-') != -1:
		return "IMP" + strange
	if fst.find(u'.') != -1:
		return "IMP" + strange
	if fst[:-1].find(u'\'') != -1:
		return "IMP" + strange
	try:
		if fst[-1] == u'\'':
			fst = fst[:-2] + soft(fst[-2])
			i -= 1
	except Exception:
		return "IMP" + strange
	fst = fst.replace(u'é', u'e')
	snd = snd.replace(u'é', u'e')
	while i >= 0 and j >= 0:
		while i >= 0 and fst[i] in [u',', u'(', u')', u'\'']: i -= 1
		while j >= 0 and snd[j] in [u',', u'(', u')', u'\'']: j -= 1
		#if snd == u"podwódca":
		#	print i, j, fst[i], snd[j]
		if i < 0 or j < 0:
			break
		try:
			if lt(fst[i], snd[j]):
				return "OK" + strange
			elif lt(snd[j], fst[i]):
				#print fst, snd, i, j
				#exit()
				return "NOT" + strange
		except ValueError:
			return "BAD" + strange
		except Exception:
			return "IMP" + strange
		else:
			i -= 1
			j -= 1
	if len(fst) <= len(snd):
		return "OK" + strange
	else:
		#print fst, snd
		#exit()
		return "NOT" + strange

def merge(line, res, ok=True):
	#print line[0] == "u"
	if not ok:
		line = line[1:]
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
		elif res == "BADS":
			new = u"-?"
		elif res == "OKS":
			new = u"?"
		elif res == "NOTS":
			new = u"!?"
		elif res == "IMP":
			new = u"#"
		elif res == "IMPS":
			new = u"#?"
	elif old.replace(u"@", u"") == u"-":
		if res == "OK":
			new = u"+"
		elif res == "NOT":
			new = u"!"
		elif res == "BAD":
			new = u"-"
		elif res == "BADS":
			new = u"-?"
		elif res == "OKS":
			new = u"?"
		elif res == "NOTS":
			new = u"!?"
		elif res == "IMP":
			new = u"#"
		elif res == "IMPS":
			new = u"#?"
	elif old.replace(u"@", u"") == u"!":
		if res == "OK":
			new = u"+"
		elif res == "NOT":
			new = u"!"
		elif res == "BAD":
			new = u"-"
		elif res == "BADS":
			new = u"-?"
		elif res == "OKS":
			new = u"?"
		elif res == "NOTS":
			new = u"!?"
		elif res == "IMP":
			new = u"#"
		elif res == "IMPS":
			new = u"#?"
	elif old.replace(u"@", u"") == u"?":
		if res == "OK":
			new = u"?"
		elif res == "NOT":
			new = u"!?"
		elif res == "BAD":
			new = u"-?"
		elif res == "BADS":
			new = u"-?"
		elif res == "OKS":
			new = u"?"
		elif res == "NOTS":
			new = u"!?"
		elif res == "IMP":
			new = u"#?"
		elif res == "IMPS":
			new = u"#?"
	if new == u"":
		print res, old, line
		assert(False)
	app = u""
	if old != u"+":
		app = u"; " + old
	return u"" + head + u"" + new + u"" + at + u"" + tail[i:-1] + u"" + app + u"\n"

def main(argv):
	fin = open(argv[1])
	fout = open(argv[2], "w")
	prev = None
	for line in fin:
		if line == "\n":
			fout.write(u"\n".encode("utf-8"))
			continue
		line = unicode(line.decode("utf-8"))
		els = line.split(u";")
		if els[13] != els[14]:
			res = ok(prev, els[13])
			if res in ["NOTS", "OKS", "BADS", "BAD"]: # TODO: (1) dziala to w ten sposob, ze ignorujemy informacje o kolejnosci
			    # alfabetycznej - interesuje nas tylko "-" i "?"
			    # sa tu dwa bledy:
			    # - nie sprawdzamy czy res == IMPS ("#?"), a zatem w takim przypadku zgubimy "?"
			    # - jezeli res == NOTS ("!?"), to wypiszemy wykrzyknik w podhasle (czego nie powinnismy robic) - ale skrypt
			    #   subcheck pozwala sie nam pozbyc tego problemu
				line = merge(line, res)
			else:
				line = merge(line, "OK")
			fout.write(line.encode("utf-8"))
		else:
			if prev == None:
				res = ok(u"napisktoregonapewnoniema", els[13]) # TODO: (2) przypadek szczegolny - pierwsze haslo, prev == None,
  		    # ten sam blad co powyzej:
  		    # - jezeli res == NOTS ("!?"), to wypiszemy wykrzyknik ktorego nie powinno byc (ale to sie nie dzieje akurat
  		    #   w tym przypadku)
				  # parametr opcjonalny ok=False do merge pozwalal zignorowac jakies smieci na poczatku pliku
				if res in ["NOTS", "OKS", "BAD", "BADS"]:
					line = merge(line, res, ok=False)
				else:
					line = merge(line, "OK", ok=False)
			else:
				res = ok(prev, els[13])
				line = merge(line, res)
			prev = els[13]
			fout.write(line.encode("utf-8"))
	fin.close()
	fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

