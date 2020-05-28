#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import wx
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

class Preview(wx.Panel):
	def __init__(self, parent, pages):
		wx.Panel.__init__(self, parent)
		self.pages = pages
		self.i = 0
		self.Draw()
		self.Bind(wx.EVT_PAINT, self.Paint)
		#self.Bind(wx.EVT_LEFT_UP, self.OnLeft)
		#self.Bind(wx.EVT_RIGHT_UP, self.OnRight)
		self.bbox = None
	def nextPage(self):
		if self.i < len(self.pages) - 1:
			self.i += 1
			return self.i
		return None
	def page(self, pg):
		self.i = pg - 1
	def prevPage(self):
		if self.i > 0:
			self.i -= 1
			return self.i
		return None
	def Paint(self, event):
		SCALE = 7
		dc = wx.PaintDC(self)
		#print len(self.pages)
		k = 0
		for div in self.pages[self.i].children:
			k += 1
			self.bbox = div.bbox
			dc.SetPen(wx.Pen("blue", 1))
			dc.DrawLine(self.bbox[0]/SCALE, self.bbox[1]/SCALE, self.bbox[2]/SCALE, self.bbox[1]/SCALE)
			dc.DrawLine(self.bbox[0]/SCALE, self.bbox[1]/SCALE, self.bbox[0]/SCALE, self.bbox[3]/SCALE)
			dc.DrawLine(self.bbox[2]/SCALE, self.bbox[3]/SCALE, self.bbox[0]/SCALE, self.bbox[3]/SCALE)
			dc.DrawLine(self.bbox[2]/SCALE, self.bbox[3]/SCALE, self.bbox[2]/SCALE, self.bbox[1]/SCALE)
			for word in div.children:
				#if word.children[0].isupper() or word.children[0] == u"-":
				if True:
					dc.SetPen(wx.Pen("black", 1))
					height = (word.bbox[3]/SCALE - word.bbox[1]/SCALE)
					#width = (word.bbox[2]/SCALE - word.bbox[0]/SCALE)
					font = dc.GetFont()
					if height != 0:
						font.SetPixelSize((height, height))
					dc.SetFont(font)
					dc.DrawText(word.children[0], word.bbox[0]/SCALE, word.bbox[1]/SCALE)
					dc.SetPen(wx.Pen("red" if k == 3 else ("gray" if k == 2 else "green"), 1))
					dc.DrawLine(word.bbox[0]/SCALE, word.bbox[1]/SCALE, word.bbox[2]/SCALE, word.bbox[1]/SCALE)
					dc.DrawLine(word.bbox[0]/SCALE, word.bbox[1]/SCALE, word.bbox[0]/SCALE, word.bbox[3]/SCALE)
					dc.DrawLine(word.bbox[2]/SCALE, word.bbox[3]/SCALE, word.bbox[0]/SCALE, word.bbox[3]/SCALE)
					dc.DrawLine(word.bbox[2]/SCALE, word.bbox[3]/SCALE, word.bbox[2]/SCALE, word.bbox[1]/SCALE)					
		return
	def Draw(self):
		SCALE = 7
		#print len(self.pages)
		#print self.i
		k = 0
		for div in self.pages[self.i].children:
			k += 1
			self.bbox = div.bbox
			dc = wx.MemoryDC()
			dc.SetPen(wx.Pen("blue", 1))
			dc.DrawLine(self.bbox[0]/SCALE, self.bbox[1]/SCALE, self.bbox[2]/SCALE, self.bbox[1]/SCALE)
			dc.DrawLine(self.bbox[0]/SCALE, self.bbox[1]/SCALE, self.bbox[0]/SCALE, self.bbox[3]/SCALE)
			dc.DrawLine(self.bbox[2]/SCALE, self.bbox[3]/SCALE, self.bbox[0]/SCALE, self.bbox[3]/SCALE)
			dc.DrawLine(self.bbox[2]/SCALE, self.bbox[3]/SCALE, self.bbox[2]/SCALE, self.bbox[1]/SCALE)
			for word in div.children:
				#if word.children[0].isupper() or word.children[0] == u"-":			
				if True:
					dc.SetPen(wx.Pen("black", 1))
					height = (word.bbox[3]/SCALE - word.bbox[1]/SCALE)
					#width = (word.bbox[2]/SCALE - word.bbox[0]/SCALE)
					font = dc.GetFont()
					if height != 0:
						font.SetPixelSize((height, height))
					dc.SetFont(font)
					dc.DrawText(word.children[0], word.bbox[0]/SCALE, word.bbox[1]/SCALE)
					dc.SetPen(wx.Pen("red" if k == 3 else ("gray" if k == 2 else "green"), 1))
					dc.DrawLine(word.bbox[0]/SCALE, word.bbox[1]/SCALE, word.bbox[2]/SCALE, word.bbox[1]/SCALE)
					dc.DrawLine(word.bbox[0]/SCALE, word.bbox[1]/SCALE, word.bbox[0]/SCALE, word.bbox[3]/SCALE)
					dc.DrawLine(word.bbox[2]/SCALE, word.bbox[3]/SCALE, word.bbox[0]/SCALE, word.bbox[3]/SCALE)
					dc.DrawLine(word.bbox[2]/SCALE, word.bbox[3]/SCALE, word.bbox[2]/SCALE, word.bbox[1]/SCALE)
		return
	#def OnLeft(self, e):
	#	self.nextPage()
	#	self.ClearBackground()
	#	self.Draw()
	#	self.Refresh()
	#def OnRight(self, e):
	#	self.prevPage()
	#	self.ClearBackground()
	#	self.Draw()
	#	self.Refresh()

