#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from optparse import OptionParser

def semiSep(txt, gap=0):
    return unicode(txt) + u";"

def humanSep(txt, gap=20):
    diff = gap - len(unicode(txt))
    res = u""
    for i in range(0, diff): res += u" "
    return unicode(txt) + res

url = u"http://poliqarp.wbl.klf.uw.edu.pl/extra/linde/index.djvu"

class Word:

    global url

    def __init__(self, text, pageno, colno, lineno, indent, wordIndex, charIndex, colPrefix, globalWordIndex, globalCharIndex, globalPrefix, italic, bold, family, size, bbox, rel):
        self.text = text
        self.pageno = pageno
        self.colno = colno
        self.lineno = lineno
        self.indent = indent
        self.secIndent = None
        self.wordIndex = wordIndex
        self.charIndex = charIndex
        self.colPrefix = colPrefix
        self.afterWords = []
        self.globalWordIndex = globalWordIndex
        self.globalCharIndex = globalCharIndex
        self.globalPrefix = globalPrefix
        self.italic = italic
        self.secitalic = None
        self.bold = bold
        self.secbold = None
        self.family = family
        self.secfamily = None
        self.size = size
        self.secsize = None
        self.bbox = bbox
        self.rel = rel
        self.__outfiles = None
    
    def setOutFiles(self, outfiles):
        self.__outfiles = outfiles
    
    def addAfterWord(self, word):
        self.afterWords.append(word)
    
    def join(self, word):
        self.secIndent = word.indent
        self.secfamily = word.family
        self.secbold = word.bold
        self.secitalic = word.italic
        self.secsize = word.size
        self.text += word.text
    
    def __url(self, pageno):
        global url
        if self.__outfiles == None:
            return url
        else:
          for (name, fromm, too) in self.__outfiles:
            if pageno >= fromm and pageno <= too:
              return name
        assert(False)
    
    def toString(self, humanReadable=False):
        res = u""
        if not humanReadable:
            res = u"0;;1;1;"        
        if humanReadable:
            sep = humanSep
        else:
            sep = semiSep
        res += sep(unicode(self.pageno) + u";" + unicode(self.colno) + u";" + unicode(self.lineno), gap=10)
        res += sep(self.text)
        if self.secIndent != None:
            res += sep(unicode(self.indent) + u"," + unicode(self.secIndent), gap=8)
        else:
            res += sep(unicode(self.indent), gap=8)
        res += sep(unicode(self.wordIndex) + u";" + unicode(self.charIndex), gap=7) + sep(self.colPrefix.replace(u";", u"\<sr>"), gap=18)
        first = True
        sum = u""
        for w in self.afterWords:
            sum += (u"<" if humanReadable else u"") + w.replace(u";", u"\<sr>") + (u">" if humanReadable else u"")
            if first:
                first = False
            else:
                sum += u" "
        res += sep(sum, gap=30)
        res += sep(str(self.globalWordIndex) + u";" + unicode(self.globalCharIndex), gap=10) + sep(self.globalPrefix.replace(u";", u"\<sr>"), gap=18)
        if not humanReadable:
            if self.secfamily != None:
                res += sep((u"i" if self.italic else u"s") + (u"b" if self.bold else u"n") + self.family + u"," + (u"i" if self.secitalic else u"s") + (u"b" if self.secbold else u"n") + self.secfamily, gap=10)
                res += sep(self.size + u"," + self.secsize, gap=20)
            else:
                res += sep((u"i" if self.italic else u"s") + (u"b" if self.bold else u"n") + self.family, gap=10)
                res += sep(self.size, gap=20)
            res += self.__url(self.pageno) + u"?djvuopts&page=" + unicode(self.pageno) + u"&zoom=width&showposition=0.535," + (unicode(self.rel)[:5] if len(unicode(self.rel)) > 5 else unicode(self.rel)) + u"&highlight=" + unicode(self.bbox[0]) + u"," + unicode(self.bbox[3]) + u"," + unicode(self.bbox[2] - self.bbox[0]) + u"," + unicode(self.bbox[1] - self.bbox[3])
        return res

