from os.path import basename

from filters.sewagefilter import SewageFilter
from filters.sewagefilter import BrokenFilterError
from aux import lsftools as lsf, logtools


class ComplexityFilter(SewageFilter):

    __name__ = "COMPLEXITY_FILTER"

    __zero_j__ = "/www/kirschner.med.harvard.edu/docroot/genomes/code/0j/0j.py"

    __threshold_level__ = None

    def __init__(self, thresh, lfil = None):
        super(ComplexityFilter, self).__init__()
        self.__threshold_level__ = thresh
        self.__logfile__ = lfil

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run 0j on input file and strip of compressable sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """
        temporary = "tmp/" + basename(input_file) + ".0j.raw" #temporary file for 0j raw output
        lsf.run_job('"' + self.__zero_j__ + " -scores_only " + input_file + " > " + temporary + '"', wait=True, lfil=self.__logfile__) #submit lsf job
        with open(temporary, "r") as complexity_data: #open output
            with open(input_file, "r") as check_stream: #open input_file for lengths of sequences as well as checking names
                with open(output_file, "w") as out_stream: #open out_file
                    line = complexity_data.readline()
                    corresponding_line = check_stream.readline()
                    while line and corresponding_line: #read over ever sequence (and its entry in 0j raw file)
                        if line == line:
                            sequence = check_stream.readline() #get sequence from fasta
                            sequence = sequence.rstrip("\n") #get rid of extra \n
                            info = line.split() #isolate all parts of 0j raw
                            corresponding_line_id = corresponding_line.split()[0] #get only id in fasta seq
                            try:
                                assert info[0] == corresponding_line_id[1:].rstrip("\n") #make sure same sequence being analyzed
                            except AssertionError:
                                print "Caught assert err\n"
                                print "-" + info[0] + "-\n-" + corresponding_line_id[1:].rstrip("\n") + "-\n"
                                logtools.add_fatal_error(self.__logfile__, "Sequence order doesn't match up in 0j and input files")
                                raise BrokenFilterError(ComplexityFilter.__name__)
                            try:
                                complexity = float(1) - float(info[2])/len(sequence) #calc. complexity (1-compressability)
                            except ValueError:
                                print "Error Parsing raw 0j output"
                                logtools.add_fatal_error(self.__logfile__, "Cannot parse 0j raw output")
                                raise BrokenFilterError(ComplexityFilter.__name__)
                            if complexity > self.__threshold_level__:
                                out_stream.write(corresponding_line + sequence + "\n")
                            else:
                                with open(diagnostics_file, "a") as diag_stream:
                                    diag_stream.write(corresponding_line.rstrip("\n") + " Complexity Too Low:  " + ("%.3f" % complexity) + " < " + str(self.__threshold_level__) + "\n" + sequence + "\n")
                            line = complexity_data.readline()
                            corresponding_line = check_stream.readline()