class PDFMinerTree:
	def __init__(self):
		self.bbox = None
		self.children = []

pages = []
page = None
current = None
text = u""
wordbb = None

class HumanReadableHandler(ContentHandler):
	global isText, current, page, pages, stack, wordbb, text
	isText = False
	stack = []
	def __clazz(self, attrs):
		try:
			title = attrs.getValue(u"class")
		except KeyError:
			return u"dummy"
		else:
			return title
	def __bbox(self, attrs):
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
	def startElement(self, name, attrs):
		global isText, current, page, pages, wordbb, text
		stack.append(self.__clazz(attrs))
		if self.__clazz(attrs) == u"ocr_page":
			page = PDFMinerTree()
			pages.append(page)
		elif self.__clazz(attrs) == u"ocrx_word":
			isText = True
			text = u""
			wordbb = self.__bbox(attrs)
		elif self.__clazz(attrs) == u"ocr_carea":
			#print "+---------------------------------------------------------+"
			#print "|                                                         |"
			#print attrs.getValue("bbox")
			current = PDFMinerTree()
			current.bbox = []
			current.bbox.append(self.__bbox(attrs)[0])
			current.bbox.append(self.__bbox(attrs)[1])
			current.bbox.append(self.__bbox(attrs)[2])
			current.bbox.append(self.__bbox(attrs)[3])
			page.children.append(current)
	def endElement(self, name):
		global isText, current, page, pages, wordbb
		clazz = stack.pop()
		if clazz == u"ocr_page":
			#print "::::::::::::::::::::: NOWA STRONA :::::::::::::::::::::"
			#page = PDFMinerTree()
			#pages.append(page)
			pass
		elif clazz == u"ocr_carea":
			pass
			#print "|                                                         |"
			#print "+---------------------------------------------------------+"
		#elif name == "textline":
			#print ""
		elif clazz == u"ocrx_word":
			word = PDFMinerTree()
			word.children.append(text)
			word.bbox = wordbb
			isText = False
			current.children.append(word)
	def characters(self, content):
		global isText, text
		if isText:
			text += content
			#sys.stdout.write(content.encode("utf-8"))

class MachineReadableHandler(ContentHandler):
	global isText
	isText = False
	def startElement(self, name, attrs):
		global isText
		if name == "text":
			isText = True
		elif name == "textbox":
			bbox = attrs.getValue("bbox").split(',')
			print "!!--BEGINT"
			print bbox[1]
			print bbox[3]
	def endElement(self, name):
		global isText
		if name == "page":
			print "!!--PAGEB"
		elif name == "textbox":
			print "!!--ENDT"
		#elif name == "textline":
			#print ""
		elif name == "text":
			isText = False
	def characters(self, content):
		global isText
		if isText:
			sys.stdout.write(content.encode("utf-8"))

