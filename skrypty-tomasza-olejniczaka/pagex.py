#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

# skrypt sluzy do ekstrakcji paginy z plikow wygenerowanych przez Poprawiacza na potrzeby gloscheck.py
# format wyniku:
# nr_strony,pierwszy_element_paginy,trzeci_element_paginy[!]
# ! jezeli z pagina jest cos nie tak - przed dalszym uzyciem plik wynikowy nalezy bezwzglednie poprawic recznie
# pagex KATALOG_Z_WYNIKAMI_POPRAWIACZA PLIK_WYNIKOWY

b = [u'a', u'ą', u'b', u'c', u'ć', u'd', u'e', u'ę', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'ł', u'm', u'n', u'ń',
		u'o', u'ó', u'p', u'r', u's', u'ś', u't', u'u', u'v', u'w', u'x', u'y', u'z', u'ź', u'ż']

def lt(fst, snd):
	global b
	i = b.index(fst)
	j = b.index(snd)
	return i < j

def okk(fst, snd):
	try:
		fst = fst[1:].lower()
		snd = snd[1:].lower()
		fst = fst.replace(u'é', u'e')
		snd = snd.replace(u'é', u'e')
		i = len(fst) - 1
		j = len(snd) - 1
		while i >= 0 and j >= 0:
			if i < 0 or j < 0:
				break
			if lt(fst[i], snd[j]):
				return True
			elif lt(snd[j], fst[i]):
				return False
			else:
				i -= 1
				j -= 1
		return True
	except ValueError:
		return False

def ok(fst, snd):
	try:
		fst = fst[1:].lower()
		snd = snd[1:].lower()
		i = len(fst) - 1
		j = len(snd) - 1
		while i >= 0 and j >= 0:
			if i < 0 or j < 0:
				break
			if lt(fst[i], snd[j]):
				return True
			elif lt(snd[j], fst[i]):
				return False
			else:
				i -= 1
				j -= 1
		if len(fst) <= len(snd):
			return True
		else:
			return False
	except ValueError:
		return False

class MyHandler(ContentHandler):

	def __init__(self, *args, **kwargs):
		ContentHandler.__init__(self, *args, **kwargs)
		self.__stack = []
		self.__ind = 0
		self.__pag = []
		self.__text = None
	
	def getPag(self):
		return self.__pag

	def __clazz(self, attrs):
		try:
			title = attrs.getValue(u"class")
		except KeyError:
			return u"dummy"
		else:
			return title

	def startElement(self, name, attrs):
		self.__stack.append(self.__clazz(attrs))
		if self.__clazz(attrs) == u"ocr_line":
			self.__ind += 1
			if self.__ind in [1, 3]:
				self.__text = u""

	def endElement(self, name):
		type = self.__stack.pop()
		if type == u"ocr_line":
			if self.__ind in [1, 3]:
				self.__pag.append(self.__text)
				self.__text = None

	def characters(self, content):
		if self.__text != None:
			self.__text += content

def main(argv):
	fout = open(argv[2], "w")
	for i in range(9, 392):
		path = argv[1] + "/tmp_" + str(i) + ".xml"
		if os.path.exists(path):
			handler = MyHandler()
			saxparser = make_parser()
			saxparser.setContentHandler(handler)
			datasource = open(path, "r")
			saxparser.parse(datasource)
			if handler.getPag()[0][0] != '-' or handler.getPag()[1][0] != '-' or (not ok(handler.getPag()[0], handler.getPag()[1])):
				fout.write((unicode(i) + "," + handler.getPag()[0] + "," + handler.getPag()[1] + "!\n").encode("utf-8"))
			else:
				fout.write((unicode(i) + "," + handler.getPag()[0] + "," + handler.getPag()[1] + "\n").encode("utf-8"))
		else:
			fout.write(str(i) + "!\n")

if __name__ == '__main__': sys.exit(main(sys.argv))

