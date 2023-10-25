#!/usr/bin/python

def get_word_list(fileName):
  lines = []
  with open(fileName, "r") as file:
    lines = file.readlines()
    file.close()
  
  print(lines)


get_word_list("HalloweenPhrases.csv")