#!/usr/bin/python
################################################################################
#
# IMDB Based JPG Poster Creator
#
# Creates a jpg poster image based on information from IMDB
#
################################################################################
#
# Userful keys for the movie variable:
#rating
#runtimes
#year
#votes
#title
#mpaa
#cover url
#genres
#akas
#director
#kind
#plot outline
#plot
#cast
#canonical title
#long imdb title
#long imdb canonical title
#smart canonical title
#smart long imdb canonical title
#full-size cover url


################################################################################
# CONFIGURATION
################################################################################

# This option is useful for bulk runs
# True results in an interactive mode, False results in a best-guess mode
ALWAYS_USE_FIRST_RESULT = True

# The image to use if one cant be found on IMDB
DEFAULT_COVER = 'default.jpg'


################################################################################
# Imports
################################################################################

# Third party pre requisite modules 
from imdb import IMDb
# Built in modules
import Image, ImageDraw, ImageFont
import textwrap, cStringIO, urllib, sys, pprint


################################################################################
# Functions
################################################################################

# Find a movie by keywords, returns (name, id)
def findMovieNameAndIdByKeywords(keywords):
    results = ia.search_movie(keywords)
    if (len(results) == 0):
        return []
    else:
        return [(result['smart long imdb canonical title'], result.getID()) for result in results]
    

# Returns the first movie (object) that matches the keywords given
def getMovieByID(ID):
    try:
        return ia.get_movie(ID)
    except:
        return None


# Retrieves and returns the full cover
def getFullCover(movie, maxwidth=500):
    #print "cover url = " + movie['full-size cover url']

    # Fetch and store the cover image in memory
    try:
        file = urllib.urlopen(movie['full-size cover url'])
        cs = cStringIO.StringIO(file.read())
        im = Image.open(cs)

    # If a cover cannot be obtained, use the default image instead
    except:
        im = Image.open(DEFAULT_COVER)

    # Ensure the image does not exceed the max width (or height)
    im.thumbnail((maxwidth, 700), Image.ANTIALIAS)

    return im


# Make a jpeg image (aka poster) with info about the given movie
def createImage(movie):

    # Create a blank canvas to work with
    im = Image.new('RGB', (1024, 768))
    draw = ImageDraw.Draw(im)

    # Get the cover image and place it on the canvas
    cover = getFullCover(movie)
    im.paste(cover, (20,20))

    # Print the full title
    draw.text((540,20), movie['smart long imdb canonical title'])

    # Print the running time
    draw.text((540,50), "Running time: " + movie['runtimes'][0] + "m")

    # Print the plot onto the canvas line by line
    try:
        text = movie['plot'][0]
    except:
        text = movie['plot outline'][0]
        
    x, y = 540, 80
    s = textwrap.wrap(text, 70)

    for line in s:
        draw.text((x,y), line)
        y = y + 20

    # Save the image as a file and return its name
    filename = movie['title']+".jpg"
    im.save(filename, "JPEG")
    return filename
    


################################################################################
# MAIN
################################################################################

# This is the IMDB client object
ia = IMDb()

# If no keywords are given on the command line, ask for some
if (len(sys.argv) > 1):
    keywords = ' '.join(sys.argv[1:])
else:
    keywords = raw_input("Enter search terms for a movie title: ")

# Search for movies - returns a list of tuples: (name, id)
movies = findMovieNameAndIdByKeywords(keywords)
print movies

if (len(movies) == 0):
    print "No movies found."
    sys.exit
elif (len(movies) == 1 or ALWAYS_USE_FIRST_RESULT):
    print "Found " + movies[0][0]
    movie = getMovieByID(movies[0][1])
else:
    print "Results:"
    for k,v in enumerate(movies):
        print str(k) + ") " + v[0]
    choice = int(raw_input("Enter your choice: "))
    movie = getMovieByID(movies[choice][1])

pprint.pprint(movie.keys())

imageFilename = createImage(movie)
print "'" + imageFilename + "' has been created!"
#print '-'*80 + '\n' + movie['title'] + '\n' + '-'*80 + '\n' + movie['plot outline'] + '\n' + '='*80 + '\n' + movie['plot'][0]

