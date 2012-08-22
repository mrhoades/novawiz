import abc
from command_base import CommandBase

class ImageBuild(CommandBase):

  @staticmethod
  def name():        return 'image-build'
  @staticmethod
  def description(): return 'build an image'

  @staticmethod
  def help():
    return """
  novawiz image-build

  Usage: novawiz image-build --TODO
"""

  def init(self, args):
    return

  def run(self):
    return

