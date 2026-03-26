#!/usr/bin/env python3
"""
Taskify Phase III - Startup Script

This script starts both the FastAPI backend and the MCP server simultaneously.
"""

import asyncio
import subprocess
import sys
import threading
import time
import signal
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def start_fastapi_server():
    """Start the FastAPI server using uvicorn."""
    import uvicorn
    from backend.src.main import app

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def start_mcp_server():
    """Start the MCP server."""
    from backend.src.api.mcp_server import serve_mcp

    asyncio.run(serve_mcp())

def main():
    """Main function to start both servers."""
    print("🚀 Starting Taskify Phase III servers...")
    print("   - FastAPI Backend: http://localhost:8000")
    print("   - MCP Server: http://localhost:3000")

    # Start FastAPI server in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi_server, name="FastAPI-Server")
    fastapi_thread.daemon = True
    fastapi_thread.start()

    # Give FastAPI a moment to start
    time.sleep(2)

    # Start MCP server in the main thread (or another thread if preferred)
    try:
        start_mcp_server()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Taskify Phase III servers...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()