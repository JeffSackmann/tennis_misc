## given probability of winning a best-of-three-set match and the assumption that sets are independent,
## output the probability of winning a best-of-five-set match
 
##One way to find the probability of winning an n-set match is to start with the probability of winning
##a single set.  If we have an estimated probability of winning a best-of-three, e.g. from betting odds,
##we need to work backwards to get the probability of winning a single set.
##
##If x is p(set win), the probability of winning a three-setter is:
##    x^2 + 2(x^2)(1-x)
##    x^2 is the p(winning in straight sets)
##    (x^2)(1-x) is the p(winning two sets and losing one)
##    and there are 2 permutations (LWW and WLW) that result in a three-set win
##
##Written another way, we have:
##    p(three-set-win) = -2x^3 + 3x^2
##    or: -2x^3 + 3x^2 - p(three-set-win) = 0
##
##The first line of the function solves the trinomial for the relevant root.  
##The second line uses similar logic to generate the probability of winning a five-setter:
##    x^3 --- p(straight-set-win)
##    3(x^3)(1-x) --- p(four-set-win): three sets won, one set lost, three permutations
##    6(x^3)(1-x)(1-x) --- p(five-set-win): two sets lost, six permutations (4c2)
 
import numpy
 
def fiveodds(p3):
    p1 = numpy.roots([-2, 3, 0, -1*p3])[1]
    p5 = (p1**3)*(4 - 3*p1 + (6*(1-p1)*(1-p1)))
    return p5
