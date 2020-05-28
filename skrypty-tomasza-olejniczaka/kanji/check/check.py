# encoding=UTF-8

import os
import sys

def do(path):
	for f in os.listdir(path):
		if os.path.isdir(f):
			do(path + "/" + f)
		elif f[-4:] == ".xml":
			os.system("python pageassert -F hocr " + path + "/" + f)

do(sys.argv[1])

