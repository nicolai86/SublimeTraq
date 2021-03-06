import os, sys
import subprocess
import sublime, sublime_plugin
import pprint
import subprocess

class SublimeTraqCommand(sublime_plugin.WindowCommand):
  def run(self):
    view = self.window.active_view()
    self.window.show_input_panel("traq:", "", lambda user_input: self.traq(view, user_input), None, None)

  def traq(self, view, command):
    env_command = ['bash', '-c', 'source $HOME/.traqrc && env']

    proc = subprocess.Popen(env_command, stdout = subprocess.PIPE)

    for line in proc.stdout:
      (key, _, value) = line.decode("utf-8").strip().partition("=")
      os.environ[key] = value

    proc.communicate()

    # TODO validate available commands
    command = "{}/bin/traq {}".format(os.environ["TRAQ_PATH"].strip(), command)
    print(dict(os.environ))
    cmd = [command]

    proc_env = os.environ.copy()
    for k, v in proc_env.items():
      proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True, env=proc_env)
    output = str(process.stdout.read(), "utf-8")

    if len(output) > 0:
      view = self.window.new_file()
      view.run_command('append', {
        'characters': output,
      })

  def is_enabled(self):
    return True
