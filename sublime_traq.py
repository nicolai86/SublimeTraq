import os, sys
import subprocess
import sublime, sublime_plugin
import os
import pprint
import subprocess

class SublimeTraqCommand(sublime_plugin.WindowCommand):
  def run(self):
    command = ["bash", "-c",  ". {0}/.bash_profile && env".format(os.environ["HOME"])]
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)

    for line in proc.stdout:
      (key, _, value) = str(line, "utf-8").partition("=")
      os.environ[key] = value

    proc.communicate()

    pprint.pprint(dict(os.environ))
    cmd = ["cd {} && {}/bin/traq".format(os.environ["HOME"], os.environ["TRAQ_PATH"].rstrip("\n")), "-p shisha", "-m 10"]
    # proc_env = os.environ.copy()

    # for k, v in proc_env.items():
    #   proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

    # project_path = self.window.folders()[0]
    # cmd = "$HOME/.traq/bin/traq"
    pprint.pprint(cmd)
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = p.stdout.read()
    pprint.pprint(output)

    # sublime.message_dialog(str(output, "utf-8"))

  def is_enabled(self):
    return True
