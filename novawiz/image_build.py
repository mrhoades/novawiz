import abc
import argparse
from command_base import CommandBase, BadArgs
from cli import *
from nova import Nova
import os
import time

class ImageBuild(CommandBase):

  @staticmethod
  def name():        return 'image-build'
  @staticmethod
  def description(): return 'build an image'

  @staticmethod
  def help():
    return """
  novawiz image-build

  Usage: novawiz image-build [ --base_image         <image-name-regexp>      ]
                             [ --name               <new-image-name          ]
                             [ --install_script     <path-to-install-script> ]
                             [ --install_script-url <url of install script>  ]
"""

  def init(self, args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_image', dest='base_image')
    parser.add_argument('--install_script', dest='install_script')
    parser.add_argument('--install_script_url', dest='install_script_url')
    parser.add_argument('--name', dest='name')
    self.opts = parser.parse_args(args)
    if (not self.opts.base_image) or (not self.opts.name) or (not (self.opts.install_script or self.opts.install_script_url)):
      raise BadArgs('must provide --base_image, --name, and either (--install_script or --install_script_url)')
    return

  def temp_name(self):
    now = str(int(time.time()))
    return "novawiz_" + now

  def run(self):
    nova = Nova()

    node_name = key_name = self.temp_name()
    key_file = nova.create_key(key_name)

    base_image = nova.image_by_regexp(self.opts.base_image)

    s = nova.boot(node_name, nova.flavor('standard.xsmall'), base_image, key_name)
    ip = nova.public_ip(s)

    if self.opts.install_script_url:
      log("fetching " + self.opts.install_script_url)
      self.opts.install_script = "/tmp/" + node_name + '_install'
      run_cmd(['curl', '-o', self.opts.install_script, self.opts.install_script_url])

    nova.scp(ip, "ubuntu", key_file, self.opts.install_script, '/tmp/novawiz_install')
    nova.run_cmd(ip, key_file, "chmod +x {0}".format("/tmp/novawiz_install"))
    nova.run_cmd(ip, key_file, "/tmp/novawiz_install")

    log("building image")
    nova.build_image(s, self.opts.name)

    log("destroying build node")
    nova.delete_keypair(key_name)
    log("destroying temp keypair")
    os.remove(key_file)
    nova.delete_server(s)

