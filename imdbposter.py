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
ALWAYS_USE_FIRST_RESULT = False

# The image to use if one cant be found on IMDB
DEFAULT_COVER = 'default.jpg'

# Image configuration
CANVAS_WIDTH        = 1024
CANVAS_HEIGHT       = 768
CANVAS_SPACING      = 20
COVER_AREA_WIDTH    = 500
COVER_AREA_HEIGHT   = 700
TEXT_AREA_LEFT      = 540
TEXT_AREA_TOP       = CANVAS_SPACING
TEXT_AREA_SPACING   = 30
TEXT_AREA_DIVISION  = TEXT_AREA_SPACING + 20
TEXT_WRAP           = 70



################################################################################
# Imports
################################################################################

# Third party pre requisite modules 
try:
    from imdb import IMDb
except:
    print "You neet to install the python-imdbpy package!"
    sys.exit(1)

# Built in modules
import Image, ImageDraw, ImageFont
import textwrap, cStringIO, urllib, sys, pprint


################################################################################
# Functions
################################################################################

# Find a movie by keywords, returns a list of (name, id)
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
def getCover(movie, maxwidth=COVER_AREA_WIDTH, maxheight=COVER_AREA_HEIGHT):

    # Fetch and store the cover image in memory
    if (movie.has_key('full-size cover url')):
        url = movie['full-size cover url']
        cover = cStringIO.StringIO(urllib.urlopen(url).read())
    elif (movie.has_key('cover url')):
        url = movie['cover url']
        cover = cStringIO.StringIO(urllib.urlopen(url).read())

    # If a cover cannot be obtained, use the default image instead
    else:
        cover = DEFAULT_COVER

    # Open the appropriate cover
    im = Image.open(cover)

    # Ensure the image does not exceed the max width (or height)
    im.thumbnail((maxwidth, maxheight), Image.ANTIALIAS)

    return im


# Make a jpeg image (aka poster) with info about the given movie
def createImage(movie):

    # Keep track of vertical position while printing text
    y = TEXT_AREA_TOP

    # Create a blank canvas to work with
    im = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT))
    draw = ImageDraw.Draw(im)

    # Get the cover image and place it in the center of the canvas
    cover = getCover(movie)
    coverX = CANVAS_SPACING + (COVER_AREA_WIDTH  / 2) - (cover.size[0] / 2)
    coverY = CANVAS_SPACING + (COVER_AREA_HEIGHT / 2) - (cover.size[1] / 2)
    im.paste(cover, (coverX, coverY))

    # Print the TITLE
    if (movie.has_key('smart long imdb canonical title')):
        title = movie['smart long imdb canonical title']
    elif (movie.has_key('title')):
        title = movie['title']
    else:
        title = "The movie you requested could not be found"
    draw.text((TEXT_AREA_LEFT,y), title)
    
    y += TEXT_AREA_DIVISION

    # Print the RUNNING TIME
    if (movie.has_key('runtimes')):
        runtime = movie['runtimes'][0] + "m"
    else:
        runtime = "N/A"
    draw.text((TEXT_AREA_LEFT,y), "Running time: " + runtime)

    y += TEXT_AREA_SPACING

    # Print STAR RATING
    if (movie.has_key('rating')):
        rating = "%.1f / 10 stars" % movie['rating']
    else:
        rating = "N/A"
    draw.text((TEXT_AREA_LEFT,y), "Rating: " + rating)

    y += TEXT_AREA_SPACING

    # Print MPAA RATING (aka CLASSIFICATION)
    if (movie.has_key('mpaa')):
        classification = movie['mpaa']
    else:
        classification = "N/A"
    # Wrap the text at the TEXT_WRAP character limit
    text = textwrap.wrap("Classification: " + classification, TEXT_WRAP)
    for line in text:
        draw.text((TEXT_AREA_LEFT,y), line)
        y += CANVAS_SPACING

    y += TEXT_AREA_DIVISION - CANVAS_SPACING

    # Print the PLOT onto the canvas line by line
    if (movie.has_key('plot')):
        plot = movie['plot'][0]
    elif (movie.has_key('plot outline')):
        plot = movie['plot outline'][0]
    else:
        plot = "..."
    # Wrap the text at the TEXT_WRAP character limit
    text = textwrap.wrap(plot, TEXT_WRAP)
    for line in text:
        draw.text((TEXT_AREA_LEFT,y), line)
        y += CANVAS_SPACING

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

if (len(movies) == 0):
    print "No movies found."
    sys.exit(1)
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

