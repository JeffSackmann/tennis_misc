## calculate the probability that the current server wins a best-of-p tiebreak.
 
## some results shown here:
## http://summerofjeff.wordpress.com/2010/12/04/7-point-tiebreak-win-expectancy-tables/
 
def fact(x):
    if x in [0, 1]:  return 1
    r = 1
    for a in range(1, (x+1)):  r = r*a
    return r
 
def ch(a, b):
    return fact(a)/(fact(b)*fact(a-b))
 
def tiebreakProb(s, t, v=0, w=0, p=7):
    ## calculate the probability that the current server wins a best-of-p tiebreak.
    ## s = p(server wins service point)
    ## t = p(current server wins return point)
    ## v, w = current score
    ## check if tiebreak is already over:
    if v >= p and (v-w) >= 2:
        return 1
    elif w >= p and (w-v) >= 2:
        return 0
    else:   pass
    ## re-adjust so that point score is not higher than p;
    ## e.g., if p=7 and score is 8-8, adjust to 6-6, which
    ## is logically equivalent
    while True:
        if (v+w) > 2*(p-1):
            v -= 1
            w -= 1
        else:   break
    outcomes = {} ## track probability of each possible score
    ## this is messy and probably not optimal, figuring out
    ## how many points remain, and how many are on each
    ## player's serve:
    for i in range((p-1)):
        remain = p + i - v - w
        if remain < 1:  continue
        else:   pass
        if remain % 2 == 1: 
            if (v+w) % 2 == 0: ## sr[rs[sr
                if (remain-1) % 4 == 0: ## ...s
                    svc = (remain+1)/2 
                    ret = (remain-1)/2
                else:
                    svc = (remain-1)/2
                    ret = (remain+1)/2
            else: ## ss[rr[ss[
                if (remain-1) % 4 == 0: ## ...s
                    svc = (remain+1)/2 
                    ret = (remain-1)/2
                else:
                    svc = (remain+1)/2
                    ret = (remain-1)/2                
        else:
            if (v+w) % 2 == 0: ## sr[rs[sr
                svc, ret = remain/2, remain/2
            else: ## ss[rr[ss[
                svc, ret = (remain-2)/2, (remain-2)/2
                if remain % 4 == 0:
                    svc += 1
                    ret += 1
                else:
                    svc += 2
        ## who serves the last point?
        if (v+w) % 2 == 0:
##            if remain in [1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21]: ## pattern: remain % 4 in [0, 1]
            if (remain % 4) in [0, 1]:
                final = s
                svc -= 1
            else:
                final = t
                ret -= 1
        else:
##            if remain in [3, 4, 7, 8, 11, 12, 15, 16, 19, 20]:
            if (remain%4) in [3, 0]:
                final = t
                ret -= 1
            else:
                final = s
                svc -= 1
        pOutcome = 0
        for j in range(svc+1):
            for k in range(ret+1):
                if (j+k) == (p - 1 - v):
                    m = svc - j
                    n = ret - k
                    pr = (s**j)*(t**k)*((1-s)**m)*((1-t)**n)*ch(svc,j)*ch(ret,k)*final
                    pOutcome += pr
                else:   continue
        key = str(p) + str(i)
        outcomes[key] = pOutcome
    if remain % 2 == 1: 
        if (v+w) % 2 == 0: ## sr[rs[sr
            if (remain-1) % 4 == 0: ## ...s
                svc = (remain+1)/2 
                ret = (remain-1)/2
            else:
                svc = (remain-1)/2
                ret = (remain+1)/2
        else: ## ss[rr[ss[
            if (remain-1) % 4 == 0: ## ...s
                svc = (remain+1)/2 
                ret = (remain-1)/2
            else:
                svc = (remain+1)/2
                ret = (remain-1)/2                
    else:
        if (v+w) % 2 == 0: ## sr[rs[sr
            svc, ret = remain/2, remain/2
        else: ## ss[rr[ss[
            svc, ret = (remain-2)/2, (remain-2)/2
            if remain % 4 == 0:
                svc += 1
                ret += 1
            else:
                svc += 2
    ## probability of getting to (p-1)-(p-1) (e.g. 6-6)
    final = 1
    x = 0
    for j in range(svc+1):
        for k in range(ret+1):
            if (j+k) == (p - 1 - v):
                m = svc - j
                n = ret - k
                pr = (s**j)*(t**k)*((1-s)**m)*((1-t)**n)*ch(svc,j)*ch(ret,k)*final
                x += pr
            else:   continue
    outcomes['+'] = (x*s*t)/((s*t) + (1-s)*(1-t))
    ## add up all positive outcomes
    wtb = 0
    for z in outcomes:
        wtb += outcomes[z]
    return wtb