ID_OWN_TEXT = wx.ID_HIGHEST + 1

class MainWindow(wx.Frame):
	global pages, current, page, pages
	def __init__(self, parent, title):
		global pages
		PATH = "/home/to/skrypt/skrypt/inne"
		wx.Frame.__init__(self, parent, title=title, size=(800, 600))
		self.CreateStatusBar()
		self.fileLoaded = False
		#filemenu = wx.Menu()
		#menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
		#menuNext = filemenu.Append(wx.ID_ANY, "&Next", "Next page")
		#menuBar = wx.MenuBar()
		#menuBar.Append(filemenu, "&File")
		self.preview = Preview(self, pages)
		#self.SetMenuBar(menuBar)
		#self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.GetStatusBar().SetStatusText(str(self.preview.i), 0)
		self.__toolbar = self.CreateToolBar()
		self.__toolbar.AddLabelTool(wx.ID_PREVIEW_PREVIOUS, "", wx.Bitmap(PATH + "/prev.png"))
		self.__pageNoCtrl = wx.TextCtrl(self.__toolbar, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
		self.__pageNoCtrl.SetSize((self.__pageNoCtrl.GetSize()[1] * 2.0, self.__pageNoCtrl.GetSize()[1]))
		self.__pageNoCtrl.SetValue("1")
		self.__maxPageNo = len(pages)
		self.__maxPageNoCtrl = wx.StaticText(self.__toolbar, wx.ID_ANY)
		self.__maxPageNoCtrl.SetLabel(" of " + str(len(pages)))
		self.__maxPageNoCtrl.SetSize((self.__maxPageNoCtrl.GetSize()[1] * 3.0, self.__maxPageNoCtrl.GetSize()[1]))
		self.__maxPageNoCtrl.SetBackgroundStyle(wx.TRANSPARENT)
		self.__toolbar.AddControl(self.__pageNoCtrl)
		self.__toolbar.AddControl(self.__maxPageNoCtrl)
		self.__toolbar.AddLabelTool(wx.ID_PREVIEW_NEXT, "", wx.Bitmap(PATH + "/next.png"))
		self.__toolbar.Realize()
		self.Bind(wx.EVT_TOOL, self.OnLeft, id=wx.ID_PREVIEW_NEXT)
		self.Bind(wx.EVT_TOOL, self.OnRight, id=wx.ID_PREVIEW_PREVIOUS)
		self.Bind(wx.EVT_TEXT_ENTER, self.__onEnter, self.__pageNoCtrl)
	def OnLeft(self, e):
		i = self.preview.nextPage()
		if i != None:
			self.__pageNoCtrl.SetValue(str(i + 1))
		self.preview.ClearBackground()
		self.preview.Draw()
		self.preview.Refresh()
	def OnRight(self, e):
		i = self.preview.prevPage()
		if i != None:
			self.__pageNoCtrl.SetValue(str(i + 1))
		self.preview.ClearBackground()
		self.preview.Draw()
		self.preview.Refresh()
	def __onEnter(self, event):
		pg = int(self.__pageNoCtrl.GetValue())
		if pg > 0 and pg < self.__maxPageNo + 1:
			self.preview.page(pg)
			self.preview.ClearBackground()
			self.preview.Draw()
			self.preview.Refresh()
	#def OnExit(self, e):
	#	self.Close(True)

def main(argv):
	global current, page, pages
	#if len(argv) > 2:
	#	if argv[2] == "-h":
	#		handler = HumanReadableHandler()
	#	else:
	#		handler = MachineReadableHandler()
	#else:
	#	handler = MachineReadableHandler()
	handler = HumanReadableHandler()
	saxparser = make_parser()
	saxparser.setContentHandler(handler)
	datasource = open(argv[1], 'r')
	saxparser.parse(datasource)
	#for p in pages:
	#	print "[", len(p.children), "]"
	#if argv[2] == "-h":
	if True:
		app = wx.App(False)
		frame = MainWindow(None, "Linde hOCR Browser")
		frame.Show(True)
		app.MainLoop()
	return

if __name__ == '__main__': sys.exit(main(sys.argv))

