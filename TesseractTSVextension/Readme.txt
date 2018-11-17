The data in this directory contain in particular the simulation of the
extended TSV output (just a fragment of a page from Linde's
dictionary).

$ tesseract --version
tesseract 4.0.0
 leptonica-1.76.0
  libgif 5.1.4 : libjpeg 6b (libjpeg-turbo 1.5.2) : libpng 1.6.34 : libtiff 4.0.9 : zlib 1.2.11 : libwebp 0.6.1 : libopenjp2 2.3.0
 Found AVX2
 Found AVX
 Found SSE
 
$ TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata/ tesseract  000142.tif Linde142 --oem 0 -l deu_frak+pol tsv4linde
Tesseract Open Source OCR Engine v4.0.0 with Leptonica
Page 1

$ TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata/ tesseract  000142.tif Linde142 --oem 0 -l deu_frak+pol hocr4linde
Tesseract Open Source OCR Engine v4.0.0 with Leptonica
Page 1 

Please note strange discrepancies of bounding boxes in hocr and tsv!
