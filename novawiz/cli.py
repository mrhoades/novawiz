import subprocess
import sys

class colors:
  OK     = '\033[92m'
  PROMPT = '\033[1;36m'
  RED = '\033[0;31m'
  END = '\033[0m'


def log(msg):
  print msg
  sys.stdout.flush()

def prompt(p, nova_cmd=None):
  if nova_cmd: show_nova(nova_cmd)
  res = raw_input(colors.PROMPT + p + ": " + colors.OK)
  print colors.END
  print "\n"
  print "\n"
  return res

def show_nova(cmd):
  print subprocess.check_output(['nova', cmd])

def confirm(opts, p=None):
  for k in opts.keys():
    print k + ":  " + opts[k]
  if not p:
    p = "is this correct?"
  res = prompt(p + " (y/n)")
  return (res == 'y' or res == 'Y')

def run_cmd(xs):
  print "running:  " + colors.OK + " ".join(xs) + colors.END
  print subprocess.check_output(xs)
