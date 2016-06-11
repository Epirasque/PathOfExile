#!/usr/bin/python

import itertools
import operator
import copy

class packOfQuality:
    def __init__(self, qualities):
        self.qualities=qualities

    def __str__(self):
        return " < %s > " % self.qualities

def powerset(seq): #http://www.technomancy.org/python/powerset-generator-python/
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item



def removeQualities(qualities, toRemoveOnce):
    qualitiesLeft=copy.deepcopy(qualities)
    assert(len(toRemoveOnce)==1)
    for r in toRemoveOnce[0]:
        qualitiesLeft.remove(str(r))

    return qualitiesLeft



def findAllValidSolutions(narrowedCandidates, args):
    v=args.verbose
    validSolutions={}
    progress=0
    for candidate in narrowedCandidates:
        progress+=1
        if v and progress%100==0:
            print("Candidates: %u / %u" % (progress, len(narrowedCandidates)) )
        combined=sum(candidate)

        if combined%40==0 and combined>0: #narrow possible solutions
            if v:
                print("Found a candidate: %s" %candidate)
            #nrCombinations=sum(1 for _ in itertools.permutations(candidate)) #this destroys the iterator; also way too expensive
            #print("Number of combinations: %u" % nrCombinations)
            combinations=itertools.permutations(candidate)
            combinationProgress=0
            for combination in combinations:
                combinationProgress+=1
                if v and combinationProgress%1000000==0:
                    print("Combinations: %u" % (combinationProgress) )
                reach40=0
                nr40s=0
                invalid=False
                for c in combination:
                    reach40+=c
                    if reach40==40:
                        reach40=0
                        nr40s+=1
                    if reach40>40:
                        invalid=True
                        break
                if not invalid:
                    validSolutions[str(combination)]=nr40s
                    break
                #print("%s" % str(combination))

    return validSolutions


def multipleSolutions(qualities, args):
    candidates_gen=powerset(copy.deepcopy(qualities))
    candidates=reversed(list(candidates_gen))
    allCandidates=[]
    for str_candidate in candidates: #reversed faster in worst case with many elements
        candidate_int=[int (i) for i in str_candidate]
        allCandidates.append(sorted(candidate_int))

    allCandidates.sort()
    narrowedCandidates=list(allCandidates for allCandidates,_ in itertools.groupby(allCandidates))  #get rid of duplicates (thx to sorting within candidates)
    narrowedCandidates.sort()
    print("All candidates: %u, narrowed down: %u" % (len(allCandidates), len(narrowedCandidates)) )

    validSolutions=findAllValidSolutions(narrowedCandidates, args)

    return validSolutions


def printSortedSolutions(validSolutions):
    sortedSolutions = sorted(validSolutions.items(), key=operator.itemgetter(1))
    for solution in sortedSolutions:
        print("Solution with %u groups of 40: %s" % (solution[1], str(solution[0])) )

def exhaustiveSearch(qualities, args): #recommended to run with <= 16 quality values, very big amounts won't fit the RAM
            validSolutions=multipleSolutions(qualities, args)
            printSortedSolutions(validSolutions)





#--- databeavers "quick & greedy" implementation

def find_valid(q, b, s, t):
	for i in range(b, len(q)):
		if s+q[i]==t or s+q[i]+q[-1]<=t:
			return i

def increment(q, c):
	n = q[c[-1]]
	for i in range(c[-1]+1, len(q)):
		if q[i]!=n:
			c[-1] = i
			return True
	return False

def greedy(q, t):
	r = []
	while sum(q)>=t:
		c = [0]
		while c:
			s = sum(q[i] for i in c)
			if s==t:
				break

			i = find_valid(q, c[-1]+1, s, t)
			if i:
				c.append(i)
				continue

			while c:
				if increment(q, c):
					break

				c.pop()

		if not c:
			break

		r.append([q[i] for i in c])
		q = [q[i] for i in range(len(q)) if i not in c]

	return r, q

def pair_sums(q):
	return [(i, j, q[i]+q[j]) for i in range(0, len(q)-1) for j in range(i+1, len(q))]

def permute(r, q):
	p = pair_sums(q)
	for c in r:
		t = pair_sums(c)

		for x in t:
			for y in p:
				if x[2]==y[2] and q[y[0]]<c[x[0]]:
					c[x[0]], q[y[0]] = q[y[0]], c[x[0]]
					c[x[1]], q[y[1]] = q[y[1]], c[x[1]]
					return True

	return False

def main(args): #modified implementation of arguments
    q=args.qualities
    v=args.verbose

    allQualities=copy.deepcopy(q) #backup for exhaustive search

    q = sorted(q, reverse=True)

    print("Performing quick and greedy search.")

    if v:
        print("Input: {}".format(" ".join(str(n) for n in q)))

    r, q = greedy(q, 40)
    if v:
        print("Leftovers after initial round: {} (total {})".format(" ".join(str(n) for n in q), sum(q)))
    i = 0
    while sum(q)>40 and i<100:
        permute(r, q)
        i += 1
        n, q = greedy(q, 40)
        r += n
    for c in r:
        print("Found 40% combination: {}".format(" ".join([str(n) for n in c])))
    if q:
        print("Leftovers: {} (total {})".format(" ".join(str(n) for n in q), sum(q)))
        if len(allQualities)<=16:
            print("At most 16 inputs -> performing exhaustive search to list all possible combinations")
            exhaustiveSearch(allQualities, args)
        else:
            print("More than 16 inputs, exhaustive search is not recommended (it can be enforced it with -e)")
    else:
        print("No leftovers")

def test():
	import random
	a = 5**0.5
	b = 20**0.5
	for k in range(100):
		q = [int((a+random.random()*(b-a))**2) for i in range(100)]
		if k:
			print("---")
		main(q, True)

#--- end of databeavers implementation


if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description="For given quality values, find groups of 40. Uses two different approaches depending on the number of arguments.")

    parser.add_argument("-t", "--test", dest="test", action="store_true", help="test the quick and greedy approach")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="output progress and intermediate results")
    parser.add_argument("-e", "--exhaustive", dest="exhaustive", action="store_true", help="enforce exhaustive search WARNING: might occupy huge amounts of RAM resulting in system-wide issues")
    parser.add_argument("-g", "--greedy", dest="greedy", action="store_true", help="enforce greedy search (much faster but not always optimal)")

    parser.add_argument("qualities", nargs="+", type=int, help="integer quality values")

    args = parser.parse_args()

    if args.exhaustive or args.greedy:
        print("SORRY: the flags -e and -g are not implemented yet.")
        exit(1)

    if args.test:
        test()
    else:
        main(args)