class MyHandler(ContentHandler):

    def __init__(self, *args, **kwargs):
        ContentHandler.__init__(self, *args, **kwargs)
        self.__stack = []
        self.__isWord = False
        self.__isCol = False
        self.__wordStart = 0
        self.__colStart = 0
        self.__wordIndex = 0
        self.__charIndex = 0
        self.__globalWordIndex = 0
        self.__globalCharIndex = 0
        self.__globalPrefix = u""
        self.__colPrefix = u""
        self.__word = u""
        self.__words = []
        self.__pageno = 0
        self.__colno = -1
        self.__lineno = 0
        self.__minWordIndex = 3
        self.__minCharIndex = 10
        self.__maxAfterWords = 1
        self.__minGlobalWordIndex = 3
        self.__minGlobalCharIndex = 10
        self.__immediateBuffer = []
        self.__italic = False
        self.__bold = False
        self.__size = 0.0
        self.__family = u""
        self.__words = []
        self.__last = None
        self.__wasHyphen = False
        self.__lineBegin = False
        self.__bbox = [0, 0, 0, 0]
        self.__pagebbox = [0, 0, 0, 0]
        self.__width = None
        self.__height = None
        self.__ignpags = []
        self.__ignore = False
        self.__outfiles = None
        self.__rel = 0.0
        self.__map = {"Impact": "Im", "Georgia": "Ge", "Arial": "Ar", "Trebuchet MS": "Tr", "Times New Roman": "Ti",
            "Tahoma": "Ta", "Palatino Linotype": "Pa"}
    
    def setParameters(self, minWordIndex=3, minCharIndex=10, maxAfterWords=1, minGlobalWordIndex=3, minGlobalCharIndex=10):
        self.__minWordIndex = minWordIndex
        self.__minCharIndex = minCharIndex
        self.__maxAfterWords = maxAfterWords
        self.__minGlobalWordIndex = minGlobalWordIndex
        self.__minGlobalCharIndex = minGlobalCharIndex
    
    def setOutFiles(self, outfiles):
       self.__outfiles = outfiles
    
    def setPageNo(self, no):
        self.__pageno = no - 1
    
    def setIgnPags(self, ignpags):
        self.__ignpags = ignpags
    
    def setResolution(self, w, h):
        self.__width = w
        self.__height = h
    
    def getWords(self):
        return self.__words

    def __clazz(self, attrs):
        try:
            title = attrs.getValue(u"class")
        except KeyError:
            return u"dummy"
        else:
            return title
    
    def __getBbox(self, attrs):
        try:
            title = attrs.getValue(u"title")
            els = title.split(u";")
            bbox = [0, 0, 0, 0]
            for el in els:
                if el.find(u"bbox") != -1:
                    coords = el.lstrip().split(u" ")
                    #print coords
                    bbox = [int(coords[1]), int(coords[2]), int(coords[3]), int(coords[4])]
                    break
        except KeyError:
            return [0, 0, 0, 0]
        return bbox
    
    def __isItalic(self, attrs):
        try:
            title = attrs.getValue("style")
            els = title.split(u";")
            for el in els:
                if el.find(u"font-style") != -1:
                    coords = el.lstrip().split(u" ")
                    if coords[1] == u"italic":
                        return True
        except KeyError:
            return False
        return False

    def __isBold(self, attrs):
        try:
            title = attrs.getValue("style")
            els = title.split(u";")
            for el in els:
                if el.find(u"font-weight") != -1:
                    coords = el.lstrip().split(u" ")
                    if coords[1] == u"bold":
                        return True
        except KeyError:
            return False
        return False

    def __getFamily(self, attrs):
        try:
            title = attrs.getValue("style")
            els = title.split(u";")
            for el in els:
                if el.find(u"font-family") != -1:
                    coords = el.lstrip().split(u":")
                    return self.__map[coords[1][1:]]
        except KeyError:
            return u""
        return u""
    
    def __getSize(self, attrs):
        try:
            title = attrs.getValue("style")
            els = title.split(u";")
            for el in els:
                if el.find(u"font-size") != -1:
                    coords = el.lstrip().split(u":")
                    return coords[1][1:-2]
        except KeyError:
            return u""
        return u""
    
    def __notifyImmediateBuffer(self, word):
        for el in self.__immediateBuffer:
            el[0].addAfterWord(word)
            el[1] -= 1
        self.__immediateBuffer = [[w, i] for [w, i] in self.__immediateBuffer if i > 0]

    def startElement(self, name, attrs):
        clazz = self.__clazz(attrs)
        bbox = self.__getBbox(attrs)
        self.__stack.append(clazz)
        if clazz == u"ocr_page":
            self.__pageno += 1
            if self.__pageno in self.__ignpags:
              self.__ignore = True
              return
            else:
              self.__ignore = False
            self.__colno = -1
            self.__pagebbox = bbox
            #print bbox
            #if self.__pageno == 435:
            #    print bbox
        elif clazz == u"ocr_carea":
            if self.__ignore: return
            self.__colno += 1
            self.__lineno = 0
            if self.__colno in [1, 2, 3, 4]:
                self.__isCol = True
            self.__colStart = bbox[0]
        elif clazz == u"ocr_line":
            if self.__ignore: return
            self.__lineno += 1
            self.__wordIndex = 0
            self.__charIndex = 0
            self.__colPrefix = u""
            self.__lineBegin = True
        elif clazz == u"ocrx_word":
            if self.__ignore: return
            self.__isWord = True
            self.__wordStart = bbox[0]
            self.__word = u""
            self.__bbox = bbox
            #self.__pagebbox[3] = 766
            self.__bbox[1] = self.__pagebbox[3] - self.__bbox[1]
            self.__bbox[3] = self.__pagebbox[3] - self.__bbox[3]
            if self.__width != None:
            #if False:
                self.__bbox[0] *= self.__width
                self.__bbox[2] *= self.__width
                self.__bbox[1] *= self.__height
                self.__bbox[3] *= self.__height
                self.__bbox[0] /= self.__pagebbox[2]
                self.__bbox[2] /= self.__pagebbox[2]
                self.__bbox[1] /= self.__pagebbox[3]
                self.__bbox[3] /= self.__pagebbox[3]
                self.__rel = 1.0 - float(self.__bbox[3]) / self.__height
            else:
                self.__rel = 1.0 - float(self.__bbox[3]) / self.__pagebbox[3]
        elif clazz == u"dummy":
            if self.__ignore: return
            self.__italic = self.__isItalic(attrs)
            self.__bold = self.__isBold(attrs)
            self.__family = self.__getFamily(attrs)
            self.__size = self.__getSize(attrs)

    def endElement(self, name):
        clazz = self.__stack.pop()
        if self.__ignore: return
        if clazz == u"ocrx_word":
            self.__isWord = False
            #if self.__isCol:
            #    self.__notifyImmediateBuffer(self.__word)
            if self.__word.isupper() and len(self.__word) > 1 and self.__isCol:
                if self.__wordIndex < self.__minWordIndex or self.__charIndex < self.__minCharIndex:
                    colPrefix = self.__colPrefix
                else:
                    colPrefix = u""
                if self.__globalWordIndex < self.__minGlobalWordIndex or self.__globalCharIndex < self.__minGlobalCharIndex:
                    globalPrefix = self.__globalPrefix
                else:
                    globalPrefix = u""
                #if self.__pageno == 435 and self.__word == u"DŁUGOŻYWOTNY":
                #    print self.__bbox
                word = Word(self.__word, self.__pageno, self.__colno, self.__lineno, self.__wordStart - self.__colStart, self.__wordIndex, self.__charIndex, colPrefix, self.__globalWordIndex, self.__globalCharIndex, globalPrefix, self.__italic, self.__bold, self.__family, self.__size, self.__bbox, self.__rel)
                word.setOutFiles(self.__outfiles)
                if self.__wasHyphen and self.__lineBegin:
                    self.__wasHyphen = False
                    self.__last.join(word)
                    #print self.__last.text, self.__last.afterWords
                    self.__last = None
                else:
                    if self.__wasHyphen:
                        self.__wasHyphen = False
                        self.__notifyImmediateBuffer(u"-")
                    self.__notifyImmediateBuffer(self.__word) # TODO: uwaga w przypadku multiline beda osobno liczone polowki
                    self.__last = word
                    self.__words.append(word)
                    self.__immediateBuffer.append([word, self.__maxAfterWords])
                self.__globalWordIndex = 0
                self.__globalCharIndex = 0
                self.__globalPrefix = u""
            elif self.__isCol:
                self.__globalWordIndex += 1
                self.__globalCharIndex += len(self.__word)
                self.__globalPrefix += self.__word
                if self.__word != u"-" or self.__wasHyphen:
                    if self.__wasHyphen:
                        self.__notifyImmediateBuffer(u"-")
                    self.__notifyImmediateBuffer(self.__word)
                    self.__last = None
                    self.__wasHyphen = False
                elif self.__word == u"-" and self.__last != None:
                    self.__wasHyphen = True
                self.__lineBegin = False
            self.__wordIndex += 1
            self.__charIndex += len(self.__word)
            self.__colPrefix += self.__word
            self.__word = u""
        elif clazz == u"ocr_carea":
            self.__isCol = False

    def characters(self, content):
        if self.__ignore: return
        if self.__isWord:
            self.__word += content

def main(argv):
    global url
    usage = "%prog [OPTIONS] INPUT_FILE OUTPUT_FILE"
    parser = OptionParser(usage = usage, version = "hocr_parser 0.1")
    parser.add_option("-H", "--human", action="store_true", help="human readable format", dest="human", default=False)
    parser.add_option("-r", "--resolution", help="djvu document resolution", dest="res", default=None)
    parser.add_option("-u", "--url", help="djvu document url", dest="url", default=None)
    (options, args) = parser.parse_args(argv)
    fout = open(args[2], "w")
    if options.url != None:
        url = unicode(options.url)
    handler = MyHandler()
    handler.setParameters(maxAfterWords=3)
    if options.res != None:
        handler.setResolution(int(options.res.split("x")[0]), int(options.res.split("x")[1]))
    saxparser = make_parser()
    saxparser.setContentHandler(handler)
    datasource = open(args[1], "r")
    saxparser.parse(datasource)
    for w in handler.getWords():
        fout.write((w.toString(humanReadable=options.human) + u"\n").encode("utf-8"))
    fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

