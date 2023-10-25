#!/usr/bin/python

def get_word_list(fileName):
  file = open(fileName, "r")
  lines = file.readlines()
  file.close()
  print(lines)


get_word_list("Halloween words and puns - Sheet1.csv")