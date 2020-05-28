import os
import sys
from xml.dom import minidom
from shuffle import getElementsByClassName

PDFA_2_HOCR = "python /home/to/workspace/PDFAUtilities2/src/pdfa2hocr.py"
PAGINATION = "/home/to/workspace/PDFAUtilities2/src/pagina.py"
arr = [
	["FR10_Linde3_2127a-b2130", 2, 3, "3-2103-2162", 25, 26],
	["FR10_Linde3_2127a-b2130", 6, 7, "3-2103-2162", 29, 30], # 27, 28
	["FR10_Linde3_2143ab2144", 2, 3, "3-2103-2162", 45, 46], # 41, 42
	["FR10_Linde4_2883ab2884", 2, 3, "4-2837-2900", 53, 54],
	["FR10_Linde6-2_4365ab4366", 2, 3, "6b-4371-4378", 3, 4],
	["FR10_Linde6-2_4867a-b4870", 2, 3, "6b-4817-4902", 61, 62],
	["FR10_Linde6-2_4867a-b4870", 6, 7, "6b-4817-4902", 65, 66] # 63, 64
]

path = sys.argv[1]
expath = sys.argv[2]

for a in arr:
	if not os.path.exists(path + "/" + a[0] + ".html"):
		print PDFA_2_HOCR + " -p -i -c 2 -u pl_PL -l " + PAGINATION + " " + path + "/" + a[0] + ".pdf " + path + "/" + a[0] + ".html"
		os.system(PDFA_2_HOCR + " -p -i -c 2 -u pl_PL -l \"" + PAGINATION + "\" \"" + path + "/" + a[0] + ".pdf\" \"" + path + "/" + a[0] + ".html\"")
	f = open(path + "/" + a[0] + ".html")
	if os.path.exists(expath + "/" + a[3] + "_real.html"):
		g = open(expath + "/" + a[3] + "_real.html")
	else:
		g = open(expath + "/" + a[3] + ".html")
	indom = minidom.parse(f)
	outdom = minidom.parse(g)
	inbody = indom.getElementsByTagName("body")[0]
	outbody = outdom.getElementsByTagName("body")[0]
	pages = outbody.childNodes
	i = 0
	for pag in inbody.childNodes:
		i += 1
		if i == a[1]:
			pages.insert(a[5] - 1, pag)
		if i == a[2]:
			pages.insert(a[5], pag)
	f.close()
	g.close()
	newf = open(expath + "/" + a[3] + "_real.html", "w")
	newf.write(outbody.toxml().encode("utf-8"))
	newf.close()

