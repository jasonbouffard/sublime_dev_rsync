import sublime, sublime_plugin, json, os

class DevRsyncCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        cmd = "rsync"
        projectFolder = view.window().folders()[0]
        projectFile   = projectFolder + '/dev_rsync.json'
        
        # Skip syncing if there is no dev_rsync.json file
        if os.path.exists(projectFile):
            json_data = open(projectFile)
            data = json.load(json_data)
            json_data.close
            
            for option in data['option']:
                cmd += ' --' + option
            
            for exclude in data['exclude']:
                cmd += ' --exclude="' + exclude + '"'

            cmd += ' ' + projectFolder + '/' + ' ' + data['host'] + ':' + data['target_dir'] + '/' + ' &'

            print cmd

            # Execute the rsync command
            os.system(cmd)
