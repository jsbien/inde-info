(TeX-add-style-hook
 "J-etap6bdb"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("footmisc" "para")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art12"
    "fontspec"
    "graphicx"
    "hyperref"
    "footmisc")
   (TeX-add-symbols
    '("wikiq" 2)
    '("subentry" 2)
    '("quoteref" 1)
    '("showimage" 1)
    '("pos" 2)
    '("mainentrypageend" 1)
    '("mainentryend" 1)
    '("mainentrybegin" 2)
    '("mainentry" 2)
    '("gram" 1)
    '("fraktur" 1)
    '("doh" 1)
    '("entryref" 2)
    '("entry" 2)
    '("abbrev" 2)
    '("marginlabel" 1)))
 :latex)

