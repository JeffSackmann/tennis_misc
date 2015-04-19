## calculate the probability of the current server winning
## a 6-game, tiebreak set, given prob. of server winning any
## given service point (s) or return point (u), and the current
## game score (v, w)
 
## some results:
## http://summerofjeff.wordpress.com/2010/12/02/single-set-win-expectancy-tables/

from tennisGameProbability import gameProb
from tennisTiebreakProbability import tiebreakProb
 
def fact(x):
    if x in [0, 1]:  return 1
    r = 1
    for a in range(1, (x+1)):  r = r*a
    return r
 
def ch(a, b):
    return fact(a)/(fact(b)*fact(a-b))
 
def setOutcome(final, sGames, rGames, vw, g, h):
    pOutcome = 0
    for j in range((sGames+1)):
        for k in range((rGames+1)):
            if (j + k) == (6 - 1 - vw):
                m = sGames - j
                n = rGames - k
                p = (g**j)*(h**k)*((1-g)**m)*((1-h)**n)*ch(sGames,j)*ch(rGames,k)*final
                pOutcome += p
            else:   continue
    return pOutcome
 
def setGeneral(s, u, v=0, w=0, tb=1):
    ## calculate the probability of the current server winning
    ## a 6-game, tiebreak set, given prob. of server winning any
    ## given service point (s) or return point (u), and the current
    ## game score (v, w)
    ## get prob of current server winning a service game:
    g = gameProb(s)
    ## and current server winning a return game:
    h = gameProb(u)
    ## is set over?
    if tb:
        if v == 7:  return 1
        elif w == 7:    return 0
        elif v == 6 and (v-w) > 1:  return 1
        elif w == 6 and (w-v) > 1:  return 0
        else:   pass
    else:
        if v >= 6 and (v-w) > 1:    return 1
        elif w >= 6 and (w-v) > 1:  return 0
        else:   pass
    ## if not over, re-adjust down to no higher than 6-6
    while True:
        if (v+w) > 12:
            v -= 1
            w -= 1
        else:   break
    ## if no tiebreak, chance that server wins set is ratio of server's prob of winning
    ## two games in a row to returner's prob of winning two games in a row
    if not tb:  deuceprob = (g*h)/((g*h) + (1-g)*(1-h))
    outcomes = {}
    ## special cases, 11 games or more already
    if (v+w) == 12:
        if tb:
            tp = tiebreakProb(s, u)
            outcomes['76'] = tp
            outcomes['67'] = 1 - tp
        else:
            outcomes['75'] = deuceprob
            outcomes['57'] = 1-deuceprob 
    elif (v+w) == 11:
        if tb:
            tp = tiebreakProb((1-u), (1-s))
            if v == 6:
                outcomes['75'] = g
                x = (1-g)
                outcomes['76'] = x*(1 - tp)
                outcomes['67'] = x*tp
            else:
                outcomes['57'] = 1-g
                x = g
                outcomes['76'] = x*(1 - tp)
                outcomes['67'] = x*tp
        else:
            if v == 6:
                outcomes['75'] = g
                outcomes['57'] = 0
                f = 1 - g ## f is p(getting to 6-6)
            else:
                outcomes['57'] = 1-g
                outcomes['75'] = 0
                f = g ## f is p(getting to 6-6)
            outcomes['75'] += f*deuceprob
            outcomes['57'] += f*(1-deuceprob)            
    else:   
        ## win probabilities
        for i in range(5): ## i = 0
            t = 6 + i - v - w ## total games remaining in set
            if t < 1:   continue
            if t % 2 == 0:
                final = h
                sGames = t/2
                rGames = sGames - 1
            else:
                final = g
                sGames = (t-1)/2
                rGames = (t-1)/2
            pOutcome = setOutcome(final, sGames, rGames, v, g, h)
            key = '6' + str(i)
            outcomes[key] = pOutcome
        ## loss probabilities
        ## this section isn't necessary, but I wrote it for informal
        ## testing purposes
        for i in range(5):
            t = 6 + i - v - w ## total games in set; here it's 6
            if t < 1:   continue
            if t % 2 == 0:
                final = 1-h
                sGames = t/2
                rGames = sGames - 1
            else:
                final = 1-g
                sGames = (t-1)/2
                rGames = (t-1)/2
            pOutcome = setOutcome(final, sGames, rGames, w, (1-g), (1-h))
            key = str(i) + '6'
            outcomes[key] = pOutcome       
        ## prob of getting to 5-5
        t = 10 - v - w
        if t % 2 == 0:
            sGames = t/2
            rGames = t/2
        else:
            sGames = (t-1)/2 + 1
            rGames = (t-1)/2
        f = setOutcome(1, sGames, rGames, v, g, h)
        if tb == 1:
            outcomes['75'] = f*g*h
            outcomes['57'] = f*(1-g)*(1-h)
            x = f*g*(1-h) + f*(1-g)*h ## p(getting to 6-6)    
            if (v+w) % 2 == 0:
                tp = tiebreakProb(s, u)
            else:
                tp = tiebreakProb(u, s)
            outcomes['76'] = x*tp
            outcomes['67'] = x - x*tp
        else:
            outcomes['75'] = f*deuceprob
            outcomes['57'] = f*(1-deuceprob)        
    win = 0
    for o in outcomes:
        if o in ['60', '61', '62', '63', '64', '75', '76']:
            win += outcomes[o]
        else:   pass
    return win, outcomes
