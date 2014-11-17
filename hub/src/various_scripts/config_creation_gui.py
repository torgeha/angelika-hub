__author__ = 'David'
import Tkinter as tk
import ConfigParser
import calendar
from datetime import datetime as dt


class ConfigGui:
    def __init__(self, filename):
        self.filename = filename
        self.master = tk.Tk()
        self.fields = [('Hub ID', ""), ('Password', ""),
                       ('Server URL', "https://api.angelika.care/"),
                       ('Server interval', "10"), ('Server wait', "15")]
        self.entries = []
        for i in range(0, len(self.fields)):
            self.entries.append(self.new_input_field(self.fields[i][0], i, self.fields[i][1]))
        self.status_text = tk.StringVar()
        tk.Button(self.master, text="OK", command=self.ok).grid(row=len(self.fields),
                                                                sticky=(tk.E, tk.W))
        status_label = tk.Label(self.master, textvariable=self.status_text)
        status_label.grid(row=len(self.fields), column=1, sticky=(tk.E, tk.W))
        self.master.wait_window()

    def new_input_field(self, description, row, preset=""):
        tk.Label(self.master, text=description).grid(row=row, sticky=tk.E)
        var = tk.StringVar()
        var.set(preset)
        entry = tk.Entry(self.master, textvariable=var, width=50)
        if description == 'Password':
            entry.__setitem__('show', '*')
        entry.grid(row=row, column=1)
        return entry

    def validate_entry(self, name, value):
        if not value:
            return False
        if name == "Server interval" or name == "Server wait":
            try:
                int(value)
            except ValueError:
                return False
        return True

    def write_config(self):
        f = open(self.filename, 'w')
        config = ConfigParser.RawConfigParser()
        config.read(self.filename)
        config.add_section('hub')
        config.add_section('sensors')
        options = ['hub_id', 'password', 'server_url', 'server_interval', 'server_wait']
        for i in range(0, len(options)):
            config.set('hub', options[i], self.entries[i].get())
        config.set('hub', 'last_update', calendar.timegm(dt.utcnow().timetuple()))
        config.set('hub', 'token', '')
        server_url = config.get('hub', 'server_url')
        if server_url[-1] != '/':
            new_url = (server_url + '/')
            config.set('hub', 'server_url', new_url)
        config.write(f)
        f.close()

    def ok(self):
        success = True
        for i in range(0, len(self.fields)):
            if not self.validate_entry(self.fields[i][0], self.entries[i].get()):
                success = False
                break
        if success:
            self.status_text.set('Success')
            self.write_config()
        else:
            self.status_text.set('Error')


if __name__ == "__main__":
    ConfigGui("hub_config.txt")
