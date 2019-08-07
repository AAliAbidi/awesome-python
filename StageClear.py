#!/usr/bin/python 

#PBS -l nodes=2:ppn=2
#PBS -l mem=512MB
#PBS -l walltime=00:10:00
#PBS -N myStage_clear

import os
import random
import string 
import subprocess
import signal 
import time 
import sys

### Exporting License and Environ Variable 

os.environ["ALTAIR_LICENSE_PATH"]="6200@licsrv"
#os.environ["I_MPI_FABRICS"]="shm:ofa"
os.environ["RADFLEX_PATH"]="/apps/2017/altair/hwsolvers/common/bin/linux64"
os.environ["LD_LIBRARY_PATH"]="/apps/2017/altair/hwsolvers/optistruct/bin/linux64/:/apps/2017/altair/hwsolvers/common/bin/linux64"

os.chdir(os.environ['PBS_O_WORKDIR'])

###Create Local scratch
lscratch_root='/lscratch'
thislscratch=lscratch_root+"/"+os.environ['USER']+"/"+''.join(os.environ ['PBS_JOBID'])

def createDir():
  try:
    thisnodes=open(os.environ['PBS_NODEFILE']).read().split()
    for thisnode in set(thisnodes):
      dircreate="ssh " + thisnode + " mkdir -p  " + thislscratch
      subprocess.call(dircreate,shell=True)
  except:
    print "Cannot create directory %s" %(thislscratch)
    sys.exit(1)
 
  os.environ['TMPDIR']=thislscratch
  os.environ['TEMP'] = os.environ['TMPDIR'] 


### Command line 
cmd = '/apps/2017/altair/scripts/optistruct -np 2 -hostfile ' +os.environ['PBS_NODEFILE']+ ' -scr ' +thislscratch+' '+os.path.basename(os.getcwd()+"/runScript/beam.fem")+' '+ '-ddm'
print cmd
print "\nMy working Dir\n"
print os.environ['PBS_O_WORKDIR']
print "\nOs.getcwd() output\n"
print os.getcwd()
print os.environ['PBS_JOBID']




#Remove scratch directory
def removeDir():
  try:
    thisnodes=open(os.environ['PBS_NODEFILE']).read().split()
    for thisnode in set(thisnodes):
      dirdel="ssh " + thisnode + " rm -r " + thislscratch  
      subprocess.call(dirdel,shell=True)
  except:
    print "Cannot create directory %s" %(thislscratch)
    sys.exit(1)
 


### Function to trap and remove files 
def signalHandler(signum, frame):
  print "signal caught"
  thisnodes=open(os.environ['PBS_NODEFILE']).read().split()
  for thisnode in set(thisnodes):
    dirdel="ssh " + thisnode + " rm -r " + thislscratch
    subprocess.call(dirdel,shell=True)
  sys.exit(1)
signal.signal(signal.SIGTERM, signalHandler)


def main():
  createDir()
  solver = subprocess.Popen(cmd, shell=True)
  retval = solver.wait();
  removeDir()
  #signal.signal(signal.SIGTERM, signalHandler)
  print "Terminated signal"
  for i in range(1,5):
    print i
    time.sleep(1)

if __name__ == "__main__":
    main()

