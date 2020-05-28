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

class MyAttrs:

  def __init__(self, myDict):
    self.__dict = myDict
    
  def keys(self):
    return self.__dict.keys()
  
  def items(self):
    return self.__dict.items()

  def values(self):
    return self.__dict.values()

  def has_key(self, key):
    return self.__dict.has_key(key)
  
  def copy(self):
    return MyAttrs(self.__dict.copy())
  
  def get(self, attr):
    return self.__dict.get(attr)

  def getValue(self, name):
    return self.__dict[name]

  def getLength(self):
    return len(self.__dict.keys())
  
  def getNames(self):
    return self.__dict.keys()
  
  def getType(self, name):
    return type(self.__dict[name])

class MyFilter(XMLFilterBase):

  def __init__(self, upstream, downstream):
    XMLFilterBase.__init__(self, upstream)
    self.__downstream = downstream
    self.__stack = []
    
  def __getBbox(self, attrs):
    try:
      title = attrs.getValue("title")
    except KeyError:
      return None
    if title != None:
       els = title.split(";")
       #print els
       for el in els:
         elel = el.split(" ")
         if len(elel) == 5 and elel[0] == u"bbox":
           return [int(elel[1]), int(elel[2]), int(elel[3]), int(elel[4])]
    else:
      return None

  def __getBboxText(self, attrs):
    try:
      title = attrs.getValue("title")
    except KeyError:
      return u""
    if title != None:
       els = title.split(";")
       #print els
       for el in els:
         elel = el.split(" ")
         if len(elel) == 5 and elel[0] == u"bbox":
           return el
    else:
      return u""     
  
  def __bboxOk(self, bbox, parentbbox):
    if parentbbox == None or bbox == None:
      return True
    if bbox[0] < parentbbox[0] or bbox[1] < parentbbox[1] or bbox[2] > parentbbox[2] or bbox[3] > parentbbox[3]:
      return False
    return True

  def __trim(self, bbox, parentbbox):
    if bbox[0] < parentbbox[0]:
      bbox[0] = parentbbox[0]
    if bbox[1] < parentbbox[1]:
      bbox[1] = parentbbox[1]
    if bbox[2] > parentbbox[2]:
      bbox[2] = parentbbox[2]
    if bbox[3] > parentbbox[3]:
      bbox[3] = parentbbox[3]
    return bbox

  def startElement(self, name, attrs):
    bbox = self.__getBbox(attrs)
    bboxtext = self.__getBboxText(attrs)
    if bbox == None:
      if len(self.__stack) > 0:
        bbox = self.__stack[-1]
    notok = False
    if len(self.__stack) > 0:
      if not self.__bboxOk(bbox, self.__stack[-1]):
        #print bbox, self.__stack[-1], name
        notok = True
        bbox = self.__trim(bbox, self.__stack[-1])
        #print bbox
    self.__stack.append(bbox)    
    if notok:
      na = {}
      for k in attrs.getNames():
        if k != u"title":
          na.setdefault(k, attrs.getValue(k))
        else:
          na.setdefault(k, attrs.getValue(k).replace(bboxtext, u" bbox " + unicode(bbox[0]) + u" " + unicode(bbox[1]) + u" " + unicode(bbox[2]) + u" " + unicode(bbox[3])))
      #print na
      #na.setdefault("mybbox", str(bbox))
      #na.setdefault("parent", self.__stack[-2])
      attrs = MyAttrs(na)
    self.__downstream.startElement(name, attrs)
    #print type(attrs)
    # attrs.getValue("bbox")

  def endElement(self, name):
    self.__stack.pop()
      #$self.__downstream.startElement(u"base", {})
    self.__downstream.endElement(name)

  def characters(self, content):
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
  out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n")
  #out.write("<!DOCTYPE cesAna SYSTEM \"xcesAnaIPI.dtd\">\n")
  generator = XMLGenerator(out, "utf-8")
  filter = MyFilter(saxparser, generator)
  #print argv[1]
  filter.parse(argv[1])
  out.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

