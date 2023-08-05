import npyscreen
import psutil
import sys
from collections import defaultdict


class ProcessList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ProcessList, self).__init__(*args, **keywords)
        self.add_handlers({
            "q": self.when_exit,
            "K": self.when_kill_process
        })

    def display_value(self, vl):
        pid = vl['pid']
        name = vl['name']
        create_time = vl['create_time'] if vl['create_time'] else ''
        username = vl['username'] if vl['username'] else ''
        return "{:<10} {:<30} {:<20} {:<20}".format(pid, name, create_time, username)

    def when_exit(self, *args, **keywords):
        self.parent.parentApp.switchForm(None)

    def when_kill_process(self, *args, **keywords):
        selected_value = self.values[self.cursor_line]
        if isinstance(selected_value, dict):
            pid = selected_value['pid']
            try:
                p = psutil.Process(pid)
                p.terminate()
                npyscreen.notify_confirm(f"Process {pid} terminated.", title="Success")
            except psutil.NoSuchProcess:
                npyscreen.notify_confirm(f"No such process with PID {pid}.", title="Error")
            except psutil.AccessDenied:
                npyscreen.notify_confirm(f"Access denied to terminate process with PID {pid}.", title="Error")
        else:
            npyscreen.notify_confirm("Please select a process to terminate.", title="Error")


class ProcessListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ProcessList

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        processes = []
        header = {'pid': 'PID', 'name': 'Name', 'create_time': 'Create Time', 'username': 'Username'}
        processes.append(header)
        for process in psutil.process_iter():
            try:
                process_info = process.as_dict(attrs=['pid', 'name', 'username', 'create_time', 'cpu_percent'])
                if len(sys.argv) > 1:
                    if sys.argv[1] in process_info['name']:
                        processes.append(process_info)
                else:
                    processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        processes.pop(0)
        processes.sort(key=lambda x: x['create_time'] if x['create_time'] else 0, reverse=True)
        processes.insert(0, header)
        self.wMain.values = processes[:26]
        self.wMain.display()


class ProcessListApplication(npyscreen.NPSAppManaged):
    keypress_timeout_default = 10

    def onStart(self):
        self.addForm("MAIN", ProcessListDisplay)


if __name__ == '__main__':
    app = ProcessListApplication()
    app.run()
