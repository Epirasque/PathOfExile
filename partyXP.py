__author__ = 'laoshra'

import sys

def level2share(level):
    #http://pathofexile.gamepedia.com/Experience#Party_Play
    return pow(level+10,2.71)

def solutionHandler(str_levels):
    levels=[int (i) for i in str_levels]
    totalShare=0
    for level in levels:
        totalShare+=level2share(level)

    for level in levels:
        percentualShare=100.*level2share(level)/float(totalShare)
        print("Percentage of XP for level %u: %f" % (level, percentualShare) )

def main(argv):
    characterLevels=argv[1:]
    print("Running partyXP with arguments: %s" % characterLevels)
    solutionHandler(characterLevels)
    print("done.")

if __name__=="__main__":
    main(sys.argv);