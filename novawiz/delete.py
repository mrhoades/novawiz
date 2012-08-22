import abc
from command_base import CommandBase
from cli import *

class Delete(CommandBase):

  @staticmethod
  def name():        return 'delete'
  @staticmethod
  def description(): return 'delete an instance'

  @staticmethod
  def help():
    return """
  novawiz delete

  Usage: novawiz delete
"""

  def init(self, args):
    pass

  def run(self):
    opts = {'node': prompt("enter the node name or id from above to destroy", "list") }
    if not confirm(opts, "are you sure you want to delete this node?"):
      print colors.RED + "not confirmed. starting over..." + colors.END + "\n\n"
      return self.run()
    run_cmd(["nova", "delete", opts['node']])

