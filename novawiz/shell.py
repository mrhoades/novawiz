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

def usage():
  print >> sys.stderr,"foo"
  exit(1)

def main():
  if len(sys.argv) <= 1:    usage()
  if not cmds[sys.argv[1]]: usage()
  cmd = cmds[sys.argv[1]]()
  try:
    cmd.init(sys.argv[2:])
  except BadArgs:
    print >> sys.stderr, "invalid arguments.\n\n"
    print >> sys.stderr, cmd.usage()
    exit(1)
  cmd.run()

if __name__ == "__main__":
  main()
