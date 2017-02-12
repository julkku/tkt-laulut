#!/bin/bash
python3 to_latex.py ordering.csv lyrics.csv > laulut.tex && \
pdflatex laulukirja.tex && \
pdflatex laulukirja.tex && \
pdflatex laulukirja.tex
