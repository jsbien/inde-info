# -*- coding: utf-8 -*-
import sys
from hocr_parser import extract, get_supergloss

# TODO: obsluga i...
# TODO: obsluga zaznaczania miejsca dzielenia wyrazow
# TODO: obsluga d vs. a (chyba jest)

# skrypt tworzy liste indeksu z plikow w postaci kolumnowej ktore byly poprawiane recznie i wykorzystuje hocr
# z ktorego te pliki byly wygenerowane do znalezienia podhasel
# uwaga: skrypt zostal stworzony do obslugi konkretnego pliki hocr w ktorym byl problem brakujacej 350 strony
# bierze on jednak jako dodatkowy parametr plik hocr z brakujaca 350 strona (poniewaz brak jej jednak w pliku
# w postaci kolumnowej jest on ignorowany)
# txt2info PLIK_W_POSTACI_KOLUMNOWEJ PLIK_WYNIKOWY PLIK_HOCR PLIK_HOCR_Z_BRAKUJACA_STRONA_350
# uwagi:
# - w formacie brak kolumny z miejscem podzialu linii
# - przy ad na poczatku jest zalozenie ze po ad jest tylko jeden numer
# - przy ad na koncu moze byc wiele numerow
# - pojawienie sie nawiasow wewnatrz hasla ("(w) domu" a nie "(haslo)") powoduje wypisanie "?"
# - program akceptuje na koncu wyrazow ` i ', natomiast ’ tylko po p (' moze byc ogolnie po p, w i b, a w pozniejszych
#   wersjach listy rozne rodzaje apostrofow zmieniono na '
# wykorzystywany skrypt hocr_parser sluzy do obslugi wykorzystywanego przez txt2info pliku hocr

class Page:

	def __init__(self, no):
		self.cols = [[], [], [], []]
		self.no = no

