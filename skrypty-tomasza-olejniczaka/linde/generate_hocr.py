import os

scopes = [(2369, 2479), (133, 813), (835, 1515), (1535, 2162), (2177, 2899), (2921, 3666),	(3751, 4358), (4365, 4899)]
todos = [
	["Linde3_1-349_OCRonly.pdf", 1521, 1869],
	["Linde3_350-end_OCRonly.pdf", 1870, 2164],
	["Linde4_OCRonly.pdf", 2163, 2906], # -= 2
	["Linde5_OCRonly.pdf", 2907, 3672],
	["Linde6-1_OCRonly.pdf", 3673, 4358],
	["Linde6-2_OCRonly.pdf", 4359, 4914]
]

PDFA_2_HOCR = "python /home/to/workspace/PDFAUtilities2/src/pdfa2hocr.py"
PAGINATION = "/home/to/workspace/PDFAUtilities2/src/pagina.py"

igndump = True

j = 0
for el in todos:
	#print el
	j += 1
	#if j != 3: continue
	lenel = el[2] - el[1] + 1
	ign = []
	for i in range(0, lenel):
		stop = False
		for (a, b) in scopes:
			if el[1] + i >= a and el[1] + i <= b:
				ign.append(True)
				stop = True
				break
		if stop:
			continue
		ign.append(False)
	ignstr = ""
	for i in range(0, lenel):
		if not ign[i]:
			ignstr += "," + str(i + 1)
	if len(ignstr) > 0:
		ignstr = " -g " + ignstr[1:]
		if igndump:
			print str(el[1]) + "-" + str(el[2]) + ";" + ignstr[4:]
			continue
	os.system(PDFA_2_HOCR + " -i -u pl_PL -p -l " + PAGINATION + ignstr + " -c 2 " + "Desktop/lindenew/" + el[0] + " Desktop/lindenew/" + str(el[1]) + "-" + str(el[2]) + ".html")

