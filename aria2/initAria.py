import os
import subprocess
import threading
from infi.systray import SysTrayIcon
import http.server
import socketserver


def restart_aria2c(systray):
    global aria2c_process
    aria2c_process.terminate()
    aria2c_process = subprocess.Popen(["aria2c.exe", "--enable-rpc", "--rpc-listen-all"])


def on_quit(systray):
    aria2c_process.terminate()
    httpd.shutdown()


if not os.path.exists("D:\\Aria2Data"):
    os.makedirs("D:\\Aria2Data")

aria2c_process = subprocess.Popen(["aria2c.exe", "--enable-rpc", "--rpc-listen-all"])

menu_options = (("Restart", None, restart_aria2c),)
systray = SysTrayIcon("icon.ico", "Aria2c", menu_options, on_quit=on_quit)

PORT = 8800
os.chdir("webui-aria2\\docs")
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)


def start_server():
    print(f"Serving at port {PORT}")
    httpd.serve_forever()


server_thread = threading.Thread(target=start_server)
server_thread.start()

systray.start()
