#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import wx
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax.handler import feature_validation
from xml.sax.handler import feature_external_ges
from xml.sax.saxutils import XMLFilterBase
from xml.sax.saxutils import XMLGenerator

TEXTEL_PATH = "/home/jsbien/extraUnicodeData/TextelNormalization.txt"
#TEXTEL_PATH = "../textel/TextelNormalization.txt"

def hex2char(heks):
	i = int(heks, 16)
	#print i
	return unichr(i)

def getLigs():
	f = open(TEXTEL_PATH, "r")
	dic = {}
	for line in f:
		if line[0] == '#':
			continue
		if line == "\n":
			continue
		els = line.split(";")
		fromm = hex2char(els[0])
		too = els[2].split(" ")
		ts = u""
		for i in range(len(too)):
			ts += hex2char(too[i])
		#print fromm, ts
		dic.setdefault(fromm, ts)
	f.close()
	return dic

class MyAttrs:

	def __init__(self, mydict):
		self.__dict = mydict

	def copy(self):
		return MyAttrs(self.__dict.copy())

	def get(self, key):
		return self.__dict.get(key)

	def has_key(self, key):
		return self.__dict.has_key(key)

	def items(self):
		return self.__dict.items()

	def keys(self):
		return self.__dict.keys()
	
	def values(self):
		return self.__dict.values()
	
	def getLength(self):
		return len(self.__dict.keys())
	
	def getNames(self):
		return self.__dict.keys()
	
	def getType(self, key):
		return type(self.__dict.get(key))
	
	def getValue(self, key):
		return self.__dict[key]

class MyFilter(XMLFilterBase):

	def __init__(self, upstream, downstream):
		XMLFilterBase.__init__(self, upstream)
		self.__downstream = downstream
		self.__isUni = False
		self.__ligs = getLigs()

	def startElement(self, name, attrs):
		if name == u"Unicode":
			self.__isUni = True
		self.__downstream.startElement(name, attrs)

	def endElement(self, name):
		if name == u"Unicode":
			self.__isUni = False
		self.__downstream.endElement(name)

	def characters(self, content):
		if self.__isUni:
			text = content
			for (k, v) in self.__ligs.iteritems():
				text = text.replace(k, v)
			self.__downstream.characters(text)
		else:
			self.__downstream.characters(content)

def main(argv):
	#feature_validation = "false"
	#feature_external_ges = "false"
	saxparser = make_parser()
	saxparser.setFeature(feature_validation,False)
	saxparser.setFeature(feature_external_ges,False)
	#feature_validation = "false"
	#feature_external_ges = "false"
	out = open(argv[2], "w")
	out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
	generator = XMLGenerator(out, "utf-8")
	filter = MyFilter(saxparser, generator)
	filter.parse(argv[1])
	out.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

