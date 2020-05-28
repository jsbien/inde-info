# -*- coding: utf-8 -*-

import sys

# skrypt uwzglednia poprawki edycyjne
# wykomentowany fragment dodatkowo sluzyl do jednorazowego przenumerowania numerow w nawiasach klamrowych
# z 0..n-1 na 1..n
# check3 PLIK_WEJSCIOWY PLIK_WYNIKOWY
# reguly:
# - "_": zmieniamy na podhaslo - drugi czlon staje sie ostatnim haslem glownym
# - "=": drugi czlon staje sie taki sam jak pierwszy
# - bylo chyba zalozenie, ze "=" i "_" nie moga razem wystapic (bo "=" wystepuje tylko w haslach glownych)
#   wpp tez zadziala ("=" bedzie ignorowane w miejscach uzycia "_"), chyba ze haslo glowne na ktore zmieniamy
#   drugi czlon w wyniku uzycia "_" bedzie rowne oryginalnemu drugiemu czlonowi (wtedy "=" nadpisze "_")

def main(argv):
	fin = open(argv[1])
	fout = open(argv[2], "w")
	last = None
	for line in fin:
		if line == "\n":
			fout.write("\n")
			continue
		line = unicode(line.decode("utf-8"))
		els = line.split(u";")
		
		if (els[13] == els[14] or els[13].find(u"=") != -1) and els[13].find(u"_") == -1:
			last = els[13]
		
		if els[13].find(u"_") != -1:
			line = line.replace(els[13] + u";" + els[14], els[13] + u";" + last)
			line = line.replace(u"_", u"");
		
		if els[13].find(u"=") != -1:
			line = line.replace(els[13] + u";" + els[14], els[13] + u";" + els[13])
			line = line.replace(u"=", u"")
			last = line.split(u";")[13]
			
		
		'''if els[16] != u"[]\n":
			nums = els[16][1:-1].split(u"-")
			if nums[-1][-1] == u"]":
				nums[-1] = nums[-1][:-1]
			for i in range(0, len(nums)):
				try:
					nums[i] = unicode(int(nums[i]) + 1)
				except ValueError:
					print els[16] + u":" + unicode(str(nums)) + u":" + line
			res = u"[" + nums[0]
			for j in range(1, len(nums)):
				res += u"-" + nums[j]
			res += u"]"
			if els[16][-1] == u"\n":
				res += u"\n"
			line = line.replace(els[16], res)'''
		
		fout.write(line.encode("utf-8"))
	fout.close()

if __name__ == '__main__': sys.exit(main(sys.argv))

