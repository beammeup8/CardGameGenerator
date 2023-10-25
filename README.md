# CardGameGenerator
Generate card games with a consistent image on the back, and different strings for each card ad provided in a csv file. You can then just print the generated pdf out and cut out the individual cards and substitute them for the standard cards in your game of choice, or use them to make your own card based games.

## Usage
The script is run from the command line and takes a csv file to convert (tsv, or txt file with one entry per line will work as well is desired, however if the extension is not 3 characters long then the output filename may not be correct), and an optional picture to print on the back of the cards.  

If you use the -h option you get the full help documents as listed here:
```
usage: Printable CardGame Generator [-h] [-p picture path] filename

Takes a csv file and converts it to a pdf that can be printed and cut out to
be used for games such as charades, codenames, or freedom of speech

positional arguments:
  filename         csv file containing the list of the words/ phrases, one
                   per line

optional arguments:
  -h, --help       show this help message and exit
  -p picture path  location of the image to use as the back of the cards
```
