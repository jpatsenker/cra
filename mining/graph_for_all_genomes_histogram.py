import sys
import os
import matplotlib
import bisect

matplotlib.use('Agg')

import numpy as np
import pylab as pl

def perform_bin(range_list, num):
    beg = bisect.bisect_right(range_list, num)
    if range_list[beg - 1] == num:  # Handle Perfect Hit Edge Case
        return [num, num]
    elif not beg:  # Left Edge Case
        return [None, range_list[0]]
    elif beg == len(range_list):  # Right Edge Case
        return [range_list[-1], None]
    else:
        return range_list[beg - 1:beg + 1]


poi = 0
direc = ""
outfile = ""
files = []

try:
    direc = sys.argv[1]
except IndexError:
    print "Improper Parameter: missing directory"
    exit(1)

try:
    files = os.listdir(direc)
except OSError:
    print "Improper Parameter: directory does not exist"
    exit(1)

try:
    outfile = sys.argv[2]
except IndexError:
    print "Improper Parameter: missing out-file"
    exit(1)

try:
    poi = sys.argv[3]
except IndexError:
    print "Improper Parameter: missing % of interest"
    exit(1)

try:
    poi = float(poi)
except ValueError:
    print "Improper Parameter: % of interest must be a float"
    exit(1)

d = {}

bins = [0,.01,.02,.03,.04,.05,.06,1]



for f in files:
    if f[f.rfind("."):] == ".0j" or f[f.rfind("."):] == ".cdhit":
        with open(direc + f) as stream_f:
            everything = stream_f.read()
            pairs = everything.split("\n")
            pairs.pop() #rid of last empty pair
            cumulative = 0
            for pair in pairs:
                print pair + "\n"
                ord_pair = pair.split(",")
                try:
                    if float(ord_pair[0]) <= poi:
                        cumulative += float(ord_pair[1])
                    if float(ord_pair[0]) == poi:
                        try:
                            d[perform_bin(bins, cumulative)[0]] = d[perform_bin(bins, cumulative)[0]] + 1
                        except KeyError:
                            d[perform_bin(bins, cumulative)[0]] = 1
                except (IndexError, ValueError):
                    print "Improperly Formatted File"
                    exit(1)



xs = sorted(d).keys()
ys = sorted(d).values()

X = np.arange(len(xs))
pl.bar(X, ys, align = 'edge', width=1)
pl.xticks(X, xs, rotation='vertical')

try:
    pl.ylim(float(sys.argv[4]),float(sys.argv[5]))
except ValueError:
    print "Improper limit"
except IndexError:
    try:
        pl.ylim(0,float(sys.argv[4]))
    except IndexError:
        pl.ylim(0,1)

fig = pl.gcf()
#axis.set_title( "" )
if files[0][files[0].find(".")+1:] == "cdhit":
    pl.xlabel( "Threshold (%)" )
    pl.ylabel( "Fraction Clusters to Total Sequences" )
else:
    pl.xlabel( "% Complexity" )
    pl.ylabel( "% of Corpus" )

fig.tight_layout()
pl.savefig(outfile)
pl.show()