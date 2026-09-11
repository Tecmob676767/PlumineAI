@echo off
title Plumine AI - Autonomous Operating System
color 0b
echo ========================================================
echo         INITIALIZING PLUMINE AI NEURAL CORE
echo ========================================================
echo Checking dependencies...
py -m pip install psutil --quiet
echo Starting Plumine Server...
py server.py
pause
