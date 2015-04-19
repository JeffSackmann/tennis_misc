import random
from operator import itemgetter

## todo: reseeder() treats, e.g. seeds 17-32 as equivalent, though grand slam draws assign 17-24 to 
## potential matchups with 9-16 and 25-32 to potential matchups with 1-8. add function parameter for that.

def insertSeedOrNonseed(ndraw, seeds, nonseeds, sj, nj):
    if sj < len(seeds):
        ndraw.append(seeds[sj])
        sj += 1
    else:
        ndraw.append(nonseeds[nj])
        nj += 1
    return ndraw, sj, nj

byerow = [129, 'bye', 'bye', '', 'BYE']

def reseeder(draw, seedloc=3):
    ## reseeder takes a list of players (perhaps an existing draw) and generates
    ## a (new) draw according to non-strict seeding rules.  1st and 2nd seeds are
    ## placed in separate halves; 3 and 4 are randomly placed in the remaining
    ## quarters; 5 through 8 are randomly placed in the remaining 8ths,
    ## and so on.  If there are byes, they are given to the top seeds.
    ##
    ## parameter "draw" is a list of player entries between 24 and 128 players long, e.g.
    ## [['1', 'nadalra15', '(1)Nadal', '1', 'ESP'],
    ##  ['2', 'gruelsi15', 'Greul', '', 'GER']
    ##  ...]
    ## The column contents don't matter, except that seeds must all be in the same column,
    ## the index of which is the optional 'seedloc' parameter.  
    ## The player rows will be returned in the new order.
    ##
    ## As many seeds can be specified as you wish, but only one-quarter of the field
    ## (defined as a power of two, e.g. 24 players implies a 32 draw, so up to 8 seeds)
    ## will be 'seeded' in the sense that they will avoid other seeds until later
    ## rounds.  There must be at least two seeds.
    ## Byes are ok, too.  There cannot be more byes than seeds, and byes cannot
    ## exceed one-quarter of the draw.  reseeder inserts those with a row defined
    ## by the global variable byerow
    ##
    ## A basic test is included, testReseeder().  It generates sample draws within
    ## the above parameters, with draw sizes from 24 to 128 and numbers of seeds
    ## between 2 and one-quarter of the field, then runs reseeder on each.
    drawlen = len(draw)
    if drawlen > 64:    drawbin = 128
    elif drawlen > 32:  drawbin = 64
    else:   drawbin = 32
    numbyes = drawbin - drawlen
    ## extract and sort seeds
    seedlist = []
    for p in draw:
        if str(p[seedloc]).isdigit():
            newrow = p[:seedloc] + [int(p[seedloc])] + p[(seedloc+1):]
            seedlist.append(newrow)
    if len(seedlist) < 2:
        print 'reseeder requires at least two seeds'
        print impossiblevariable
    elif numbyes > len(seedlist):
        print 'reseeder cannot handle more byes than seeds'
        print impossiblevariable
    seedlist = sorted(seedlist, key=itemgetter(seedloc))
    ## place seeds in groups: 1, 2, 3-4, 5-8, etc.
    s1, s2, s3, s5, s9, s17, s33 = [], [], [], [], [], [], []
    for i in range(len(seedlist)):
        s = seedlist[i]
        if i == 0:  s1.append(s)
        elif i == 1:    s2.append(s)
        elif i < 4: s3.append(s)
        elif i < 8: s5.append(s)
        elif i < 16:    s9.append(s)
        elif i < 32:    s17.append(s)
        else:   s33.append(s)
    ## next few lines place 'extra' seeds with unseeded players
    if drawbin == 128:  unseeds = s33
    elif drawbin == 64: unseeds = s17
    else:   unseeds = s9
    for r in draw:
        if str(r[seedloc]).isdigit():    pass
        else:   unseeds.append(r)
    random.shuffle(s3)
    random.shuffle(s5)
    random.shuffle(s9)
    random.shuffle(s17)
    random.shuffle(unseeds)
    ## generate new draw according to non-strict seeding logic
    ndraw = []
    i = 0
    j, k, m, n, p = 0, 0, 0, 0, 0 ## counters to loop through lists of seeds, e.g. k through s5 for seeds 5-8
    while True:
        if i == drawbin:    break
        if i == 0:  ndraw.append(s1[0])
        elif i == (drawbin/2):   ndraw.append(s2[0])
        elif i % (drawbin/4) == 0:
            ndraw, j, p = insertSeedOrNonseed(ndraw, s3, unseeds, j, p)
        elif i % (drawbin/8) == 0:
            ndraw, k, p = insertSeedOrNonseed(ndraw, s5, unseeds, k, p)
        elif drawbin >= 64 and  i % (drawbin/16) == 0:
            ndraw, m, p = insertSeedOrNonseed(ndraw, s9, unseeds, m, p)
        elif drawbin == 128 and i % (drawbin/32) == 0:
            ndraw, n, p = insertSeedOrNonseed(ndraw, s17, unseeds, n, p)
        elif numbyes and type(ndraw[-1][seedloc]) is int:
            if int(ndraw[-1][seedloc]) <= numbyes:
                ndraw.append(byerow)
            else:
                ndraw.append(unseeds[p])
                p += 1
        else:
            ndraw.append(unseeds[p])
            p += 1
        i += 1
    return ndraw

def generateSampleDraw(fieldsize, numseeds):
    fakedraw = []
    for i in range(1, fieldsize+1):
        if i <= numseeds:
            fakerow = [i, 'playerid', 'Player', i, 'XXX']
        else:
            fakerow = [i, 'playerid', 'Player', '', 'XXX']
        fakedraw.append(fakerow)
    return fakedraw

def testReseeder():
    ## generates sample draws for every acceptable combination of
    ## field size and number of seeds
    for fieldsize in range(24, 129):
        if fieldsize > 64:  maxseeds = 32
        elif fieldsize > 32:    maxseeds = 16
        else:   maxseeds = 8
        for numseeds in range(2, (maxseeds+1)):
            byes = maxseeds*4 - fieldsize
            if byes > numseeds: continue
            print fieldsize, numseeds
            fakedraw = generateSampleDraw(fieldsize, numseeds)
            ndraw = reseeder(fakedraw)

def printSampleReseed(fieldsize, numseeds):
    ## generates sample draw and sends it to reseeder to get a
    ## visual check that it is behaving as predicted
    sdraw = generateSampleDraw(fieldsize, numseeds)
    ndraw = reseeder(sdraw)
    for player in ndraw:    print player
