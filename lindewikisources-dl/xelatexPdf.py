#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Autor: Jan Chęć (277635)
# Licencja: Creative Commons 3.0 CC-BY (uznanie autorstwa)
# Wersja: 1.1

FONT = 'Linux Libertine O'

def generateXelatex(dictionary):
  """
  Prints dictionary to XeLaTeX and returns this as a string ready
  to write to a file.
  
  dictionary -- Pairs word+description

  >>> generateXelatex(5)
  Traceback (most recent call last):
    ...
  ValueError: dictionary must be a list
  """
  # Error checking
  if type(dictionary) != type([]):
    raise ValueError("dictionary must be a list")

  # Initializing document
  xelatex = u'''
\\documentclass[11pt]{book}
\\usepackage{xltxtra}
\\usepackage{supertabular}
\\setmainfont[Mapping=tex-text]{%s}
\\setcounter{secnumdepth}{0}
\\renewcommand*\\contentsname{Spis treści}
\\begin{document}
\\title{Słownik}
\\date{}
\\maketitle
\\cleardoublepage
''' % (FONT)


  # Processing dictionary
  import string, re
  for word, desc in dictionary:
    word = word.replace('_', ' ')
    xelatex += u'\n\n\section{' + word + u'}'

    # Transforming description
    texDesc = desc

    # Dealing with double <span> on page anchors
    #texDesc = re.sub("(<span[\# \w=\"-;]*>){2}\[<b><a[\# \w=\"-;/]*>\w*</a></b>\](</span>){2}",
    #    "", texDesc)
    texDesc = re.sub("(<span[\# \w=\"-;]*>){2}\[<b><a[\# \w=\"-;/.\?]*>\w*</a></b>\](</span>){2}",
        "", texDesc)

    # Cropping tail for some pages
    texDesc = texDesc.split('<a href="/w/index.php?title=Strona:')[0]
    #print texDesc

    # Removing <sup>, <a>, <div>, <span>
    texDesc = re.sub("</?((sup)|(a)|(div)|(span))[\# \w=\"-:;]*>", "", texDesc)

    # Additional replaces
    replaces = [('<i>', '\emph{'), ('</i>', '}'), ('<b>', '\\textbf{'),
        ('</b>', '}'), ('<br />', "\n"), ('<center>', ''),
        ('</center>', '\n\n'), ('amp;', '')]

    for old, new in replaces:
      texDesc = texDesc.replace(old, new)

    # Dealing with <tt><small>*</small></tt>
    texDesc = texDesc.replace('<tt><small>', "{\\tt \\small ")
    texDesc = texDesc.replace('</small></tt>', "}")

    # Dealing with <tt> alone.
    texDesc = texDesc.replace('<tt>', "{\\tt ")
    texDesc = texDesc.replace('</tt>', "}")

    # Replacing bad sign &#160; (non-breakable space) to LaTeX
    # legal equivalent "~"
    texDesc = texDesc.replace("&#160;", '~')

    # Replacing &gt; and &lt; to LaTeX legal equivalents
    texDesc = texDesc.replace("&gt;", '>')
    texDesc = texDesc.replace("&lt;", '>')

    # Escaping ampersand 
    texDesc = texDesc.replace('&', '\&')

    # Dealing with tables
    texDesc = re.sub('<table[\# \w=\"-:;]*>',
        "\\\\begin{supertabular}{l l}\n", texDesc)
    texDesc = re.sub('<tr[\# \w=\"-:;]*>', "\n", texDesc)
    texDesc = re.sub('</td>\s*<td[\# \w=\"-:;]*>', " & ", texDesc)
    texDesc = re.sub('<td[\# \w=\"-:;]*>', "", texDesc)
    texDesc = texDesc.replace('</td>', "")
    texDesc = texDesc.replace('</tr>', "\\\\\n")
    texDesc = texDesc.replace('</table>', "\\end{supertabular}\n")

    # Removing too nested quotes
    texDesc = re.sub("(\\\\begin\{quote\}\s*){3}", "\\\\begin{quote}\n\n",
        texDesc)
    texDesc = re.sub("(\\\\end\{quote\}\s*){3}", "\end{quote}\n\n",
        texDesc)


    #print texDesc
    xelatex += u'\n\n' + unicode(texDesc, "UTF-8")


  # Adding foot
  xelatex += u'''
\\cleardoublepage
\\tableofcontents

\\end{document}
'''

  return xelatex

def printToFile(xelatex, filename):
  f = open(filename, 'w')
  xelatex = xelatex.encode("UTF-8")
  f.write(xelatex)
  f.close()

def makePDF(texFileDir):
  """
  Executing shell command to convert .tex -> .pdf
  
  texFileDir -- directory of .tex file (string)


  If the given texFileDir isn't a string, it raises a ValueError.
  >>> makePDF(5)
  Traceback (most recent call last):
    ...
  ValueError: texFileDir must be a string
  >>> makePDF(dict())
  Traceback (most recent call last):
    ...
  ValueError: texFileDir must be a string

  If the given texFileDir is empty - it raises a ValueError.
  >>> makePDF('')
  Traceback (most recent call last):
    ...
  ValueError: texFileDir must be nonempty
  """
  if type(texFileDir) != type("") and type(texFileDir) != type(u""):
    raise ValueError("texFileDir must be a string")
  if len(texFileDir) < 1:
    raise ValueError("texFileDir must be nonempty")

  import subprocess

  returnCode = subprocess.call(["xelatex", texFileDir, "-halt-on-error"])
  return returnCode
