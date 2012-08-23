import sys
import subprocess

from command_base import BadArgs
from boot import Boot
from delete import Delete
from image_build import ImageBuild

cmd_classes = [
  Boot,
  Delete,
  ImageBuild
]

cmds = {}
for klass in cmd_classes:
  cmds[klass.name()] = klass

def pad(s, l):
  while len(s) < l:
    s = s + ' '
  return s

def usage():
  print >> sys.stderr, "for help on a subcommand, run `novawiz help <command>`\n"
  print >> sys.stderr, "commands:"
  for klass in cmd_classes:
    print >> sys.stderr, "  " + pad(klass.name(), 20) + "- " + klass.description()
  exit(1)

def main():
  if len(sys.argv) <= 1:    usage()
  if sys.argv[1] == 'help':
    if len(sys.argv) > 2 and cmds[sys.argv[2]]:
      print >> sys.stderr, cmds[sys.argv[2]].help()
      exit(1)
    else: usage()
  if not cmds[sys.argv[1]]: usage()
  cmd = cmds[sys.argv[1]]()
  try:
    cmd.init(sys.argv[2:])
  except BadArgs as e:
    print >> sys.stderr, "invalid arguments: " + e.message + "\n\n"
    print >> sys.stderr, cmd.help()
    exit(1)
  cmd.run()

if __name__ == "__main__":
  main()
