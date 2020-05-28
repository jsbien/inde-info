import os
import sys
from extract_entries import MyHandler, Word
from xml.sax import make_parser
from optparse import OptionParser

def lmb(el):
  try:
    (a, b) = el.split(".")[0].split("-")
    return int(a)
  except ValueError:
    return 0

def proceed(dirp):
  els = os.listdir(dirp)
  li = sorted(els, key=lmb)
  res = []
  for el in li:
    if el.find(".html") != -1: res.append(el)
  return res

outfiles = [
  ["Linde3_OCRonly.djvu", 1521, 2164],
  ["Linde4_OCRonly.djvu", 2165, 2906], # strona 2165 to 3 strona pliku - dwie pierwsze sa nadmiarowe (nie bylo ich w starych skanach)
  ["Linde5_OCRonly.djvu", 2907, 3672],
  ["Linde6-1_OCRonly.djvu", 3673, 4358],
  ["Linde6-2_OCRonly.djvu", 4359, 4914]
]

def once(pageno, dirp, filen, fout, x, y, ignpags, pagebreak=True):
  global outfiles
  handler = MyHandler()
  handler.setParameters(maxAfterWords=3)
  handler.setPageNo(pageno)
  handler.setOutFiles(outfiles)
  for i in range(0, len(ignpags)):
    ignpags[i] += pageno - 1
    #print ignpags[i]
  #return
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
  f = open("ignores2.txt")
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
  parser = OptionParser(usage = usage, version = "hej2 0.1")
  parser.add_option("-r", "--resolution", help="djvu document resolution", dest="res", default=None)
  (options, args) = parser.parse_args(argv)
  fout = open(args[2], "w")
  if options.res != None:
    (resx, resy) = (int(options.res.split("x")[0]), int(options.res.split("x")[1]))
  else:
    (resx, resy) = (None, None)
  igns = readignores()
  for f in proceed(argv[1]):
    ignpags = []
    for ign in igns:
      if f.find(ign[0]) != -1:
        ignpags = ign[1]
        break
    pageno = int(f.split("-")[0])
    #print pageno, f, fout, resx, resy, ignpags
    once(pageno, argv[1], f, fout, resx, resy, ignpags)
  fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

