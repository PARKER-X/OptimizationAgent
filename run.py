#!/usr/bin/env python3
"""
MILP Optimization Agent - FastAPI Application Runner
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Run the FastAPI application"""

    # Set project root directory as working directory
    project_root = Path(__file__).resolve().parent
    os.chdir(project_root)

    print("\n🚀 Starting MILP Optimization Agent API...")
    print(f"📁 Project root:             {project_root}")
    print("🌐 API available at:         http://localhost:8000")
    print("📚 Swagger Docs:             http://localhost:8000/docs")
    print("🧪 ReDoc (optional):         http://localhost:8000/redoc")
    print("🎨 Frontend UI (HTML/CSS):   http://localhost:8000/")
    print("-" * 60)

    try:
        # Run FastAPI app defined in `api/main.py`
        uvicorn.run(
            "api.main:app",     # path.to.module:app_instance
            host="0.0.0.0",      # expose to all interfaces (LAN/dev use)
            port=8000,
            reload=True,        # auto-reload on code changes (for dev only)
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
