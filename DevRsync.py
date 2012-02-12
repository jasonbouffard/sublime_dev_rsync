import sublime, sublime_plugin
import json, os, subprocess, functools

class DevRsyncCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        cmd = ["rsync"]

        # Check if we're in a proper ST2 project
        if not view.window().folders():
            return

        projectFolder = view.window().folders()[0]
        projectFile   = projectFolder + '/dev_rsync.json'

        # Skip syncing if there is no dev_rsync.json file
        if os.path.exists(projectFile):
            json_data = open(projectFile)
            data      = json.load(json_data)
            json_data.close

            for option in data['option']:
                cmd.append('--' + option)

            for exclude in data['exclude']:
                cmd.append('--exclude="' + exclude + '"')

            cmd.append(projectFolder + '/')
            cmd.append(data['host'] + ':' + data['target_dir'] + '/')

            # Execute the rsync command
            p = subprocess.call(cmd)

            sublime.set_timeout(functools.partial(self.updateStatus, view, 'DevRsync Done!'), 100)

    def updateStatus(self, view, text):
        sublime.status_message(text);
