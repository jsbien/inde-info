#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax.handler import feature_validation
from xml.sax.handler import feature_external_ges

class MyFilter(ContentHandler):

	def __init__(self, fout):
		ContentHandler.__init__(self)
		#self.__isOrth = False
		self.__isBase = False
		#self.__orthText = u""
		self.__fout = fout

	def startElement(self, name, attrs):
		#if name == u"orth":
		#	self.__isOrth = True
		if name == u"base":
			self.__isBase = True
		#print type(attrs)
		# attrs.getValue("bbox")

	def endElement(self, name):
		#if name == u"orth":
		#	self.__isOrth = False
		if name == u"base":
			self.__isBase = False

	def characters(self, content):
		#if self.__isOrth:
		#	self.__orthText += content
		if self.__isBase:
			self.__fout.write(content.encode("utf-8"))

def main(argv):
	saxparser = make_parser()
	saxparser.setFeature(feature_validation,False)
	saxparser.setFeature(feature_external_ges,False)
	#feature_validation = "false"
	#feature_external_ges = "false"
	out = open(argv[2], "w")
	filter = MyFilter(out)
	datasource = open(argv[1], 'r')
	saxparser.setContentHandler(filter)
	#print argv[1]
	saxparser.parse(datasource)
	out.close()

if __name__ == '__main__': sys.exit(main(sys.argv))
	
