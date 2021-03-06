import sys
import string

from aux import lsftools

#MODULE_PYTHON_INIT = "/opt/Modules/3.2.10/init/python.py"
MODULE_PYTHON_INIT = "/opt/Modules/3.2.10/init"

'''
Hmmer location on orchestra
'''
HMMER_PATH = "seq/hmmer/3.1"

"""
Toolbox for working with HMMER
"""

def runHmmer(sequences, reference, output, lfil = None):
	"""
	Run HMMER parallel-like
	TODO: make sure this doesn't stall - requests a lot of resources
	:param sequences:
	:param reference:
	:param output:
	:param lfil:
	:return:
	"""
	run = lsftools.run_hmmer_parallel(sequences, reference, output, lfil=lfil)
	#print "phmmer --domtblout " + output + " " + sequences + " " + reference
	#run = subprocess.Popen(["phmmer", "--domtblout", output, sequences, reference])
	#run.wait()

def loadHmmer():
	"""
	Load HMMER
	:return:
	"""
	sys.path.append(MODULE_PYTHON_INIT)
	import python
	#execfile(MODULE_PYTHON_INIT)
	python.module("load", HMMER_PATH)


class DomTableRow:
	"""
	Class to hold information about a single domtblout row for phmmer. PLEASE KEEP IMMUTABLE
	"""
	def __init__(self, target, targetAccession, tlen, query, queryAccession, qlen, eValue, score, bias, queryFrom, queryTo, targetFrom, targetTo, acc, description):
		self.__target__ = target
		self.__targetAccession__ = targetAccession
		self.__tlen__ = int(tlen)
		self.__query__ = query
		self.__queryAccession__ = queryAccession
		self.__qlen__ = int(qlen)
		self.__eValue__ = float(eValue)
		self.__score__ = score
		self.__bias__ = bias
		self.__queryFrom__ = queryFrom
		self.__queryTo__ = queryTo
		self.__targetFrom__ = targetFrom
		self.__targetTo__ = targetTo
		self.__acc__ = acc
		self.__description__ = description

	def getTarget(self):
		return self.__target__

	def getTargetAccession(self):
		return self.__targetAccession__

	def getTLen(self):
		return self.__tlen__

	def getQuery(self):
		return self.__query__

	def getQueryAccession(self):
		return self.__queryAccession__

	def getQLen(self):
		return self.__qlen__

	def getEValue(self):
		return self.__eValue__

	def getScore(self):
		return self.__score__

	def getBias(self):
		return self.__bias__

	def getQueryFrom(self):
		return self.__queryFrom__

	def getQueryTo(self):
		return self.__queryTo__

	def getTargetFrom(self):
		return self.__targetFrom__

	def getTargetTo(self):
		return self.__targetTo__

	def getAcc(self):
		return self.__acc__

	def getDescription(self):
		return self.__description__





class DomTableReader:
	"""
	Class for reading --domtblout files from phmmer
	"""
	BADFORMAT = -666
	EOF = False

	def __init__ (self, input_file):
		"""
		Method for initializing fasta reader
		"""
		self.__input_file__ = input_file
		self.__file_stream__ = open(self.__input_file__, "r")
		self.__line_number__ = 0

	def __enter__(self):
		assert not self.__file_stream__.closed
		check = self.__file_stream__.readline().rstrip()
		#assert check == "#                                                                            --- full sequence --- -------------- this domain -------------   hmm coord   ali coord   env coord"
		check = self.__file_stream__.readline().rstrip()
		
		#assert check == "# target name        accession   tlen query name           accession   qlen   E-value  score  bias   #  of  c-Evalue  i-Evalue  score  bias  from    to  from    to  from    to  acc description of target"
		ref = ['target name', 'accession', 'tlen', 'query name', 'qlen', 'E-value', 'score', 'bias', '#', 'of', 'c-Evalue', 'i-Evalue', 'from', 'to', 'acc', 'description of target']
		assert reduce(lambda b,c: b and c, map(lambda a: a>=0, map(lambda x: string.find(check, x), ref)), True)

		check = self.__file_stream__.readline().rstrip()
		self.__line_number__+=3
		#assert check == "#------------------- ---------- ----- -------------------- ---------- ----- --------- ------ ----- --- --- --------- --------- ------ ----- ----- ----- ----- ----- ----- ----- ---- ---------------------"
		return self

	def readRow(self):
		"""
		Method for reading a tbl row from file
		"""
		rowRaw = self.__file_stream__.readline()
		self.__line_number__+=1
		row = rowRaw.rstrip()
		if not row:
			return DomTableReader.EOF
		while row[0] == '#':
			row = self.__file_stream__.readline().rstrip()
			self.__line_number__+=1
			if not row:
				return DomTableReader.EOF

		rowArr = row.split()
		#print row
		#print rowArr
		try:
			tblRow = DomTableRow(rowArr[0],
								rowArr[1],
								rowArr[2],
								rowArr[3],
								rowArr[4],
								rowArr[5],
								rowArr[6],
								rowArr[7],
								rowArr[8], 
								rowArr[15],
								rowArr[16],
								rowArr[17],
								rowArr[18],
								rowArr[21],
								rowArr[22])
		except IndexError as e:
			print rowRaw
			print row
			print rowArr
			print self.__line_number__
			print "Check Format of HMMER domtblout file: " + str(e)
			return DomTableReader.BADFORMAT

		return tblRow

	def __exit__(self ,type, value, traceback):
		"""
		Method for closing fasta file
		"""
		self.__file_stream__.close()
