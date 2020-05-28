Program: xelatex.py
Autor: Jan Chęć (277635)
Licencja: Creative Commons 3.0 CC-BY (uznanie autorstwa)


Wymagania:
  Linuksowa konsola ustawiona na UTF-8

  Python 2.6 (stabilny)

  XeLaTeX z pakietem "xkeyval.sty"
    Przykładowo z paczek texlive-xetex + texlive-latex-recommended.

  Połączenie z internetem

  Font "Linux Libertine"
    Przykładowo z paczki ttf-linux-libertine. W razie konieczności podmiany - wystarczy zamienić "Linux Libertine 0" w jednej z pierwszych linii kodu "xelatexPdf.py" na pożądaną nazwę.


Opis:
  Program xelatex.py służy do ściągania podanych przez użytkownika haseł z zasobów słowika Samuela Linde udostępnionych na Wikisources i umieszczania ich w pliku XeLaTeX'owym. Następnie program kompiluje ów plik do formatu .pdf.

  W razie nieistnienia podanego hasła w zbiorach Wikisources, program wypisze stosowny komunikat.

  Działanie jest dwustopniowe - najpierw odbywa się zbieranie pożądanych haseł z wejścia, od użytkownika. Następnie program przechodzi do ściągania haseł, tworzenia pliku .tex oraz .pdf.


Wejście:
  Lista haseł, jedno na linię.


Wyjście:
  Plik "slownik.tex" oraz "slownik.pdf", zawierające ściągnięte hasła.


Użytkowanie:
  Podstawowa komenda:
    ./xelatex.py

    Uruchomienie programu w ten sposób skutkuje odpytaniem użytkownika o słowa, jakie chce ze słownika pobrać i umieścić w generowanym słowniku.
    Jedna fraza na linię.
    Pełne instrukcje są wypisywane na ekranie.
    Kończenie wpisywania zaznacza się wciśnięciem Ctrl-D.

  Wygodna wariacja:
    ./xelatex.py < plikZHasłami.txt

    Wystarczy w pliku .txt zapisać hasła, jedno na linię, a wywołanie programu odbędzie się bez interwencji użytkownika.

  Tylko .tex:
    ./xelatex.py --tex-only
    
    Nie generuje pliku .pdf, jedynie plik .tex

Umieszczone testy:
  Pliki tekstowe z hasłami z pierwszych 4 stron są umieszczone w plikach:
    strona90.txt
    strona91.txt
    strona92.txt
    strona93.txt
  Oraz plik łączący wszystkie poprzednie:
    strony90-93.txt

  Aby je wykorzystać, należy użyć drugiej metody z działu "Użytkowanie". Na przykład:
    ./xelatex.py < strona93.txt
