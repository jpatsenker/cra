import subprocess


def srun(command, error, output, queue, timelim, wait):
    full_command = "slurm -p " + queue + " -t " + str(timelim) + " -o " + output + " -e " + error + " " + command
    proc = subprocess.Popen([full_command])
    if wait:
        proc.wait()
    return proc