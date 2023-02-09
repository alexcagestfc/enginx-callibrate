"""
enginx-callibrate
program will load experiment and analyse for offset


CSB1 contains all functions called upon
  I'd suggest reading through the code, explanations are provided and requirements explained
example of usage is provided
info is extracted from summary.ext

previous changes and observations:
code was designed around north bank analysis, south bank offsets tend to be negative. I'm uncertain as to if the bank is negativly displaced in reality or if it is a bug

pending additions and fixes:
  additional flexibility in detector sets for compared analysis of specific areas
  
  selecting for experiments with particular columnators. This should be pretty easy, I already have code that can select experiments from particualr substrings 

"""
