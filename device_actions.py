import os
import sys
import subprocess
import webbrowser
import platform
import shutil
import time
import json
import psutil
from datetime import datetime

class DeviceController:
    """
    Native Windows Device Controller for Plumine AI.
    Executes commands, application controls, filesystem operations, and diagnostics.
    """
    APP_SHORTCUTS = {
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",
        "edge": "msedge.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "paint": "mspaint.exe",
        "task manager": "taskmgr.exe",
        "settings": "start ms-settings:",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "spotify": "spotify.exe",
        "vlc": "vlc.exe",
        "vscode": "code.exe",
        "code": "code.exe"
    }

    @staticmethod
    def open_app(app_name: str) -> dict:
        clean_name = app_name.strip().lower()
        target = DeviceController.APP_SHORTCUTS.get(clean_name, clean_name)
        try:
            if target.startswith("start "):
                subprocess.Popen(["cmd.exe", "/c", target], shell=True)
            else:
                subprocess.Popen(target, shell=True)
            return {"status": "success", "message": f"Successfully launched {app_name}"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to launch {app_name}: {str(e)}"}

    @staticmethod
    def close_app(process_name: str) -> dict:
        name = process_name.strip().lower()
        if not name.endswith(".exe"):
            name += ".exe"
        killed = 0
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == name:
                    proc.terminate()
                    killed += 1
            except Exception:
                continue
        if killed > 0:
            return {"status": "success", "message": f"Closed {killed} instance(s) of {process_name}"}
        return {"status": "warning", "message": f"No active process found matching {process_name}"}

    @staticmethod
    def search_web(query: str) -> dict:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return {"status": "success", "message": f"Searching Google for: {query}"}

    @staticmethod
    def open_url(url: str) -> dict:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        webbrowser.open(url)
        return {"status": "success", "message": f"Opened URL: {url}"}

    @staticmethod
    def run_command(command: str) -> dict:
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Command execution timed out after 30 seconds."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def create_file(path: str, content: str = "") -> dict:
        try:
            target = os.path.expanduser(path)
            parent = os.path.dirname(target)
            if parent and not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "message": f"File created at: {target}", "size": len(content)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def read_file(path: str) -> dict:
        try:
            target = os.path.expanduser(path)
            if not os.path.exists(target):
                return {"status": "error", "message": f"File not found: {target}"}
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(50000)
            return {"status": "success", "path": target, "content": content}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def list_files(path: str = ".") -> dict:
        try:
            target = os.path.expanduser(path)
            if not os.path.exists(target):
                return {"status": "error", "message": f"Directory not found: {target}"}
            items = []
            for item in os.listdir(target):
                full_item = os.path.join(target, item)
                is_dir = os.path.isdir(full_item)
                items.append({
                    "name": item,
                    "type": "directory" if is_dir else "file",
                    "size": os.path.getsize(full_item) if not is_dir else None
                })
            return {"status": "success", "path": os.path.abspath(target), "items": items[:100]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def delete_file(path: str) -> dict:
        try:
            target = os.path.expanduser(path)
            if not os.path.exists(target):
                return {"status": "error", "message": f"Path not found: {target}"}
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
            return {"status": "success", "message": f"Deleted successfully: {target}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def system_info() -> dict:
        try:
            cpu_pct = psutil.cpu_percent(interval=0.2)
            cpu_count = psutil.cpu_count(logical=True)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")
            battery = psutil.sensors_battery()
            
            return {
                "status": "success",
                "os": platform.platform(),
                "cpu_usage_pct": cpu_pct,
                "cpu_cores": cpu_count,
                "ram_total_gb": round(ram.total / (1024**3), 2),
                "ram_used_gb": round(ram.used / (1024**3), 2),
                "ram_pct": ram.percent,
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "disk_pct": disk.percent,
                "battery_pct": battery.percent if battery else "N/A",
                "is_charging": battery.power_plugged if battery else "N/A",
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def list_processes() -> dict:
        try:
            procs = []
            for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = p.info
                    if info['name']:
                        procs.append(info)
                except Exception:
                    continue
            procs.sort(key=lambda x: x.get('memory_percent') or 0, reverse=True)
            return {"status": "success", "processes": procs[:25]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def volume_control(action: str) -> dict:
        cmd = "$wscript = New-Object -ComObject Wscript.Shell; "
        if action.lower() == "up":
            cmd += "$wscript.SendKeys([char]175)"
        elif action.lower() == "mute":
            cmd += "$wscript.SendKeys([char]173)"
        else:
            cmd += "$wscript.SendKeys([char]174)"
        subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        return {"status": "success", "message": f"Volume action executed: {action}"}

    @staticmethod
    def lock_device() -> dict:
        try:
            subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
            return {"status": "success", "message": "Workstation locked successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def set_clipboard(text: str) -> dict:
        try:
            cmd = f'Set-Clipboard -Value @"\n{text}\n"@'
            subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            return {"status": "success", "message": "Copied text to clipboard."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_clipboard() -> dict:
        try:
            res = subprocess.run(["powershell", "-Command", "Get-Clipboard"], capture_output=True, text=True)
            return {"status": "success", "clipboard": res.stdout.strip()}
        except Exception as e:
            return {"status": "error", "message": str(e)}
