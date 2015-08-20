from os.path import basename
from sewagefilter import SewageFilter
import lsftools as lsf


class ComplexityFilter(SewageFilter):

    __name__ = "0J_CHECK_FILTER"

    __zero_j__ = "/www/kirschner.med.harvard.edu/docroot/genomes/code/0j/0j.py"

    __threshold_level__ = None

    def __init__(self, thresh):
        super(SewageFilter, self).__init__()
        self.__threshold_level__ = thresh

    def filter_crap(self, input_file, output_file, diagnostics_file):
        """
        Run 0j on input file and strip of compressable sequences
        :param input_file: fasta input
        :param output_file: fasta output with fewer sequences than input
        :param diagnostics_file: fasta output with compressable sequences (appended to)
        :return:
        """
        temporary = "tmp/" + basename(input_file) + ".0j.raw" #temporary file for 0j raw output
        lsf.run_job('"' + self.__zero_j__ + " -scores_only " + input_file + " > " + temporary + '"', wait=True) #submit lsf job
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
                            try:
                                assert info[0] == corresponding_line[1:] #make sure same sequence being analyzed
                            except AssertionError:
                                print "Caught assert err\n"
                                print info[0] + "\n" + corresponding_line[1:] + "\n"
                                exit(1)
                            try:
                                complexity = float(info[1])/len(sequence) #calc. complexity (1-compressability)
                            except ValueError:
                                print "Error Parsing raw 0j output"
                                exit(1)
                            if complexity > self.__threshold_level__:
                                out_stream.write(corresponding_line + sequence + "\n")
                            else:
                                with open(diagnostics_file, "a") as diag_stream:
                                    diag_stream.write(corresponding_line.rstrip("\n") + "Sequence caught in complexity filter: " + str(complexity) + " < " + str(self.__threshold_level__) + "\n" + sequence + "\n")
                            line = complexity_data.readline()
                            corresponding_line = check_stream.readline()