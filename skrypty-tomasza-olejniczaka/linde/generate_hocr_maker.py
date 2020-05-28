import os
import sys

# (4365, 4902)
scopes = [(2369, 2479), (133, 813), (835, 1515), (1535, 2162), (2177, 2899), (2921, 3666),	(3751, 4358), (4365, 4899)]

#mapp = {"linde1": 0, "line1b": 222, "linde2": 222 + 594}

#special = {813: 500, 1515: 500}

forceIgnore = [(3211, 3308)]

PDFA_2_HOCR = "python /home/to/workspace/PDFAUtilities2/src/pdfa2hocr.py"
PAGINATION = "/home/to/workspace/PDFAUtilities2/src/pagina.py"

#def _(i):
#	return i

igndump = False

def generateHOCR(vol, fromm, too, filen):
	global igndump
	def _(i):
		#if (vol == "6b" and i == 4869 + 6 + 2 + 2 + 2):
		#	return -1
		#if (vol == "6b" and i == 4867 + 6 + 2 + 2):
		#	return -1
		#if (vol == "6b" and i == 4365 + 6 + 2):
		#	return -1
		#if (vol == "4" and i == 2883 + 6):
		#	return -1
		#if (vol == "3" and i == 2143 + 4):
		#	return -1
		#if (vol == "3" and i == 2129 + 2):
		#	return -1
		#if (vol == "3" and i == 2127):
		#	return -1
		if vol > "6b" or (vol == "6b" and i > 4869 + 6 + 2 + 2 + 2):
			return i + 14
		if vol > "6b" or (vol == "6b" and i > 4867 + 6 + 2 + 2):
			return i + 12
		#if vol > "6b" or (vol == "6b" and i > 4363 + 6 + 2):
		if vol > "6b" or (vol == "6b" and i > 4365 + 6 + 2):
			return i + 10
		#if vol > "4" or (vol == "4" and i > 2831 + 6):
		if vol > "4" or (vol == "4" and i > 2883 + 6):
			return i + 8
		#if vol > "3" or (vol == "3" and i > 2103):
		if vol > "3" or (vol == "3" and i > 2143 + 4):
			return i + 6
		if vol > "3" or (vol == "3" and i > 2129 + 2):
			return i + 4
		if vol > "3" or (vol == "3" and i > 2127):
			return i + 2
		return i
	#print vol, fromm, too, a
	ign = []
	fromi = 1
	toi = too - fromm + 1
	
	for i in range(fromi, toi + 1):
		stop = False
		for (a, b) in scopes:
			if _(fromm - 1 + i) >= a and _(fromm - 1 + i) <= b:
				#if vol == "3" and fromm == 2157:
				#	print ":::", i, _(fromm - 1 + i), _(a), _(b)
				#	print ":::", fromm - 1 + i, a, b
				ign.append(True)
				stop = True
				break
		if stop:
			continue
		#if vol == "3" and fromm == 2157:
		#	print i, _(fromm - 1 + i), _(a), _(b)
		#	print fromm - 1 + i, a, b
		ign.append(False)
	
	#ts = 0
	#fs = 0
	#for el in ign:
	#	if el: ts += 1
	#	else: fs += 1
	#print ts, fs
	#return

	ignstr = ""
	oll = True
	for i in range(fromi, toi + 1):
		if not ign[i - 1]:
			ignstr += "," + str(i)
		else:
			oll = False
	if oll:
		#print "oj"
		return
	if len(ignstr) > 0:
		ignstr = " -g " + ignstr[1:]
		if igndump:
			print vol + "-" + str(_(fromm)) + "-" + str(_(too)) + ";" + ignstr[4:]
			return
	if igndump:
		return
	#print ignstr
	#return
	#print fromm, too, _(fromm), _(too), ignstr
	filen2 = vol + "-" + str(_(fromm)) + "-" + str(_(too))
	print "echo '" + PDFA_2_HOCR + " -p -i -c 2 -u pl_PL -l " + PAGINATION + ignstr + " " + filen + " " + filen2 + ".html" + "'"
	print "echo '" + PDFA_2_HOCR + " -p -i -c 2 -u pl_PL -l " + PAGINATION + ignstr + " " + filen + " " + filen2 + ".html" + "' > /dev/stderr"
	print PDFA_2_HOCR + " -p -i -c 2 -u pl_PL -l " + PAGINATION + ignstr + " " + filen + " " + filen2 + ".html"
	#if vol == "3": print _(fromm), _(too)
	#exit()
	#os.system(PDFA_2_HOCR + " -p -i -u pl_PL -l " + PAGINATION + ignstr + " " + filen + " " + filen2 + ".html")

i = 0

if len(sys.argv) > 2:
	if (sys.argv[2]) == "-i":
		igndump = True

for f in os.listdir(sys.argv[1]):
	i += 1
	name = f.split(".")
	#print f, name[0]
	if f.find("pdf") == -1:
		continue
	(vol, fromm, too) = name[0].split("-")
	fromm = int(fromm)
	too = int(too)
	generateHOCR(vol, fromm, too, f)

	#if i == 5:
		#exit()

