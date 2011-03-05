#!/bin/bash

# SIMPLE TEST
# Grab one poster and then view it! ...simple! :)

#python imdbposter.py -a stone; eog Stone.jpg

# BULK TEST
# This script just runs some common test cases I've been using
# Then I just have to run through the jpg's to check how it went

python imdbposter.py -a stone
python imdbposter.py -a matrix
python imdbposter.py -a matrix reloaded
python imdbposter.py -a pulp fiction
python imdbposter.py -a snatch
python imdbposter.py -a vendetta


# OPTIONS TEST
# This tests some different possibilities of options

#python imdbposter.py -a matrix
#python imdbposter.py -auto matrix
#python imdbposter.py -a
#python imdbposter.py -auto
