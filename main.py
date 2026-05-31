"""
Main application for RAG System
Streamlit launcher with process management
"""

import sys
import subprocess
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

from config.settings import STREAMLIT_CONFIG


def kill_existing_processes():
    """Kill existing processes on the configured port"""
    try:
        # Kill processes on the specific port
        subprocess.run(
            f"lsof -ti :{STREAMLIT_CONFIG['port']} | xargs kill -9",
            shell=True, check=False
        )
        print(f"🔄 Killed existing processes on port {STREAMLIT_CONFIG['port']}")
    except:
        pass
    
    # Also kill any existing Streamlit processes
    try:
        subprocess.run(["pkill", "-f", "streamlit"], check=False)
        print("🔄 Killed existing Streamlit processes")
    except:
        pass


def run_streamlit():
    """Run the Streamlit web interface"""
    print("🚀 Starting Streamlit web interface...")
    print(f"📱 Open your browser to: http://{STREAMLIT_CONFIG['host']}:{STREAMLIT_CONFIG['port']}")
    
    # Kill existing processes
    kill_existing_processes()
    
    # Run Streamlit
    subprocess.run([
        "streamlit", "run", "app.py",
        "--server.port", str(STREAMLIT_CONFIG['port']),
        "--server.address", STREAMLIT_CONFIG['host']
    ])


def main():
    """Main function - launches Streamlit web interface"""
    run_streamlit()


if __name__ == "__main__":
    main()