#!/usr/bin/python

from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import math


FONT_SIZE = 18
ROW_COUNT = 4
COL_COUNT = 2

TABLE_STYLE_START = (0,0)
TABLE_STYLE_END = (-1,-1)
IMAGE_SCALE = 0.8

def get_word_list(fileName, hasHeader, addNewLines):
  lines = []
  with open(fileName, "r") as file:
    txt = file.read()
    file.close()
    lines = txt.splitlines()
  if hasHeader:
    lines = lines[1:]

  if addNewLines:
    lines = [line.replace(" (", "<br/>(") for line in lines]
  
  return lines

def fill_out_list(words):
  # Makes sure the final column is always full 
  # by adding spare cards that can be filled in later
  per_page = COL_COUNT * ROW_COUNT
  words.extend([''] * (per_page - (len(words) % per_page)))
  return words

def output_pdf(words, picture, newFileName):

  doc = SimpleDocTemplate(newFileName, pagesize=letter)
  x,y = letter

  if picture:
    a = Image(picture, (IMAGE_SCALE*x)/COL_COUNT, (IMAGE_SCALE*y)/ROW_COUNT)  

  elements = []
  data = []
  page_entry = ROW_COUNT * COL_COUNT
  style = ParagraphStyle(
    name='Normal',
    fontSize=FONT_SIZE,
    alignment=TA_CENTER,
    leading=FONT_SIZE
  )
  
    
  words = fill_out_list(words)
  
  for i in range(0, len(words), COL_COUNT):
    # add the card backs where needed
    if picture and i % page_entry == 0 and i != 0:
      for j in range(ROW_COUNT):
        data.append([a for k in range(COL_COUNT)])
    # add the current row of words
    data.append([Paragraph(words[i+k], style) for k in range(COL_COUNT)])

  # add the pictures for the page
  if picture:
    for j in range(ROW_COUNT):
      data.append([a for k in range(COL_COUNT)])
  
  t=Table(data, x/COL_COUNT, y/(ROW_COUNT + 1))
  t.setStyle(TableStyle([('ALIGN',TABLE_STYLE_START,TABLE_STYLE_END,'CENTER'),
                        ('VALIGN',TABLE_STYLE_START, TABLE_STYLE_END, 'MIDDLE'),
                        ('FONTSIZE', TABLE_STYLE_START, TABLE_STYLE_END, FONT_SIZE),
                        ('INNERGRID', TABLE_STYLE_START, TABLE_STYLE_END, 0.25, colors.black),
                        ('BOX', TABLE_STYLE_START, TABLE_STYLE_END, 0.25, colors.black),
                        ]))

  elements.append(t)
  # write the document to disk
  doc.build(elements)


def convert_to_flashcards(wordSource, picSource, hasHeader, addNewLines):
  words = get_word_list(wordSource, hasHeader, addNewLines)
  output_pdf(words, picSource, wordSource[:-4] + ".pdf")

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(
    prog='Printable CardGame Generator',
    description='Takes a csv file and converts it to a pdf that can be printed and cut out to be used for games such as charades, codenames, or freedom of speech'
  )
  parser.add_argument('filename', help='csv file containing the list of the words/ phrases, one per line') 
  parser.add_argument('-p', metavar='picture path', help='location of the image to use as the back of the cards')
  parser.add_argument('-f', action='store_true', help='flag to say that the first line is a header and should be ignored.')
  parser.add_argument('-n', action='store_true', help='flag to add a newline around parenthesis')

  args = parser.parse_args()
  convert_to_flashcards(args.filename, args.p, args.f, args.n)