class Gloss:

	def __init__(self, id, specid, content, page, coln, supergloss):
		self.id = id # ...[14]
		self.supergloss = supergloss
		self.page = page
		self.coln = coln
		self.secid = None # ....[14,15] przeniesienie wyrazu
		self.specid = specid # ...[14,15] klamerka
		self.secpage = None
		self.seccoln = None
		self.ad = False
		self.paren = False
		self.addig = None
		self.excl = False
		self.digits = []
		self.see = False
		self.adafter = False
		self.star = False
		self.content = content
		while content[-1] == " ":
			content = content[:-1]
		while content[0] == " ":
			content = content[1:]
		if len(content) > 2:
			if content[:1] == "*":
				self.star = True
				content = content[1:]
				self.content = content				
				#(self.ok, self.parin, self.spanum) = iscorrect(self.content)
				#return
		if len(content) > 3:
			if content[-3:] == "(!)":
				self.excl = True
				if content[-4] == ' ':
					self.content = content[:-4]
				else:
					self.content = content[:-3]
				(self.ok, self.parin, self.spanum) = iscorrect(self.content)
				return
		(newContent, digits, one) = extractDigits(content)
		#print newContent, digits
		if digits != None:
			self.digits = digits
			if len(newContent) > 3:
				if newContent[-3:] == " ad":
					self.ad = True
					self.adafter = True
					self.content = newContent[:-3]
				elif newContent[:5] == "zob. ":
					self.see = True
					self.content = newContent[5:]
				else:
					#if one:
					self.content = newContent
					#else:
					#	(self.ok, self.parin, self.spanum) = iscorrect(self.content)
					#	self.digits = []
					#	self.ok = False
					#	return
			else:
				self.content = newContent
			(self.ok, self.parin, self.spanum) = iscorrect(self.content)
			return
		if len(content) > 5:
			if content[:5] == "zob. ":
				self.see = True
				self.content = content[5:]
				(self.ok, self.parin, self.spanum) = iscorrect(self.content)
				return
		if len(content) > 2:
			if content[0] == '(' and content[-1] == ')':
				self.paren = True
				self.content = content[1:-1]
				(self.ok, self.parin, self.spanum) = iscorrect(self.content)
				return
		if len(content) > 5:
			if content[:3] == "ad " and content[4] == ' ':
				if str.isdigit(content[3]) and int(content[3]) < 6 and int(content[3]) > 0:
					self.ad = True
					self.addig = int(content[3])
					self.content = content[5:]
					(self.ok, self.parin, self.spanum) = iscorrect(self.content)
					return
		(self.ok, self.parin, self.spanum) = iscorrect(self.content)
	
	def append(self, id, content, pageno, coln, sgloss=None):
		if content[0] != "+":
			print "Fatal error: malformed word break"
			exit()
		content = content[1:]
		while content[0] == ' ':
			content = content[1:]
		#print content, self.content
		#assert(content[0] == "+")
		self.content += content
		if self.content[0] == '(' and self.content[-1] == ')':
			self.paren = True
			self.content = self.content[1:-1]
		(self.ok, self.parin, self.spanum) = iscorrect(self.content)
		self.secid = id
		if pageno != self.page:
			self.secpage = pageno
		if coln != self.coln:
			self.seccoln = coln
		if sgloss != None:
			self.superglosss = sgloss
		return self

	def str(self, ord):
		if self.digits == []:
			digits = "-"
		else:
			digits = []
			for d in self.digits:
				digits.append(str(d))
		#print self.content, digits
		res = ""
		for d in digits:
			#print self.content
			if self.ok == None:
				res += "?;"
			elif self.ok:
				res += "+;"
			else:
				res += "-;"
			res += str(self.page + 8) + ";" + str(self.coln) + ";" + str(ord)
			if self.star:
				res += ";*"
			else:
				res += ";-"
			if self.see:
				res += ";z"
			elif self.ad:
				if self.adafter:
					res += ";d"
				else:
					res += ";a"
			else:
				res += ";-"
			if self.excl:
				res += ";!"
			else:
				res += ";-"
			if self.paren:
				res += ";()"
			else:
				res += ";--"
			if self.parin:
				res += ";()"
			else:
				res += ";--"
			if self.secpage != None or self.seccoln != None or self.secid != None:
				res += ";+"
			else:
				res += ";-"
			res += ";" + str(self.spanum)
			if d == "-" and self.ad:
				res += ";" + str(self.addig)
			else:
				res += ";" + d
			res += ";" + self.content
			if not (self.ad or self.see) and self.supergloss == "?":
				res += ";" + self.content
			else:
				#print self.ad, self.see
				#assert(self.supergloss != "?")
				#print self.content
				res += ";" + self.supergloss
			res += ";[" + str(int(self.id) + 1)
			if (self.secpage != None or self.seccoln != None or self.secid != None) and self.specid != None:
				assert(False) # w tej chwili nie obslugiwane (bo sie nie trafia)
			if self.specid != None:
				res += "-" + str(int(self.specid) + 1)
			if self.secpage != None or self.seccoln != None or self.secid != None:
				res += "-"
			if self.secpage != None:
				res += str(self.secpage + 8) + ":"
			if self.seccoln != None:
				res += str(self.seccoln) + ":"
			if self.secid != None:
				res += str(int(self.secid) + 1)
			res += "]"
			res += "\n"
		return res[:-1]

def extractDigits(content, lastdig=None, comma=False):
	if len(content) > 2:
		if comma:
			if len(content) < 3:
				return (content, None, False)
			elif content[-1] != ',':
				return (content, None, False)
			else:
				content = content[:-1]
		if str.isdigit(content[-1]) and (content[-2] == ' ' or content[-2] == ','):
			dig = int(content[-1])
			#if lastdig != None:
			#	if lastdig - 1 != dig:
			#		return (content, None, False)
		else:
			return (content, None, False)
		#if dig == 1:
		if content[-2] == ' ' and (not str.isdigit(content[-3])) and content[-3] != ',':
			#assert(content[-2] == ' ')
			return (content[:-2], [str(dig)], dig == 1)
		else:
			if content[-2] == ',':
				(content, digs, one) = extractDigits(content[:-1], lastdig=dig, comma=True)
			else:
				(content, digs, one) = extractDigits(content[:-2], lastdig=dig, comma=True)
			if digs != None:
				return (content, digs + [str(dig)], one)
	return (content, None, False)

def ispageno(line):
	if len(line) < 4:
		return False
	line = line[:-1]
	if line[0] == '[' and line[-1] == ']' and str.isdigit(line[1:-1]):
		return True
	return False

