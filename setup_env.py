#!/usr/bin/env python3
"""
Environment setup script for LightRAG with UI
Creates .env file from env.example with user preferences
"""

import os
import shutil
from pathlib import Path

def setup_environment():
    """Set up environment configuration"""
    print("🔧 Setting up environment configuration...")
    
    # Check if .env already exists
    if Path(".env").exists():
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Setup cancelled.")
            return
    
    # Copy env.example to .env
    try:
        shutil.copy("env.example", ".env")
        print("✅ Created .env file from env.example")
        
        # Ask for user preferences
        print("\n🎯 Let's customize your configuration:")
        
        # Model selection
        print("\n📱 Available models:")
        models = [
            "gemma3:12b (recommended)",
            "gemma2:12b", 
            "gemma2:9b",
            "gemma2:2b",
            "llama3:8b",
            "llama3:70b",
            "mistral:7b",
            "codellama:7b"
        ]
        
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        
        while True:
            try:
                choice = input(f"\nSelect model (1-{len(models)}, default=1): ").strip()
                if not choice:
                    choice = "1"
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(models):
                    selected_model = models[choice_idx].split(" (")[0]  # Remove "(recommended)"
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
        
        # Update .env file with selected model
        with open(".env", "r") as f:
            content = f.read()
        
        content = content.replace("LLM_MODEL_NAME=gemma3:12b", f"LLM_MODEL_NAME={selected_model}")
        
        with open(".env", "w") as f:
            f.write(content)
        
        print(f"✅ Set model to: {selected_model}")
        
        # Port configuration
        port = input("\n🌐 Streamlit port (default=8501): ").strip()
        if port:
            with open(".env", "r") as f:
                content = f.read()
            content = content.replace("STREAMLIT_PORT=8501", f"STREAMLIT_PORT={port}")
            with open(".env", "w") as f:
                f.write(content)
            print(f"✅ Set port to: {port}")
        
        print("\n🎉 Environment setup complete!")
        print("📝 You can edit .env file anytime to change settings.")
        print("🚀 Run: python main.py streamlit")
        
    except FileNotFoundError:
        print("❌ env.example not found. Please run this from the project root.")
    except Exception as e:
        print(f"❌ Error setting up environment: {e}")

if __name__ == "__main__":
    setup_environment()
