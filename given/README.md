There are three python programs here (`-h` for usage):

-`./align` aligns words.

-`./check-alignments` checks that the entire dataset is aligned, and
  that there are no out-of-bounds alignment points.

-`./score-alignments` computes alignment error rate.

The commands work in a pipeline. For instance:

   > ./align -t 0.9 -n 1000 | ./check | ./grade -n 5

The `data` directory contains a fragment of the Canadian Hansards,
aligned by Ulrich Germann:

-`hansards.e` is the English side.

-`hansards.f` is the French side.

-`hansards.a` is the alignment of the first 37 sentences. The 
  notation i-j means the word as position i of the French is 
  aligned to the word at position j of the English. Notation 
  i?j means they are probably aligned. Positions are 0-indexed.
  
---------------------------------------------------------------- 
Startbefehl 
$ python Model1.py

Optionale Kommandos
-d  --data				default= ”data/hansards”	Prefix des Daten-Dateinamens
-e 	–-english			default= ”e”				Suffix der Englisch-Datei
-f 	–-french			default= ”f”				Suffix der Franzoesisch-Datei
-t 	–-threshold			default= 0.2				Schwellenwert
-l 	–-loop				default= 3					Anzahl der Iterationen
-n  -–num sentences   	default=1000				Anzahl der Saetze

$ python Model1.py -l 5 -t 0.5

Befehl zum Scoren der Alignments MIT Speicherung der Alignments
$ python Model1.py -l 5 -t 0.5 > out.txt
$ python score-alignments < out

Befehl zum Scoren der Alignments OHNE Speicherung der Alignments
$python Model1.py -l 5 -t 0.5 — python score-alignments