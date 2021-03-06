from email.mime.multipart import MIMEMultipart
import sys
import os
import subprocess
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

"""DEPRECATED"""

def send_email(info, email, files):
    sender = 'noreply@kirschner.med.harvard.edu'
    receivers = email

    message = MIMEMultipart(
        From="CRAP DB <noreply@kirschner.med.harvard.edu>",
        Subject="CRAP Score"
    )

    body = MIMEText(info)
    message.attach(body)

    for f in files or []:
        with open(f, "rb") as fil:
            attach_file = MIMEApplication(fil.read())
            attach_file.add_header('Content-Disposition', 'attachment', filename="length_distribution.png")
            message.attach(attach_file)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"





# launch from main dir

fastaChecker = '/www/kirschner.med.harvard.edu/docroot/genomes/code/fasta_checker.pl'

input_file = sys.argv[1]
mail_address = sys.argv[2]

checked_file = input_file[:input_file.rfind('.')] + '_checked' + input_file[input_file.rfind('.'):]

clear_errors = subprocess.Popen(['rm', 'tmp/fasta_errors.txt'])
clear_errors.wait()



# PERFORM A FASTA CHECK
# print './run_with_profile.sh -q short -K -W 1 -o ' + checked_file + ' -e tmp/errors.txt perl ' + fastaChecker +' '+ input_file +' 0 2>tmp/fasta_errors.txt'



process_fastaCheck = subprocess.Popen(['/bin/bash', '-c',
                                       './run_with_profile.sh -q short -K -W 1 -o ' + checked_file + ' -e tmp/fasta_errors.txt perl ' + fastaChecker + ' ' + input_file + ' 0 2>tmp/errors.txt'])

process_fastaCheck.wait()  # wait for fasta to finish before continuing


# CHECK IF ITS OK TO CONTINUE
with open('tmp/fasta_errors.txt', "r") as fastaErrors:
    if fastaErrors.readline():
        fastaErrors.seek(0, 0)
        errorStr = fastaErrors.read()
        send_email("Fasta file improperly formatted: \n" + errorStr, mail_address, []);
        sys.exit(0);


# CHANGE INTO MINING DIRECTORY
try:
    os.chdir('mining')
except OSError:
    print "Error, couldn't get into directory mining"
    sys.exit(0)


# THE OUTSTRING
outstr = "Fasta is in proper format \n"

# FILES TO BE ATTACHED
outfiles = []

# CONSTANTS

too_short = 30
too_long = 30000


# TOOLS
addLengths = 'add_lengths.py'
getLongShort = 'get_longest_and_shortest.py'
getLenDist = 'get_length_distribution.py'
getTooLongTooShort = 'get_too_long_too_short.py'
getSimpleStats = 'get_simple_stats.py'
graphMe = 'graph_ordered_pairs.py'




# ADD LENGTHS TO THE FILE

file_with_lengths = checked_file[:checked_file.rfind('.')] + '_lengths' + checked_file[checked_file.rfind('.'):]

process_addLengths = subprocess.Popen(['/bin/sh', '-c',
                                       '../run_with_profile.sh -q short -K -W 1 python ' + addLengths + ' ../' + checked_file + ' ../' + file_with_lengths])
process_addLengths.wait()

# GET LONG AND SHORT SEQS



long_short = input_file[:input_file.rfind('.')] + '_long_short' + input_file[input_file.rfind('.'):]

process_longShort = subprocess.Popen(['/bin/sh', '-c',
                                      '../run_with_profile.sh -q short -K -W 1 python ' + getLongShort + ' ../' + file_with_lengths + ' ../' + long_short])


# GET LENGTH DISTRIBUTION

len_dist = 'tmp' + input_file[input_file.rfind('/'):] + '.hist'

process_lenDistribution = subprocess.Popen(['/bin/sh', '-c',
                                            '../run_with_profile.sh -q short -K -W 1 python ' + getLenDist + ' ../' + file_with_lengths + ' ' + len_dist + ' 100'])


# GET SEQUENCES THAT ARE TOO SHORT AND TOO LONG

too_s_too_l = input_file[:input_file.rfind('.')] + '_bad_length' + input_file[input_file.rfind('.'):]

process_badLength = subprocess.Popen(['/bin/sh', '-c',
                                      '../run_with_profile.sh -q short -K -W 1 python ' + getTooLongTooShort + ' ../' + file_with_lengths + ' ../' + too_s_too_l + ' ' + str(
                                          too_short) + ' ' + str(too_long)])

# JUST SOME SIMPLE STATS

simple_stats = input_file + '.stat'

process_simple = subprocess.Popen(['/bin/sh', '-c',
                                   '../run_with_profile.sh -q short -K -W 1 python ' + getSimpleStats + ' ../' + file_with_lengths + ' ../' + simple_stats])





# -------PULLING ANALYSIS-------


# PROCESS SIMPLE

process_simple.wait()

with open('../' + simple_stats, "r") as stream_simp:
    outstr += '\n' + stream_simp.read()

# LONGEST?SHORTEST
process_longShort.wait()

with open('../' + long_short, "r") as stream_long_short:
    outstr += '\n' + stream_long_short.read()


# TOO LONG TOO SHORT
process_badLength.wait()

with open('../' + too_s_too_l, "r") as stream_too_s_too_l:
    outstr += '\n' + stream_too_s_too_l.read()



# WAIT FOR LENGTH DIST. TO FINISH
process_lenDistribution.wait()

# GRAPH IT
process_graph = subprocess.Popen(['python', graphMe, len_dist], stderr=open("err.log", "w"))
process_graph.wait()
outfiles.append(len_dist + '.png')



# SEND EMAIL WITH RESULTS
send_email(outstr, mail_address, outfiles)
