__author__ = 'laoshra'

import sys
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



def findAllValidSolutions(narrowedCandidates):
    validSolutions={}
    progress=0
    for candidate in narrowedCandidates:
        progress+=1
        if progress%100==0:
            print("Candidates: %u / %u" % (progress, len(narrowedCandidates)) )
        combined=sum(candidate)

        if combined%40==0 and combined>0: #narrow possible solutions
            print("Found a candidate: %s" %candidate)
            #nrCombinations=sum(1 for _ in itertools.permutations(candidate)) #this destroys the iterator; also way too expensive
            #print("Number of combinations: %u" % nrCombinations)
            combinations=itertools.permutations(candidate)
            combinationProgress=0
            for combination in combinations:
                combinationProgress+=1
                if combinationProgress%1000000==0:
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


def multipleSolutions(qualities):
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

    validSolutions=findAllValidSolutions(narrowedCandidates)

    return validSolutions


def printSortedSolutions(validSolutions):
    sortedSolutions = sorted(validSolutions.items(), key=operator.itemgetter(1))
    for solution in sortedSolutions:
        print("Solution with %u groups of 40: %s" % (solution[1], str(solution[0])) )


def main(argv):
    print("Running reach40 with arguments: %s" % argv)
    qualities=argv[1:]
    validSolutions=multipleSolutions(qualities)
    printSortedSolutions(validSolutions)
    print("Done.")

if __name__=="__main__":
    main(sys.argv);