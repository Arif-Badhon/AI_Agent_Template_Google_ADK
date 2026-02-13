import subprocess
import os

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        # Don't fail the generation, just print error
        pass

if __name__ == '__main__':
    # 1. Initialize Git
    print("\n--- Initializing Git Repository ---")
    run_command("git init")
    run_command("git add .")
    
    # 2. Install dependencies with uv (Optional but recommended)
    if os.path.exists("pyproject.toml"):
        print("\n--- Installing Dependencies with uv ---")
        run_command("uv sync")
        
    print("\n--- Setup Complete! ---")
    print("Don't forget to rename .env.example to .env and add your API keys.")
