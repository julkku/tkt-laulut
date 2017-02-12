all: laulukirja.pdf

.PHONY: clean
clean:
	git clean -fx

laulukirja.pdf: laulukirja.tex laulut.tex
	pdflatex laulukirja.tex && \
	pdflatex laulukirja.tex && \
	pdflatex laulukirja.tex

laulut.tex: lyrics.csv ordering.csv
	python3 to_latex.py ordering.csv lyrics.csv > laulut.tex
