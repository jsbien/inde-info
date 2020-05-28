#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

class HOCRPage:

	def __init__(self, no):
		self.hcols = []
		self.hno = no

class MyHandler(ContentHandler):

	def __init__(self, *args, **kwargs):
		ContentHandler.__init__(self, *args, **kwargs)
		self.__stack = []
		self.__page = None
		self.__pageno = 0
		self.__carea = None
		self.__careaInd = 0
		self.__line = None
		self.pages = []
		self.__size = "0.0"
		self.__special = False
	
	def setSpecial(self):
		self.__special = True

	def __clazz(self, attrs):
		try:
			title = attrs.getValue(u"class")
		except KeyError:
			return u"dummy"
		else:
			return title

	def startElement(self, name, attrs):
		self.__stack.append(self.__clazz(attrs))
		if self.__clazz(attrs) == u"ocr_page":
			self.__pageno += 1
			if self.__pageno < 9 and (not self.__special):
				self.pages.append(None)
				return
			self.__careaInd = -1
			if (not self.__special) and self.__pageno > 349:
				self.__page = HOCRPage(self.__pageno + 1)
			elif self.__special:
				self.__page = HOCRPage(350)
			else:
				self.__page = HOCRPage(self.__pageno)
		if self.__pageno < 9 and (not self.__special):
			return
		if self.__clazz(attrs) == u"ocr_carea":
			self.__careaInd += 1
			self.__carea = []
			#print "carea"#, self.__carea
		if self.__clazz(attrs) == u"ocr_line":
			self.__line = ""
		if self.__clazz(attrs) == u"dummy":
			try:
				font = attrs.getValue(u"style")
			except KeyError:
				return
			font = font.split(";")
			for f in font:
				f = f.split(":")
				#print f
				if len(f) == 2 and f[0] == u" font-size":
					#print f[1][1:-2]
					self.__size = f[1][1:-2]

	def endElement(self, name):
		type = self.__stack.pop()
		if self.__pageno < 9 and (not self.__special):
			return
		if type == u"ocr_line":
			#print self.__size
			if float(self.__size) < 10.0:
				self.__carea.append((self.__line, "subgloss"))
			else:
				self.__carea.append((self.__line, "gloss"))
			self.__line = None
		if type == u"ocr_carea":
			#print "end carea"#, self.__carea
			#if len(self.__carea) == 0:
			#	print "ZLE"
			if self.__careaInd > 0 and self.__careaInd < 5:
				self.__carea.reverse()
				#assert(self.__carea != None)
				self.__page.hcols.append(self.__carea)
			#assert(len(self.__carea) > 0)
			#assert(len(self.__page.hcols[-1]) > 0)
		if type == u"ocr_page":
			#if len(self.pages) == 8:
			#	assert(len(self.__carea) > 0)
			#	assert(len(self.__page.hcols[0]) > 0)
			self.pages.append(self.__page)
			#inspect(self.pages)

	def characters(self, content):
		if self.__pageno < 9 and (not self.__special):
			return
		if self.__line != None:
			#print content
			self.__line += content

def prevof(pages, page, col, line):
	assert(isinstance(pages, list))
	#print page, col, line
	if line > 0:
		return (page, col, line - 1)
	if col - 1 > 0:
		return (page, col - 1, len(pages[page + 7].hcols[col - 2]) - 1)
	#print page
	return (page - 1, len(pages[page + 6].hcols), len(pages[page + 6].hcols[-1]) - 1)

#def inspect(pages):
#	for p in pages:
#		if p == None:
#			continue
#		for c in p.hcols:
#			assert(len(c) != 0)

def get_supergloss(pages, page, col, line, forceSubgloss=False):
	#print page, str(page + 8), col, line
	#print len(pages[page + 7].hcols[col - 1])
	#if page + 8 == 351 and col == 2 and line == 49:
	#	i = -1
	#	for c in pages[page + 7].hcols[col - 1]:
	#		i += 1
	#		print c, i
	(content, type) = pages[page + 7].hcols[col - 1][line]
	#if content == "bronienie":
	#	print type
	#	assert(False)
	#if page + 8 == 200:
	#	print content.encode("utf-8"), type
	if type == "gloss" and (not forceSubgloss):
		return None
	prev = None
	while True:
		(page, col, line) = prevof(pages, page, col, line)
		#print str(page + 8), col, line
		(_, type) = pages[page + 7].hcols[col - 1][line]
		if type == "gloss":
			if prev == None:
				prev = (page, col, line)
			else:
				return (prev[0], prev[1], prev[2], page, col, line)
	# lepiej sprawdzac (ad i kolejnosc alfabetyczna)

def extract(file1, file2):
	handler = MyHandler()
	saxparser = make_parser()
	saxparser.setContentHandler(handler)
	datasource = open(file1, 'r')
	saxparser.parse(datasource)
	pages = handler.pages
	handler = MyHandler()
	handler.setSpecial()
	saxparser = make_parser()
	saxparser.setContentHandler(handler)
	datasource = open(file2, 'r')
	saxparser.parse(datasource)
	pages = pages[0:349] + handler.pages + pages[349:]
	#print pages
	return pages

