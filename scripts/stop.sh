#!/bin/bash

cd "$(dirname "$0")/.."

if [ -f "app.pid" ]; then
    PID=$(cat app.pid)
    kill $PID 2>/dev/null || true
    rm app.pid
    echo "Service stopped"
else
    echo "Service not running"
