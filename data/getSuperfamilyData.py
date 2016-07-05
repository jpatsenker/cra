import string

with open("superfamily/genomes", "r") as reader:
	line1 = reader.readline()
	line2 = reader.readline()
	line3 = reader.readline()

	line2Info = map(string.lstrip, map(string.rstrip, line2.split('|')))[1:-1]
	assert line2Info == ['genome', 'name', 'include', 'excuse', 'domain', 'comment', 'taxonomy', 'taxon_id', 'download_link', 'download_date', 'gene_link', 'homepage', 'password', 'parse', 'order1', 'supfam', 'order2']

	with open("superfamily/genomeInfo.csv", "w") as writer:
		map(lambda line: writer.write(reduce(lambda x, y: x+","+y, map(string.lstrip, map(string.rstrip, line.split('|')))[1:-1], "")), reader)