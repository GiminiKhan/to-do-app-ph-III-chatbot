"""Taskify Phase III - MCP Server Startup Script

This script starts the MCP server for Taskify Phase III.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
backend_src = project_root / "backend" / "src"
sys.path.insert(0, str(backend_src.parent.parent))

def main():
    """Main function to start the MCP server."""
    print("🚀 Starting Taskify Phase III MCP server...")
    print("   - MCP Server: http://localhost:3000")
    print("")

    # Import and run the MCP server
    from backend.src.api.mcp_server import serve_mcp

    try:
        asyncio.run(serve_mcp())
    except KeyboardInterrupt:
        print("\n🛑 MCP server stopped by user.")
    except Exception as e:
        print(f"\n❌ Error starting MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()