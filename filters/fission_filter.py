from filters.concatenation_filter import ConcatFilter
from filters.concatenation_filter import ConcatEvent
from filters.concatenation_filter import AlignmentInfo
from aux.hmmer_tools import DomTableReader
from model.fasta_tools import Sequence


EXON_LENGTH = 30
E_VALUE_CUTOFF = 1e-100


class FissionEvent(ConcatEvent):
	"""
	Fission type ConcatEvent
	Use to set main sequence
	"""

	def __init__(self, mainseq):
		super(FissionEvent, self).__init__(mainseq)

	def getScore(self):
		return 0

class FissionFilter(ConcatFilter):
	"""
	Fission Filter
	Extends ConcatFilter
	"""

	__name__ = "FISSION_FILTER"

	def __init__(self, reference_genome, tempDir):
		super(FissionFilter, self).__init__(reference_genome, tempDir)

	def parseHmmerIntoConcatEvents(self, hmmerOutFile):
		"""
		Parse the hmmer file into events
		Main Seq is the
		"""
		#initialize
		events = {}
		#open DomTableReader to read HMMER as AlignmentInfo objects
		with DomTableReader(hmmerOutFile) as reader:
			row = reader.readRow()
			while not row == DomTableReader.EOF:
				if row == DomTableReader.BADFORMAT:
					break
				if row.getEValue() > E_VALUE_CUTOFF:
					#print "Evalue too high"
					row = reader.readRow()
					continue
				seq = Sequence(row.getTarget(), Sequence.PLACEHOLDER(row.getTLen()))
				ss = Sequence(row.getQuery(), Sequence.PLACEHOLDER(row.getQLen()))
				try:
					events[seq].addSubseq(ss)
					print "Setting " + str(ss) + " to " + str(AlignmentInfo(int(row.getQueryFrom()), int(row.getQueryTo()), int(row.getTargetFrom()), int(row.getTargetTo()), float(row.getEValue()))) + " -> " + str(seq)
					events[seq].setCoords(ss, AlignmentInfo(int(row.getQueryFrom()), int(row.getQueryTo()), int(row.getTargetFrom()), int(row.getTargetTo()), float(row.getEValue())))
				except KeyError as e:
					#set main sequence
					events[seq] = FissionEvent(seq)
					events[seq].addSubseq(ss)
					print "Setting " + str(ss) + " to " + str(AlignmentInfo(int(row.getQueryFrom()), int(row.getQueryTo()), int(row.getTargetFrom()), int(row.getTargetTo()), float(row.getEValue()))) + " -> " + str(seq)
					events[seq].setCoords(ss, AlignmentInfo(int(row.getQueryFrom()), int(row.getQueryTo()), int(row.getTargetFrom()), int(row.getTargetTo()), float(row.getEValue())))
				row = reader.readRow()
		return events.values()

	def checkSuitability(self, sequenceCoords, candidateCoords):
		"""
		Checks Suitability of Fission candidate, requiring overlap of less than 1 exon
		"""
		# s = range(sequenceCoords[0], sequenceCoords[1])
		# c = range(candidateCoords[0], candidateCoords[1])
		# ss = set(s)
		# i = ss.intersection(c)
		# return len(i) < EXON_LENGTH
		return sequenceCoords.getTargetTo() - candidateCoords.getTargetFrom() < EXON_LENGTH or candidateCoords.getTargetTo() - sequenceCoords.getTargetFrom() < EXON_LENGTH


	def mark(self, seq, pair, ref):
		seq.addNote("Sequence is Fission of " + ref.getIdentity() + " with sequence " + pair.getIdentity())

	def scanEvents(self, events):
		#create temporary dictionary
		new_events = dict( zip( map(ConcatEvent.getMainSeq, list(events)), list(events) ) )

		needClean = True
		while needClean:
			needClean = False

			#filter set of events that aren't real events
			for event in events:
				subseqs = event.getSubseqs()
				if len(subseqs) == 0 or len(subseqs) == 1:
					if event.getMainSeq() in new_events:
						new_events.pop(event.getMainSeq())
						print "Popping event " + str(event.getMainSeq()) + " -> " + str(event.getSubseqs())
				else:
					for subseq in subseqs.keys():
						#if it isn't a realistic match, (< Exon length)
						#OR
						#if it is a match of the same length
						if event.getMatchingLength(subseq) > event.getMainSeq().getSequenceLength() - EXON_LENGTH or event.getMatchingLength(subseq) < EXON_LENGTH:
							print event.getMatchingLength(subseq)
							print event.getMainSeq()
							print subseq
							print event.getSubseqs()[subseq]
							print event.getMainSeq().getSequenceLength()
							for e in new_events.values():
								e.removeSubseq(subseq)
								print "Removing subseq " + str(subseq) + " from " + str(event.getMainSeq())
							needClean = True
			events = list(new_events.values())

		infoCSV = "fissionInfo.csv"
		dirtySequences = []
		with open(infoCSV, "w") as csvWriter:
			csvWriter.write("Query,Pair,Reference,Evalue,QueryFrom,QueryTo,TargetFrom,TargetTo")
			#mark every query gene for fission if a suitable partner is found
			for event in events:
				subseqs = event.getSubseqs()
				for subseq in subseqs.keys():
					for candidate in subseqs.keys():
						if self.checkSuitability(subseqs[subseq][0], subseqs[candidate][0]):
							self.mark(subseq, candidate, event.getMainSeq())
							csvWriter.write(str(subseq) + "," + "")
							dirtySequences.append(subseq)
		print dirtySequences
		return set(dirtySequences)