def extractid(line):
	segments = line.split(" ")
	id = segments[0]
	content = ""
	for s in segments[1:]:
		content += " " + s
	content = content[1:]
	return (id, content)

def iscorrect(gloss):
	#if gloss == "da, da, da":
	#	print str.find(gloss, ",")
	if str.find(gloss, ",") != -1:
		spanum = len(gloss.split(' ')) - 1
		return (check(gloss), False, spanum)
	glosparts = gloss.split(' ')
	spanum = len(glosparts) - 1
	sum = True
	parin = False
	for g in glosparts:
		#if gloss == "drab\'":
		#	print g, ":"
		if len(g) > 2:
			if g[0] == '(' and g[-1] == ')':
				parin = True
				if not check(g[1:-1]):
					sum = False
					#if gloss == "drab\'":
					#	print "A"
				elif sum == True:
					sum = None
					#if gloss == "drab\'":
					#	print "B"
			else:
				#if gloss == "drab\'":
				#	print "C"
				if not check(g):
					sum = False
					#if gloss == "drab\'":
					#	print "D", g
		else:
			if not check(g):
				#if gloss == "drab\'":
				#	print "E"
				sum = False
	return (sum, parin, spanum)

def check(gloss):
	gloss = unicode(gloss.decode("utf-8"))
	if len(gloss) > 1:
		if gloss[-2] == u'p' and gloss[-1] == u'’':
			gloss = gloss[:-1]
		elif gloss[-1] == u'`':
			gloss = gloss[:-1]
		elif gloss[-1] == u'\'':
			#if gloss == "drab\'":
			#	print "F"
			gloss = gloss[:-1]
	prev = u'\0'
	#if gloss == "da, da, da":
	#	print gloss
	#	assert(False)
	#if gloss == "drab":
	#	print "G"	
	#if gloss == u"drab":
	#	print "H"
	for c in gloss:
		#if gloss == u"drab":
		#	print gloss, c
		if not c in [u'A', u'Ą', u'B', u'C', u'Ć', u'D', u'E', u'É', u'Ę', u'F', u'G', u'H', u'I', u'J', u'K', u'L', u'Ł', u'M', u'N', u'Ń',
				u'O', u'Ó', u'P', u'R', u'S', u'Ś', u'T', u'U', u'W', u'X', u'Y', u'Z', u'Ź', u'Ż', u'a', u'ą', u'b', u'c', u'ć', u'd', u'e',
				u'é', u'ę', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'ł', u'm', u'n', u'ń', u'o', u'ó', u'p', u'r', u's', u'ś', u't', u'u',
				u'w', u'x', u'y', u'z', u'ź', u'ż', u'‘', u' ', u'-', u',']:
			#if gloss == u"drab":
			#	print "I"
			return False
		if c in [u'A', u'Ą', u'B', u'C', u'Ć', u'D', u'E', u'É', u'Ę', u'F', u'G', u'H', u'I', u'J', u'K', u'L', u'Ł', u'M', u'N', u'Ń', u'O',
				u'Ó', u'P', u'R', u'S', u'Ś', u'T', u'U', u'W', u'X', u'Y', u'Z', u'Ź', u'Ż']:
			if prev != u' ' and prev != u'\0':
				#if gloss == u"drab":
				#	print "J"
				return False
		if c == u',' and prev == u' ':
			#print gloss
			#assert(False)
			return False
		if c != u' ' and prev == u',':
			#if gloss == u"drab":
			#	print "K"
			return False
		prev = c
	#if gloss == u"drab":
	#	print "L"
	return True

def getSuperGloss(column, prevcolumn, id):
	for g in column:
		if int(g.id) == id:
			return g.content
		if g.secid != None and int(g.secid) == id:
			return g.content
	#print len(prevcolumn)
	if prevcolumn != None:
		g = prevcolumn[-1]
		if g.secid != None and int(g.secid) == id:
			return g.content
	return None

