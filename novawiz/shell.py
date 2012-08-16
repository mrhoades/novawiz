import sys
import subprocess

class colors:
  OK     = '\033[92m'
  PROMPT = '\033[1;36m'
  RED = '\033[0;31m'
  END = '\033[0m'



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

def boot():
  opts = {
    'name':     prompt("enter a name for the instance"),
    'flavor':   prompt("enter a flavor name or id from above", "flavor-list"),
    'image':    prompt("enter an image name or id from above", "image-list"),
    'key':      prompt("enter a keypair name from above", "keypair-list"),
    'secgroup': prompt("enter a security group name", "secgroup-list"),
    'zone':     prompt("enter an availabilty zone (default az-2)")
  }
  if len(opts['zone']) == 0: opts['zone'] = "az-2"
  if not confirm(opts):
    print colors.RED + "not confirmed. starting over..." + colors.END + "\n\n"
    return boot()
  run_cmd(["nova", "boot", "--flavor", opts['flavor'], "--image", opts['image'], "--key_name", opts['key'], opts['name'], "--security_groups", opts['secgroup'], "--availability_zone", opts['zone']])

def destroy():
  opts = {'node': prompt("enter the node name or id from above to destroy", "list") }
  if not confirm(opts, "are you sure you want to delete this node?"):
    print colors.RED + "not confirmed. starting over..." + colors.END + "\n\n"
    return destroy()
  run_cmd(["nova", "delete", opts['node']])

commands = {
  'boot': boot,
  'destroy': destroy
}

def usage():
  print >> sys.stderr, """Usage:
  novawiz boot     - boot a new instance
  novawiz destroy  - destroy an instance"""
  sys.exit(1)



def main():
  if len(sys.argv) != 2:
    usage()
  cmd = sys.argv[1]
  if not cmd in commands.keys():
    usage()
  commands[cmd]()


if __name__ == "__main__":
  main()
