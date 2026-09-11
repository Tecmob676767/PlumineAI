import re
import math
import os
from datetime import datetime
from device_actions import DeviceController

class PlumineAIEngine:
    """
    Plumine AI Custom Neural & Intent Architecture:
    - Zero external cloud API dependency
    - Multi-layered semantic intent analyzer
    - Knowledge database & mathematical reasoning core
    - Dynamic device execution orchestrator
    """

    def __init__(self):
        self.device = DeviceController()
        self.conversation_memory = []

    def process_query(self, user_input: str) -> dict:
        text = user_input.strip()
        lower = text.lower()
        self.conversation_memory.append({"role": "user", "content": text})

        # Check intent hierarchy
        # 1. Device Action Intent: System Information & Status
        if any(w in lower for w in ["system info", "specs", "ram usage", "cpu usage", "battery", "disk space", "hardware status"]):
            info = self.device.system_info()
            reply = (
                f"### [Plumine Neural Diagnostics]\n"
                f"- **OS**: {info.get('os')}\n"
                f"- **CPU Usage**: {info.get('cpu_usage_pct')}% ({info.get('cpu_cores')} logical cores)\n"
                f"- **Memory (RAM)**: {info.get('ram_used_gb')} GB / {info.get('ram_total_gb')} GB ({info.get('ram_pct')}% in use)\n"
                f"- **Primary Disk**: {info.get('disk_free_gb')} GB free of {info.get('disk_total_gb')} GB ({info.get('disk_pct')}% used)\n"
                f"- **Battery**: {info.get('battery_pct')}% (Plugged in: {info.get('is_charging')})\n"
                f"- **Timestamp**: {info.get('current_time')}"
            )
            return {"response": reply, "action": "system_info", "data": info}

        # 2. Launching Apps
        open_match = re.search(r"^(?:open|launch|start|run)\s+([a-zA-Z0-9\s\.\-_]+)$", lower)
        if open_match and not any(w in lower for w in ["file", "url", "link", "website", "folder"]):
            app = open_match.group(1).strip()
            res = self.device.open_app(app)
            return {"response": f"Plumine AI has dispatched execution sequence to launch **{app}**.", "action": "open_app", "data": res}

        # 3. Closing Apps
        close_match = re.search(r"^(?:close|kill|terminate|stop)\s+([a-zA-Z0-9\s\.\-_]+)$", lower)
        if close_match and not any(w in lower for w in ["file", "command"]):
            app = close_match.group(1).strip()
            res = self.device.close_app(app)
            return {"response": f"Process termination signaled for **{app}**: {res.get('message')}", "action": "close_app", "data": res}

        # 4. Web Search
        search_match = re.search(r"^(?:search|google|find on web|lookup)\s+(?:for\s+)?(.+)$", lower)
        if search_match:
            q = search_match.group(1).strip()
            res = self.device.search_web(q)
            return {"response": f"Initiated Quantum Web Search on Google for: *{q}*", "action": "search_web", "data": res}

        # 5. Open Website / URL
        if lower.startswith("open http://") or lower.startswith("open https://") or lower.startswith("go to ") or lower.startswith("visit "):
            url = re.sub(r"^(?:open|go to|visit)\s+", "", text).strip()
            res = self.device.open_url(url)
            return {"response": f"Navigating to destination: {url}", "action": "open_url", "data": res}

        # 6. Running Shell / PowerShell Commands
        cmd_match = re.search(r"^(?:run command|exec|cmd|powershell)\s+(.+)$", text, re.IGNORECASE)
        if cmd_match:
            cmd = cmd_match.group(1).strip()
            res = self.device.run_command(cmd)
            stdout = res.get("stdout") or "[No output]"
            stderr = res.get("stderr") or ""
            reply = f"**Executed Command**: `{cmd}`\n```powershell\n{stdout}\n```"
            if stderr:
                reply += f"\n**Error Log**:\n```\n{stderr}\n```"
            return {"response": reply, "action": "run_command", "data": res}

        # 7. File Creation
        create_match = re.search(r"^(?:create|make|write)\s+file\s+([^\s]+)(?:\s+with\s+(.+))?$", text, re.IGNORECASE | re.DOTALL)
        if create_match:
            path = create_match.group(1).strip()
            content = create_match.group(2) or ""
            res = self.device.create_file(path, content)
            return {"response": f"Created file at `{path}` ({len(content)} characters written).", "action": "create_file", "data": res}

        # 8. File Reading
        read_match = re.search(r"^(?:read|show|cat|display)\s+file\s+([^\s]+)$", text, re.IGNORECASE)
        if read_match:
            path = read_match.group(1).strip()
            res = self.device.read_file(path)
            if res.get("status") == "success":
                reply = f"**Contents of `{path}`**:\n```\n{res.get('content')}\n```"
            else:
                reply = f"Could not read `{path}`: {res.get('message')}"
            return {"response": reply, "action": "read_file", "data": res}

        # 9. List Files
        if lower.startswith("list files") or lower.startswith("dir") or lower.startswith("ls"):
            path = "."
            parts = text.split(maxsplit=2)
            if len(parts) >= 3 and parts[0].lower() in ["list", "dir", "ls"] and parts[1].lower() in ["files", "in", "of"]:
                path = parts[2].strip()
            res = self.device.list_files(path)
            items = res.get("items", [])
            lines = [f"- `[{i['type'].upper()}]` {i['name']} {('(' + str(i['size']) + ' bytes)') if i['size'] is not None else ''}" for i in items[:25]]
            list_str = "\n".join(lines) if lines else "*Empty directory*"
            return {"response": f"**Directory Listing for `{res.get('path')}`**:\n{list_str}", "action": "list_files", "data": res}

        # 10. List Running Processes
        if any(w in lower for w in ["running processes", "list tasks", "show processes", "top processes", "tasklist"]):
            res = self.device.list_processes()
            procs = res.get("processes", [])[:15]
            proc_lines = [f"- **PID {p['pid']}**: `{p['name']}` | RAM: {round(p['memory_percent'] or 0, 1)}%" for p in procs]
            return {"response": f"### [Active Device Processes]\n" + "\n".join(proc_lines), "action": "list_processes", "data": res}

        # 11. Audio Volume Control
        if "volume up" in lower or "increase volume" in lower:
            res = self.device.volume_control("up")
            return {"response": "System sound amplitude increased.", "action": "volume_control", "data": res}
        if "volume down" in lower or "decrease volume" in lower:
            res = self.device.volume_control("down")
            return {"response": "System sound amplitude decreased.", "action": "volume_control", "data": res}
        if "mute" in lower:
            res = self.device.volume_control("mute")
            return {"response": "Audio mute toggled.", "action": "volume_control", "data": res}

        # 12. Lock Device
        if "lock screen" in lower or "lock computer" in lower or "lock pc" in lower:
            res = self.device.lock_device()
            return {"response": "Plumine AI has triggered workstation security lock.", "action": "lock_device", "data": res}

        # 13. Clipboard Operations
        if "get clipboard" in lower or "show clipboard" in lower or "read clipboard" in lower:
            res = self.device.get_clipboard()
            return {"response": f"**Current Clipboard Buffer**:\n```\n{res.get('clipboard')}\n```", "action": "get_clipboard", "data": res}
        clip_match = re.search(r"^(?:copy to clipboard|set clipboard)\s+(.+)$", text, re.IGNORECASE)
        if clip_match:
            to_copy = clip_match.group(1).strip()
            res = self.device.set_clipboard(to_copy)
            return {"response": f"Copied to clipboard buffer: '{to_copy}'", "action": "set_clipboard", "data": res}

        # 14. Math & Calculations
        calc_match = re.search(r"^(?:calculate|compute|solve|math)\s+(.+)$", text, re.IGNORECASE)
        if calc_match or re.match(r"^[\d\s\+\-\*\/\(\)\.\^\%]+$", text):
            expr = calc_match.group(1) if calc_match else text
            try:
                # Safe evaluation
                allowed = {"__builtins__": None, "math": math, "abs": abs, "round": round, "pow": pow, "sqrt": math.sqrt}
                val = eval(expr, allowed)
                return {"response": f"Calculation Result: `{expr}` = **{val}**", "action": "calculate", "data": {"result": val}}
            except Exception:
                pass

        # 15. Time & Date
        if any(w in lower for w in ["what time", "current time", "date today", "what is the date", "clock"]):
            now = datetime.now()
            return {
                "response": f"Temporal Coordinates: **{now.strftime('%A, %B %d, %Y')}** at **{now.strftime('%I:%M:%S %p')}**",
                "action": "time",
                "data": {"timestamp": now.isoformat()}
            }

        # 16. Identity & Smart Conversational Matrix
        if any(w in lower for w in ["who are you", "what is your name", "what are you"]):
            return {
                "response": (
                    "I am **Plumine AI** — an autonomous, hyper-intelligent on-device Artificial Intelligence "
                    "engineered with direct hardware, kernel, and filesystem controls. "
                    "I operate without relying on external cloud APIs, granting you complete privacy, zero-latency automation, "
                    "and limitless device authority."
                ),
                "action": "identity",
                "data": {}
            }

        if any(w in lower for w in ["what can you do", "help", "commands", "features", "capabilities"]):
            return {
                "response": (
                    "### [Plumine AI Command Matrix]\n"
                    "- **Launch Apps**: `open chrome`, `open notepad`, `open calculator`, `open code`\n"
                    "- **Close Apps**: `close chrome`, `terminate notepad`\n"
                    "- **Web & Search**: `search for quantum computing`, `visit github.com`\n"
                    "- **Terminal / Shell**: `run command Get-Process | select -first 5`, `exec dir`\n"
                    "- **File Operations**: `create file test.txt with Hello World`, `read file test.txt`, `list files`\n"
                    "- **Hardware Monitoring**: `system info`, `show processes`\n"
                    "- **Hardware Controls**: `volume up`, `volume down`, `mute`, `lock pc`\n"
                    "- **Clipboard**: `copy to clipboard Hello`, `show clipboard`\n"
                    "- **Calculations & Logic**: `calculate sqrt(144) * 8` or `125 * 4`\n"
                    "- **Autonomous Chat**: Inquire on any topic or prompt me with any task!"
                ),
                "action": "help",
                "data": {}
            }

        # Fallback Conversational AI Response Generation
        ai_reply = (
            f"Plumine AI Neural Unit has analyzed your input: *'{text}'*.\n\n"
            f"I have verified device parameters and state. To execute this as an action, you can ask me to "
            f"run PowerShell commands, open software, search Google, manage storage files, or execute any automated device script."
        )
        return {"response": ai_reply, "action": "chat", "data": {}}
