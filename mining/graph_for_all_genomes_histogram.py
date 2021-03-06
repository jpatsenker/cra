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

try:
    xleft = float(sys.argv[4])
except (IndexError, ValueError):
    print "Improper Parameter: Left x limit"
    exit(1)

try:
    xright = float(sys.argv[5])
except (IndexError, ValueError):
    print "Improper Parameter: Right x limit"
    exit(1)

try:
    subdivide = int(sys.argv[6])
except (IndexError, ValueError):
    print "Improper Subdivision"
    exit(1)


d = {}
info = {}


bins = [1.0/subdivide] * subdivide
for i in range(len(bins)):
    bins[i] *= i
    d[bins[i]] = 0


#print bins;


for f in files:
    if f[f.rfind("."):] == ".0j" or f[f.rfind("."):] == ".cdhit":
        with open(direc + f) as stream_f:
            everything = stream_f.read()
            pairs = everything.split("\n")
            pairs.pop() #rid of last empty pair
            cumulative = 0
            for pair in pairs:
                #print pair + "\n"
                ord_pair = pair.split(",")
                try:
                    if float(ord_pair[0]) <= poi and f[f.rfind("."):] != ".cdhit":
                        cumulative += float(ord_pair[1])
                    if float(ord_pair[0]) == poi and f[f.rfind("."):] == ".cdhit":
                        cumulative += float(ord_pair[1])
                        print ord_pair
                    if float(ord_pair[0]) == poi:
                        try:
                            d[perform_bin(bins, cumulative)[0]] += 1
                        except KeyError:
                            d[perform_bin(bins, cumulative)[0]] = 1
                        info[f[:f.find(".")]] = perform_bin(bins, cumulative)[0]
                except (IndexError, ValueError):
                    print "Improperly Formatted File"
                    exit(1)

xs = sorted(d.keys())
ys = [None] * len(xs)
for i in range(len(xs)):
    ys[i] = d[xs[i]]

with open("out.csv", "w") as csv_stream:
    for tick in sorted(d.keys()):
        csv_stream.write(str(tick) + "," + str(d[tick]))
        for gen in info:
            if info[gen] == tick:
                csv_stream.write("," + gen)
        csv_stream.write("\n")

X = np.arange(len(xs))
pl.bar(X, ys, align = 'edge', width=1)
pl.xticks(X, xs, rotation='vertical')

try:
    pl.ylim(float(sys.argv[7]),float(sys.argv[8]))
except ValueError:
    print "Improper limit"
except IndexError:
    try:
        pl.ylim(0,float(sys.argv[7]))
    except IndexError:
        pl.ylim(0,1)

pl.xlim(xleft*subdivide, xright*subdivide)

fig = pl.gcf()
#axis.set_title( "" )
#print files[0]
if files[0][files[0].rfind(".")+1:] == "cdhit":
    pl.xlabel( "Fraction Clusters to Total Sequences at redundancy threshold of .7" )
    pl.ylabel( "Number of Genomes" )
else:
    pl.xlabel( "% of Corpus at complexity of less than .9" )
    pl.ylabel( "Number of Genomes" )

fig.tight_layout()
pl.savefig(outfile)
pl.show()