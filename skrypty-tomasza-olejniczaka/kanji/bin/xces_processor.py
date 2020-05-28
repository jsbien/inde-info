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

#TEXTEL_PATH = "/home/jsbien/extraUnicodeData/TextelNormalization.txt"

def hex2char(heks):
	i = int(heks, 16)
	#print i
	return unichr(i)

def getLigs(TEXTEL_PATH):
	f = open(TEXTEL_PATH, "r")
	dic = {}
	for line in f:
		if line[0] == '#':
			continue
		if line == "\n":
			continue
		els = line.split(";")
		fromm = els[0].split(" ")
		too = els[2].split(" ")
		fs = u""
		ts = u""
		for i in range(len(fromm)):
			fs += hex2char(fromm[i])
		for i in range(len(too)):
			ts += hex2char(too[i])
		#print fs, ts
		#print fromm, ts
		dic.setdefault(fs, ts)
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

	def __init__(self, upstream, downstream, TEXTEL_PATH):
		XMLFilterBase.__init__(self, upstream)
		self.__downstream = downstream
		self.__isOrth = False
		self.__isBase = False
		self.__orthText = u""
		self.__ligs = getLigs(TEXTEL_PATH)

	def startElement(self, name, attrs):
		if name == u"orth":
			self.__isOrth = True
			self.__orthText = u""
		if name == u"base":
			self.__isBase = True
		self.__downstream.startElement(name, attrs)
		#print type(attrs)
		# attrs.getValue("bbox")

	def endElement(self, name):
		if name == u"orth":
			self.__isOrth = False
			for (k, v) in self.__ligs.iteritems():
				self.__orthText = self.__orthText.replace(k, v)
			#self.__downstream.startElement(u"base", MyAttrs({}))
			self.__downstream.characters(self.__orthText)
			#self.__downstream.endElement(u"base")
			#self.__orthText = u""
		if name == u"base":
			self.__isBase = False
		self.__downstream.endElement(name)

	def characters(self, content):
		if self.__isOrth:
			self.__orthText += content
		#if self.__isOrth:
		#	text = content
		#	for (k, v) in self.__ligs.iteritems():
		#		text = text.replace(k, v)
		#	self.__downstream.characters(text)
		else:
			self.__downstream.characters(content)

def main(argv):
	#feature_validation = "false"
	#feature_external_ges = "false"
	saxparser = make_parser()
	saxparser.setFeature(feature_validation, False)
	saxparser.setFeature(feature_external_ges, False)
	#feature_validation = "false"
	#feature_external_ges = "false"
	out = open(argv[2], "w")
	out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
	out.write("<!DOCTYPE cesAna SYSTEM \"xcesAnaIPI.dtd\">\n")
	generator = XMLGenerator(out, "utf-8")
	filter = MyFilter(saxparser, generator, argv[3])
	#print argv[1]
	filter.parse(argv[1])
	out.close()

if __name__ == '__main__': sys.exit(main(sys.argv))
