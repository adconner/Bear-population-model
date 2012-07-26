all: eqs.pdf

eqs.pdf: eqs.tex
	pdflatex $<
