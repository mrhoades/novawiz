import abc

class CommandBase(object):
  __metaclass__ = abc.ABCMeta

  @staticmethod
  @abc.abstractmethod
  def name():
    # name of this command
    return

  @staticmethod
  @abc.abstractmethod
  def description():
    # description of this command
    return

  @staticmethod
  @abc.abstractmethod
  def help():
    # help string
    return

  @abc.abstractmethod
  def init(self, args):
    # initialize command from args, or raise on bad args
    return

  @abc.abstractmethod
  def run(self):
    # run the command
    return

class BadArgs(Exception):
  pass
