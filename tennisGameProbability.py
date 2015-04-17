## calculate the probability of server winning a single game, 
## given p(winning single point) and current point score
 
## some results and commentary here:
## http://summerofjeff.wordpress.com/2010/12/03/single-game-win-expectancy-tables/
 
def fact(x):
    if x in [0, 1]:  return 1
    r = 1
    for a in range(1, (x+1)):  r = r*a
    return r
 
def ch(a, b):
    return fact(a)/(fact(b)*fact(a-b))
 
def gameOutcome(s, a, b):
    return ch((a+b), a)*(s**a)*((1-s)**b)*s
 
def gameProb(s, v=0, w=0):
    ## function calculates the probability of server winning
    ## a single game, given p(winning any given point) [s],
    ## and the current point score.
    ## v, w = current game score, where love = 0, 15 = 1, etc.
    ## - e.g. 30-15 is v=2, w=1
    ## check if game is already over:
    if v >= 4 and (v-w) >= 2:
        return 1
    elif w >= 4 and (w-v) >= 2:
        return 0
    else:   pass
    ## if deuce or ad score e.g. 5-4, reduce to e.g. 3-2
    while True:
        if (v+w) > 6:
            v -= 1
            w -= 1
        else:   break
    ## specific probabilities:
    if w == 0:  w0 = gameOutcome(s, 3-v, 0)
    else:   w0 = 0
    if w <= 1:  w15 = gameOutcome(s, 3-v, 1-w)
    else:   w15 = 0
    if w <= 2:  w30 = gameOutcome(s, 3-v, 2-w)
    else:   w30 = 0
    if v == 4:
        wAd, lAd = s, 0
        d = 1-s
    elif w == 4:
        wAd, lAd = 0, 1-s
        d = s
    else:
        wAd, lAd = 0, 0
        a = 3 - v
        b = 3 - w
        d = ch((a+b), a)*(s**a)*((1-s)**b)
    if v <= 2:  l30 = gameOutcome((1-s), 3-w, 2-v)
    else:   l30 = 0
    if v <= 1:  l15 = gameOutcome((1-s), 3-w, 1-v)
    else:   l15 = 0
    if v == 0:  l0 = gameOutcome((1-s), 3-w, 0)
    else:   l0 = 0
    ## given d = prob of getting to deuce,
    ## math to divide up further outcomes
    denom = s**2 + (1-s)**2
    wd = (d*(s**2))/denom
    ld = (d*((1-s)**2))/denom
    win = w0 + w15 + w30 + wd + wAd
    lose = l0 + l15 + l30 + ld + lAd
    return win
