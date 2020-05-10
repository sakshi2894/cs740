# Makefile for SenSys '03 submission
# $Id: Makefile,v 1.1.1.1 2009/04/03 00:43:07 msaxena Exp $

LATEX   = pdflatex
BIBTEX  = bibtex
METAPOST= mpost
PIC     = pic
JGRAPH  = jgraph

PICOPTS = -t

MAINFILE= paper
TEXSRCS	= paper.tex 
PICSRCS	= 
FIGS    = 
JSRCS   = 
PPTS    = 

all: $(MAINFILE).pdf
	$(LATEX) $(MAINFILE)
	$(BIBTEX) -min-crossrefs=100 $(MAINFILE)
	$(LATEX) $(MAINFILE)
	$(LATEX) $(MAINFILE)

paper.pdf: *.tex *.bib
	$(LATEX) paper
	$(BIBTEX) -min-crossrefs=100 paper
	$(LATEX) paper
	$(LATEX) paper

fast:
	$(LATEX) paper

clean:
	rm -f *.dvi *.aux *.log *.blg *.bbl $(MAINFILE).ps $(PICSRCS) $(FIGS) \
	fig/*.log fig/*.aux fig/*.dvi fig/*.mpx *.tmp $(SLIDES).ps $(JSRCS)
