import subprocess
import random

def runBlast(sequences, reference):
	loadBlast()
	name = random.random()
	out = random.random()
	makedb = subprocess.Popen("makeblastdb -in " + reference + " -dbtype 'prot' -out " + out + " -name -" + name)
	makedb.wait()
	run = subprocess.Popen("blastp -outfmt 8 -evalue 1e-5 -db " + name + " -query " + sequences + " -out " + out + ".result")


def loadBlast():
	p = subprocess.Popen("module load seq/blast/ncbi-blast/2.2.30")
	p.wait()