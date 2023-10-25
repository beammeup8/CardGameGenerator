#!/usr/bin/python

def get_word_list(fileName):
  lines = []
  with open(fileName, "r") as file:
    txt = file.read()
    file.close()
    lines = txt.splitlines()
  print(lines)


get_word_list("HalloweenPhrases.csv")