#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Autor: Jan Chęć (277635)
# Licencja: Creative Commons 3.0 CC-BY (uznanie autorstwa)
# Wersja: 1.1

def downloadDescription(word):
  """
  Downloads from Linde's Dictionary of Polish (Wikisources) description
  of given word. Description is a large unicode string, which is returned.
  
  word -- Word to get the description.

  If the given word isn't a string, it raises a ValueError.
  >>> downloadDescription(5)
  Traceback (most recent call last):
    ...
  ValueError: word must be a string
  >>> downloadDescription(dict())
  Traceback (most recent call last):
    ...
  ValueError: word must be a string

  If the given word is empty - it raises a ValueError.
  >>> downloadDescription('')
  Traceback (most recent call last):
    ...
  ValueError: word must be nonempty
  """
  # Checking for errors
  if type(word) != type("") and type(word) != type(u""):
    raise ValueError("word must be a string")
  if len(word) < 1:
    raise ValueError("word must be nonempty")

  # Getting description page from the Internet
  import urllib2, string

  url = u"http://pl.wikisource.org/wiki/SJP:" + unicode.upper(word)
  #print u"Going into: " + url
  request = urllib2.Request(url.encode('UTF-8'))
  request.add_header('User-Agent', 'OpenAnything/7.9')
  opener = urllib2.build_opener()
  page = opener.open(request)

  pageText = page.read()

  # Cropping out description
  tables = pageText.split("<table>")[1:]
  tables = string.join(tables, "<table>")
  body = tables.split("<!--")[0]

  body = body.split("</table>")[:-1]
  body = string.join(body, "</table>")

  # Cropping out overlaying dull table
  import re
  body = re.sub("<tr>\W*<td valign=\"top\">\W*<div style=\"[\w\-:; \"]*>\W*<div>",
      "", body)
  body = re.sub("(</div>\W*){2}</td>\W*</tr>", "", body)

  # Transforming paragraphs
  #paras = body.split("<p>")[1:]

  finDescription = ""

  """
  for body in paras:
    # Omitting <span>*</span>
    spans = body.split("<span>")
    description = ""
    for span in spans:
      description += span.split("</span>")[-1]

    # Removing links
    links = description.split("<a href")
    description = links[0]
    for link in links[1:]:
      rest = link.split(">")[1:]
      rest = string.join(rest, ">")
      middle = string.replace(rest, "</a>", "")
      description += middle

    description = description.split("</div>")[0]
    finDescription += string.replace(description, "</p>", "\n\n")
  """
  finDescription = body
  finDescription = re.sub("</?p>", "\n\n", finDescription)

  # Transforming <dl><dd>*</dd></dl> into quoted text
  finDescription = finDescription.replace('<dl>', "\\begin{quote}")
  finDescription = re.sub("</?dd>", "", finDescription)
  finDescription = finDescription.replace('</dl>', "\\end{quote}\n\n")


  return finDescription

