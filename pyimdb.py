#!/usr/bin/python

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
#full-size cover url - Could be anysize! Although *most* are < 500px wide

import Image, ImageDraw, ImageFont, textwrap, cStringIO, urllib
from imdb import IMDb

# Returns the first movie (object) that matches the keywords given
def getMovie(keywords):
    ia = IMDb()
    results = ia.search_movie(keywords)
    if len(results) > 0:
        return ia.get_movie(results[0].getID())
    else:
        return None


# Retrieves and returns the full cover
def getFullCover(movie):
    print "cover url = " + movie['full-size cover url']
    file = urllib.urlopen(movie['full-size cover url'])
    im = cStringIO.StringIO(file.read()) # constructs a StringIO holding the image
    return Image.open(im)


# Make a 1080p image
def createImage(movie):

    # Create a blank canvas to work with
    im = Image.new('RGB', (1024, 768))
    draw = ImageDraw.Draw(im)

    # Get the cover image and place it on the canvas
    cover = getFullCover(movie)
    im.paste(cover, (20,20))

    # Print the full title
    draw.text((480,20), movie['smart long imdb canonical title'])

    # Print the plot onto the canvas line by line
    x, y = 480, 100
    s = textwrap.wrap(movie['plot'][0], 80)
    for line in s:
        draw.text((x,y), line)
        y = y + 20

    filename = movie['title']+".jpg"
    im.save(filename, "JPEG")
    return filename
    


# MAIN
keywords = raw_input("Enter search terms for a movie title: ")
movie = getMovie(keywords)

imageFilename = createImage(movie)
print "'" + imageFilename + "' has been created!"
#print '-'*80 + '\n' + movie['title'] + '\n' + '-'*80 + '\n' + movie['plot outline'] + '\n' + '='*80 + '\n' + movie['plot'][0]

