#!/usr/bin/env python

# Le Duyen Sandra Vu
# 768693
# Model1.py
# 
# CLT Programmierprojekt WiSe 15/16
# IBM Model 1 und EM-Algorithmus Implementierung 
# 
#
# Python Version 2.7.10
# MacOS 10.11.1
#
# Kommandozeilen-Optionen, DatenGenerierung und Print-Funktion wurden von 
# Adam Lopez <alopez@cs.jhu.edu> uebernommen und minimal angepasst

import optparse							# parser fuer die Kommandozeile
import sys								# fuer die Standard-Datenstroeme std::in, out, err
from collections import defaultdict		# erstellt Item falls nicht existent 

# zusaetzliche Befehl-Optionen in der Kommandozeile
optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.2, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-l", "--loop", dest="loop_nr", default=3, type="int", help="number of loops (default=3)")
optparser.add_option("-n", "--num sentences", dest="num_sents", default=1000, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)

########################
# get Data
########################
# Es wird zwischen std::err und std::out unterschieden,
# da nur die Alignments in die Datei geschrieben werden sollen.
# Der Rest geht in den std::err Kanal.

sys.stderr.write("Training with IBM Model 1...")
# bitext: [ [fr Woerter (Satz)]  [eng Woerter (Satz)] ], [...]
# ingesamt 100.000 Saetze
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
 

########################
# Initialisierung
########################

t = defaultdict(float) 		# t[(e, f)]

# uniformly initialize all probablilities
for (f_sent, e_sent) in bitext:
  e_sent.append("NULL")
  for e in set(e_sent):
    for f in set(f_sent):
      t[(e, f)] = 1.0		# auch moeglich: 1/len(f_words)


########################
# EM
########################

# Umso mehr loops, umso aussagekraeftigere Werte
for x in xrange(opts.loop_nr):
	# set count(e|f) to 0 for all e,f
	# set total(f) to 0 for all f
	count = defaultdict(float) 		# count[(e, f)]
	total = defaultdict(float)		# total[f]
	total_s = defaultdict(float)	# total_s[e]

	# for all sentence pairs (f_s,e_s)
	for (f_sent, e_sent) in bitext:
		
		# COMPUTE NORMALIZATION
		# for all words e in e_s
		for e in e_sent:
			# total_s = 0 - wird fuer jedes e auf 0 zurueck gesetzt
			# [e] Abhaengigkeit ist nicht zwangslaeufig notwendig
			# wird aber zum collecten aller e genutzt (fuer spaeter)
			total_s[e] = 0.0
			# for all words f in f_s
			for f in f_sent:
				# total_s += t(e|f)
				total_s[e] += t[(e, f)]

		# COLLECT COUNTS
		# for all words e in e_s
		for e in e_sent:
			# for all words f in f_s
			for f in f_sent:
				# count(e|f) += t(e|f) / total_s
				# total(f) += t(e|f) / total_s
				count[(e, f)] += t[(e, f)] / total_s[e]
				total[f] += t[(e, f)] / total_s[e]
				
	# ESTIMATE PROBABILITIES			
	# for all f in domain( total(.) ) 
	# bzw. for all foreign words f do
	for f in set(total):
		# for all e in domain( count(.|f) ) 
		# bzw. for all English words e do
		for e in set(total_s):
			# t(e|f) = count(e|f) / total(f) 
			t[(e, f)] = count[(e, f)] / total[f]	

########################
# print
########################
for (f_sent, e_sent) in bitext:
	for (i, f) in enumerate(f_sent):
	  	for (j, e) in enumerate(e_sent):
			if t[(e, f)] > opts.threshold:
				sys.stdout.write("%i-%i " % (i,j))
    	sys.stdout.write("\n")