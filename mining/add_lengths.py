import sys
import io
import os





input = fopen(argv[1], "r")
temp_out = fopen("tmp/withlengths", "w")

line = input.readline()

while line:
	if line[0] == '>':
		sequence = ''
		seq_line = input.readline()
		while sequence[0] != '>' or not sequence:
			sequence += seq_line
			seq_line = input.readline()
		#endwhile
		sequence.replace('\n', '')
		temp_out.write(line + " length: " + len(sequence))
		temp_out.write(sequence)
		line = sequence[sequence.rfind('>'):]
	#endif
#endwhile

subprocess.Popen(["mv", "tmp/withlengths", argv[1]])