def process(tmpcols, pageno, pages, hpage, page):
	global deferred, deferredid
	coln = 0
	for c in tmpcols:
		coln += 1
		for s in c:
				if s == "":
					continue
				else:
					if s == "EMPTY":						
						continue
					(id, content) = extractid(s)
					#print "[" + id.decode("utf-8").encode("utf-8") + "|" + content.decode("utf-8").encode("utf-8") + "]"
					if id[-1] == '!':
						continue
					id = id.split(",")
					if len(id) > 1:
						specid = id[1]
					else:
						specid = None
					id = id[0]
					if content == "EMPTY":
						continue
					else:
						#print (id, content)
						if content[-1] == "+":
							#print content
							#assert(False)
							deferred = Gloss(id, specid, content[:-1], pageno, coln, "?") #page.cols[coln - 1].append(Gloss(id, specid, content, pageno, coln, "?"))
							#assert(deferred != None)
							deferredid = (pageno, coln, id)
							continue
						if deferred != None:
							#print content
							#assert(False)
							res = get_supergloss(hpage, deferredid[0], deferredid[1], int(deferredid[2]))
							if res == None:
								page.cols[coln - 1].append(deferred.append(id, content, pageno, coln))
							else:
								sgloss = computeSuperGloss(res, pages, page, id, content, pageno, coln)
								page.cols[coln - 1].append(deferred.append(id, content, pageno, coln, sgloss))
							deferred = None
							continue
						dummy = Gloss(0, None, content, pageno, coln, "?")
						if dummy.ad or dummy.see:
							res = get_supergloss(hpage, pageno, coln, int(id), forceSubgloss=True)
						else:
							res = get_supergloss(hpage, pageno, coln, int(id))
						if res == None:
							page.cols[coln - 1].append(Gloss(id, specid, content, pageno, coln, "?"))
						else:
							sgloss = computeSuperGloss(res, pages, page, id, content, pageno, coln)
							page.cols[coln - 1].append(Gloss(id, specid, content, pageno, coln, sgloss))

def computeSuperGloss(res, pages, page, id, content, pageno, coln, two=False):
	(p, c, l, p1, c1, l1) = res
	if two:
		p = p1
		c = c1
		l = l1
	#print p, c, l, len(pages)
	if c - 1 > 0:
		if p - 1 == len(pages):
			prevcol = page.cols[c - 2]
			#print len(prevcol)
		else:
			if pages[p - 1] == None:
				prevcol = None
			else:
				prevcol = pages[p - 1].cols[c - 2]
	else:
		if p - 1 > 0:
			if pages[p - 2] == None:
				prevcol = None
			else:
				prevcol = pages[p - 2].cols[-1]
		else:
			prevcol = None
	if p - 1 == len(pages):
		sgloss = getSuperGloss(page.cols[c - 1], prevcol, l)
	else:
		sgloss = getSuperGloss(pages[p - 1].cols[c - 1], prevcol, l)	
	if sgloss == None and (not two):
		return computeSuperGloss(res, pages, page, id, content, pageno, coln, two=True)
	return sgloss

def main(argv):
	global deferred, deferredid
	hpage = extract(argv[3], argv[4])
	fin = open(argv[1])
	pages = []
	pageno = 0
	deferred = None
	deferredid = None
	page = None
	tmpcols = [[], [], [], []]
	for line in fin:		
		if line == "\n":
			continue
		elif ispageno(line):
			if tmpcols != None:
				process(tmpcols, pageno, pages, hpage, page)
			if page != None:
				pages.append(page)
			if pageno + 9 == 350:
				pages.append(None)
				pageno += 1
			page = Page(line[1:-2])			
			tmpcols = [[], [], [], []]
			pageno += 1
			#if pageno == 2:
			#	assert(False)
			assert(pageno + 8 != 350)
		else:
			line = line[:-1]
			segments = line.split('\t')
			i = -1
			#assert(len(tmpcols) == 4)
			for s in segments:
				#print "[" + s + "]"
				if s != "":
					i += 1
					#print s
					#assert(i < 5)
					#print len(tmpcols), i
					tmpcols[i].append(s)
	if page != None:
		if tmpcols != None:
			process(tmpcols, pageno, pages, hpage, page)
		pages.append(page)
	fin.close()
	fout = open(argv[2], "w")
	for p in pages:
		if p == None:
			continue
		for c in p.cols:
			i = 0
			for el in c:
				i += 1
				fout.write(el.str(i) + "\n")
			fout.write("\n")
		fout.write("\n")
	fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

#`
#? spacje nawiasy
#- niezgodne
#
#ad, zob. tylko w podhasłach

