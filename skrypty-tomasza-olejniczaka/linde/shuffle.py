from xml.dom import minidom

def getElementsByClassName(dom, clazz, where):
	res = []
	nodes = dom.getElementsByTagName(where)
	for n in nodes:
		if n.getAttribute("class") == "ocr_page":
			res.append(n)
	return res

def pageno(node):
	title = node.getAttribute("title")
	els = title.split(";")
	for e in els:
		if e.find("pageno") != -1:
			return int(e.lstrip().split(" ")[1])

f = open("linde-pdf/1-321-404.html")
dom = minidom.parse(f)
pages = getElementsByClassName(dom, "ocr_page", "div")
pages = sorted(pages, key=pageno, reverse=True)
ln = len(pages) - 1
i = 0
for node in pages:
	new = node.getAttribute("title").replace("pageno " + str(ln), "pageno " + str(i))
	node.removeAttribute("title")
	node.setAttribute("title", new)
	#print new, ln, i
	i += 1
	ln -= 1
	#print node.getAttribute("title").replace("pageno " + str(ln), "pageno " + str(i))
	#print node.getAttribute("title")
body = dom.getElementsByTagName("body")[0]
while body.hasChildNodes(): body.removeChild(body.lastChild)
for p in pages:
	body.appendChild(p)
f.close()
f = open("linde-pdf/1-321-404_real.html", "w")
f.write(dom.toxml().encode("utf-8"));
f.close();

