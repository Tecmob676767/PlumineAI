# Plumine AI

> **The World's Most Advanced Autonomous On-Device AI Assistant.**

Plumine AI is a standalone, hyper-intelligent on-device AI system with direct hardware and Windows OS authority, featuring a futuristic glassmorphic holographic user interface and a zero-latency custom neural engine (free of third-party cloud API dependencies).

---

## Capabilities & Native Controls

- **Application Lifecycle**: Launch and terminate any Windows program (`open chrome`, `open notepad`, `close notepad`)
- **Kernel Command Execution**: Execute arbitrary PowerShell scripts and commands directly (`run command Get-Process`)
- **Filesystem Authority**: Create, view, list, and delete files (`create file notes.txt with Hello`, `read file notes.txt`, `list files`)
- **System Telemetry**: Real-time CPU, RAM, Disk, and Battery diagnostics (`system info`)
- **Audio & Media Hardware**: Full volume modulation and mute control (`volume up`, `volume down`, `mute`)
- **Clipboard Buffer**: Read and modify system clipboard (`show clipboard`, `copy to clipboard <text>`)
- **Workstation Security**: Instant device locking (`lock screen`)
- **Web Navigation**: Quantum search and URL dispatch (`search for quantum computing`, `visit github.com`)
- **Mathematical Intelligence**: Real-time calculation and symbolic reasoning
- **Speech Recognition**: Hands-free voice commands via microphone integration

---

## Architecture

- **`device_actions.py`**: Direct Windows API, PowerShell, and process controls.
- **`ai_engine.py`**: Custom offline intent analyzer, neural memory, and action dispatcher.
- **`server.py`**: High-performance HTTP/REST API server.
- **`index.html`**: Futuristic Cyberpunk HUD with animated holographic orb, real-time telemetry, and particle ambiance.

---

## Launching Plumine AI

Simply double-click `start.bat` or run:

```bash
py server.py
```

The system will initialize and automatically open the holographic HUD at `http://127.0.0.1:7860`.
