import os
import re
import time
import novaclient.v1_1 as nc
import paramiko
import subprocess
import paramiko
from cli import log

class Nova:

  def __init__(self):
    self.nova = nc.client.Client(
      os.environ['OS_USERNAME'],
      os.environ['OS_PASSWORD'],
      os.environ['OS_TENANT_NAME'],
      os.environ['OS_AUTH_URL'],
      service_type='compute')


  def boot(self, name, flavor, image, keyname):
    log("booting server " + name)
    server = self.nova.servers.create(name, image, flavor, key_name=keyname)
    return self.wait_for_vm(server)

  def image_by_regexp(self, reg):
    log("searching for image: " + reg)
    images = [ i for i in self.nova.images.list() if re.match(reg, i.name) ]
    if len(images) != 1: raise Exception("bad image regexp : " + reg + " : " + str(images))
    return images[0]

  def image_by_name(self, name):
    return [ i for i in self.nova.images.list() if i.name == name ][0]

  def build_image(self, server, name):
    server.create_image(name)
    self.wait_for_image(name)


  def wait_for_image(self, image_name):
    i = self.image_by_name(image_name)
    if not i: raise Exception('image was not saved')
    while re.match('SAVING', i.status):
      print('.'),
      time.sleep(1)
      i = self.image_by_name(image_name)
    print ''
    if not re.match('ACTIVE', i.status): raise Exception('failed to create image')

  def flavor(self, flavor_name):
    log("searching for flavor: " + flavor_name)
    flavors = [ f for f in self.nova.flavors.list() if f.name == flavor_name ]
    return flavors[0]

  def get_server(self, name):
    return [ s for s in self.nova.servers.list() if s.name == name ][0]

  def wait_for_vm(self, server):
    h = self.get_server(server.name)
    while re.match('BUILD', h.status):
      print('.'),
      time.sleep(1)
      h = self.get_server(server.name)
      if re.match('ERROR', h.status): raise Exception("failed to create host {0}".format(host.name))
    for i in range(60):
      print('.'),
      time.sleep(1)
    print('')
    return h

  def public_ip(self, server):
    return server.addresses['private'][1]['addr']

  def scp(self, ip, user, key_file, src, dest):
    cmd = "scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {0} ".format(key_file)
    cmd = cmd + src + " " + user + "@" + ip + ":" + dest
    print "Running \"{0}\"".format(cmd)
    o = open('/dev/null', 'w')
    i = open('/dev/null', 'r')
    subprocess.call(cmd, shell=True, stdout=o, stderr=o, stdin=i)
    o.close()
    i.close()

  def delete_server(self, server):
    server.delete()

  def delete_key(self, name):
    kpmgr = nc.keypairs.KeypairManager(self.nova)
    k = [ k for k in kpmgr.list() if k.name == name ][0]
    k.delete()

  def create_key(self, name):
    key_file = "/tmp/{0}.pem".format(name)
    log('saving key {0} to {1}'.format(name, key_file))
    kpmgr = nc.keypairs.KeypairManager(self.nova)
    keypair = kpmgr.create(name)
    f = open(key_file, 'w')
    f.write(keypair.private_key)
    f.close()
    os.chmod(key_file, 0600)
    return key_file

  def run_cmd(self, host, key_file, cmd, expect_status=0):
    """
        run cmd on host via ssh using keyfile.
        if the result of the command is different
        than expect_status, raise an exception.
    """
    print "Running \"{0}\" on {1}".format(cmd, host)
    cmd = cmd.replace('"', '\"')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy()) # ignore unknown hosts
    ssh.connect(host, username='ubuntu', key_filename=key_file, password='')
    chan = ssh.get_transport().open_session()
    chan.exec_command(cmd)
    stdin = chan.makefile('wb')
    stdout = chan.makefile('rb')
    stderr = chan.makefile_stderr('rb')
    status = chan.recv_exit_status()
    if status != expect_status:
        raise Exception("command failed ({0}) on host {1}: {2}\n{3}".format(status, host, cmd, ''.join(stdout.readlines() + stderr.readlines())))
    ssh.close()

