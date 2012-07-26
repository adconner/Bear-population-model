videoout=bearpop.avi
fps = 46

timefile=timeintervals.data
picfolder=outfiles
picbase=pic

remake=.remake

all: eqs.pdf

vid: $(videoout)

eqs.pdf: eqs.tex
	pdflatex $<

$(videoout): $(remake)
	mencoder "mf://$(picfolder)/*.png" -ovc copy -mf fps=$(fps) -o $(videoout)

$(remake):
	touch $(remake)
