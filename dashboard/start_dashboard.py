#!/usr/bin/env python3
"""
Script to start both the static web server and the API server for AQUA_SENSE Dashboard.
"""
import subprocess
import sys
import os
def main():
    print("=" * 50)
    print("🚀 Starting AQUA_SENSE Dashboard")
    print("=" * 50)
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Start API server (port 7070)
    print("\n📡 Starting API server on port 7070...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "manager.api_server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    # Start static file server (port 8080)
    print("🌐 Starting web server on port 8080...")
    web_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    print("\n✅ Servers started successfully!")
    print("   - Dashboard: http://localhost:8080")
    print("   - API:       http://localhost:7070")
    print("\n💡 Press Ctrl+C to stop both servers\n")
    try:
        # Wait for both processes
        while True:
            api_output = api_process.stdout.readline()
            web_output = web_process.stdout.readline()
            if api_output:
                print(f"[API] {api_output.strip()}")
            if web_output:
                print(f"[WEB] {web_output.strip()}")
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        api_process.terminate()
        web_process.terminate()
        print("✅ Done!")
if __name__ == "__main__":
    main()