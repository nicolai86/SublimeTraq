import os, sys
import subprocess
import sublime, sublime_plugin
import pprint
import subprocess

class SublimeTraqCommand(sublime_plugin.WindowCommand):
  def run(self):
    command = "{}/bin/traq -p example -m 10".format(os.environ["TRAQ_PATH"])
    cmd = [command]

    proc_env = os.environ.copy()
    for k, v in proc_env.items():
      proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True, env=proc_env)
    output = process.stdout.read()
    pprint.pprint(output)

    sublime.message_dialog(str(output, "utf-8"))

  def is_enabled(self):
    return True
