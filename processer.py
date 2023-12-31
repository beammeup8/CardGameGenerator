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

def get_word_list(fileName):
  lines = []
  with open(fileName, "r") as file:
    txt = file.read()
    file.close()
    lines = txt.splitlines()
  return lines

def output_pdf(words, picture, newFileName):
  # Makes sure the final column is always full 
  # by adding spare cards that can be filled in later
  if len(words) % COL_COUNT != 0:
    for i in range(COL_COUNT - len(words) % COL_COUNT ):
      words.append("") 
  
  doc = SimpleDocTemplate(newFileName, pagesize=letter)
  x,y = letter

  if picture:
    a = Image(picture, (0.9*x)/COL_COUNT, (0.9*y)/ROW_COUNT)  

  elements = []
  data = []
  page_entry = ROW_COUNT * COL_COUNT
  style = ParagraphStyle(
    name='Normal',
    fontSize=FONT_SIZE,
    alignment=TA_CENTER,
    leading=FONT_SIZE
  )
  #style.setFont('DarkGardenMK', FONT_SIZE)
  for i in range(0, len(words), COL_COUNT):
    # add the card backs where needed
    if picture and i % page_entry == 0 and i != 0:
      for j in range(ROW_COUNT):
        data.append([a for k in range(COL_COUNT)])
    # add the current row of words
    data.append([Paragraph(words[i+k], style) for k in range(COL_COUNT)])
    
  # add the empty spaces to finish the page
  over_count = len(words) % page_entry
  curr_rows = math.ceil(over_count/ROW_COUNT)
  for i in range(curr_rows, ROW_COUNT, COL_COUNT):
    data.append(["" for j  in range(COL_COUNT)])

  # add the pictures for the page
  if picture:
    for j in range(ROW_COUNT):
      data.append([a for k in range(COL_COUNT)])
  
  t=Table(data, x/COL_COUNT, y/(ROW_COUNT + 1))
  t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1,-1), FONT_SIZE),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ]))

  elements.append(t)
  # write the document to disk
  doc.build(elements)


def convert_to_flashcards(wordSource, picSource):
  words = get_word_list(wordSource)
  output_pdf(words, picSource, wordSource[:-4] + ".pdf")

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(
    prog='Printable CardGame Generator',
    description='Takes a csv file and converts it to a pdf that can be printed and cut out to be used for games such as charades, codenames, or freedom of speech'
  )
  parser.add_argument('filename', help='csv file containing the list of the words/ phrases, one per line') 
  parser.add_argument('-p', metavar='picture path', help='location of the image to use as the back of the cards')
  args = parser.parse_args()
  convert_to_flashcards(args.filename, args.p)
