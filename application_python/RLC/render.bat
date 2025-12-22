quarto render --output-dir _build
shinylive export _build _site
py -m http.server --directory _site --bind localhost 8008