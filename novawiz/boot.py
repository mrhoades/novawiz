import abc
from command_base import CommandBase
from cli import *

class Boot(CommandBase):

  @staticmethod
  def name():        return 'boot'
  @staticmethod
  def description(): return 'boot an instance'

  @staticmethod
  def help():
    return """
  novawiz boot

  Usage: novawiz boot"""

  def init(self, args):
    pass

  def run(self):
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
      return self.run()
    run_cmd(["nova", "boot", "--flavor", opts['flavor'], "--image", opts['image'], "--key_name", opts['key'], opts['name'], "--security_groups", opts['secgroup'], "--availability_zone", opts['zone']])

