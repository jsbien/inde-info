import os
import sys
from extract_entries import MyHandler, Word
from xml.sax import make_parser
from optparse import OptionParser

def lmb(el):
  try:
    (a, b, c) = el.split("-")
  except ValueError:
    return 0
  if a == "1": a = 10000
  elif a == "2": a = 20000
  elif a == "3": a = 30000
  elif a == "4": a = 40000
  elif a == "5": a = 50000
  elif a == "6a": a = 60000
  elif a == "6b": a = 70000
  return a + int(b)

def proceed(dirp):
  els = os.listdir(dirp)
  li = sorted(els, key=lmb)
  res = []
  tmp = []
  for el in li:
    if el.find(".html") != -1: res.append(el)
    if el.find("_real.html") != -1: tmp.append(el)
  for t in tmp:
    res.remove(t.replace("_real", ""))
  return res

def once(pageno, dirp, filen, fout, x, y, ignpags, pagebreak=True):
  handler = MyHandler()
  handler.setParameters(maxAfterWords=3)
  handler.setPageNo(pageno)
  for i in range(0, len(ignpags)):
    ignpags[i] += pageno - 1
  handler.setIgnPags(ignpags)
  if x != None:
    handler.setResolution(x, y)
  saxparser = make_parser()
  saxparser.setContentHandler(handler)
  datasource = open(dirp + "/" + filen, "r")
  saxparser.parse(datasource)
  for w in handler.getWords():
    fout.write((w.toString(humanReadable=False) + u"\n").encode("utf-8"))

def readignores():
  res = []
  f = open("ignores.txt")
  for l in f:
    if l == "\n":
      continue
    l = l[:-1]
    l = l.split(";")
    k = []
    k.append(l[0])
    tmp = []
    for i in l[1].split(","):
      tmp.append(int(i))
    k.append(tmp)
    res.append(k)
  f.close()
  return res

def main(argv):
  usage = "%prog [OPTIONS] INPUT_FILE OUTPUT_FILE"
  parser = OptionParser(usage = usage, version = "hej 0.1")
  parser.add_option("-r", "--resolution", help="djvu document resolution", dest="res", default=None)
  (options, args) = parser.parse_args(argv)
  fout = open(args[2], "w")
  if options.res != None:
    (resx, resy) = (int(options.res.split("x")[0]), int(options.res.split("x")[1]))
  else:
    (resx, resy) = (None, None)
  igns = readignores()
  for f in proceed(argv[1]):
    #if f.find("5-3211-3308") != -1:
    #  continue
    ignpags = []
    for ign in igns:
      if f.find(ign[0]) != -1:
        ignpags = ign[1]
        break
    pageno = int(f.split("-")[1])
    #print pageno, f, fout, resx, resy, ignpags
    once(pageno, argv[1], f, fout, resx, resy, ignpags)
  fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

