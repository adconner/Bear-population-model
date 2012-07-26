videoout=out.avi
timeFile=timeintervals.data
picfolder=outfiles
picbase=pic
remake=.remake
fps=1

all: eqs.pdf

vid: $(videoout)

eqs.pdf: eqs.tex
	pdflatex $<

$(videoout): $(remake)
	mencoder "mf://$(picfolder)/*.png" -ovc lavc -mf fps=$(fps) -o $(videoout)

$(remake):
	touch $(remake)
