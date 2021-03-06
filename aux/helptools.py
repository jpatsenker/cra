def printHelp():
	"""
	Print help for the pipeline
	TODO: help file
	:return:
	"""
	print 'Command Example: python run_cra.py [input] [clean_output] [messy_output] [email] [parameters]\nParameters:\n"-0j #" - Set minimum complexity (default .9)\n"-ct #" - Set threshold for running CD-HIT (default .7)\n"-cl #" - Set fractional length for redundancy filtering (default .8)\n"-min #" - Set minimum length (default 30)\n"-max #" - Set maximum length (default 30000)\n"-fft #" - Set threshold for running CD-HIT in Fusion/Fission filter (default .7)\n"-ffl #" - Set fractional length (bottom) for fusion/fission filtering (default .8)\n"-xs #" - Maximum number of consecutive Xs in sequence to ignore (default 0)\n"-ms" - Check for M as first amino acid (default does not check)\n"-nolen" - Destage length filter (default completes stage)\n"-nocomp" - Destage complexity (0j) filter (default completes stage)\n"-nored" - Destage redundancy (CD-HIT) filter (default completes stage)\n"-noff" - Destage fusion/fission (Ff) filter (default completes stage)'

