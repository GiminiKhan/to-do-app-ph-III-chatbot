"""Taskify Phase III - Startup Script

This script starts the FastAPI backend server for Taskify Phase III.
The MCP server needs to be started separately if required.
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
backend_src = project_root / "backend" / "src"
sys.path.insert(0, str(backend_src.parent.parent))

def main():
    """Main function to start the FastAPI server."""
    print("🚀 Starting Taskify Phase III backend server...")
    print("   - FastAPI Backend: http://localhost:8000")
    print("   - API Documentation: http://localhost:8000/docs")
    print("\nTo start the MCP server separately, run:")
    print("   python -m backend.src.api.mcp_server")
    print("")

    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    main()