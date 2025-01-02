import subprocess
import sys
import os
import json
from typing import Tuple, Optional
import argparse
import gradio as gr

class PipManager:
    def __init__(self, config_file: str = "python_path.json"):
        self.config_file = config_file
        self.python_path = self.load_config()
        
    def load_config(self) -> str:
        """Load Python path from config file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('python_path', sys.executable)
            except json.JSONDecodeError:
                return sys.executable
        return sys.executable
    
    def save_config(self, python_path: str) -> None:
        """Save Python path to config file."""
        with open(self.config_file, 'w') as f:
            json.dump({'python_path': python_path}, f)
    
    def update_pip(self) -> Tuple[bool, str]:
        """Update pip to the latest version."""
        try:
            result = subprocess.run(
                [self.python_path, '-m', 'pip', 'install', '--upgrade', 'pip'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, "Pip updated successfully!"
            return False, f"Error updating pip: {result.stderr}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def install_package(self, package_name: str) -> Tuple[bool, str]:
        """Install a pip package."""
        try:
            result = subprocess.run(
                [self.python_path, '-m', 'pip', 'install', package_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, f"Package '{package_name}' installed successfully!"
            return False, f"Error installing package: {result.stderr}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def remove_package(self, package_name: str) -> Tuple[bool, str]:
        """Remove a pip package."""
        try:
            result = subprocess.run(
                [self.python_path, '-m', 'pip', 'uninstall', '-y', package_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, f"Package '{package_name}' removed successfully!"
            return False, f"Error removing package: {result.stderr}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def check_version(self, package_name: str) -> Tuple[bool, str]:
        """Check the version of a pip package."""
        try:
            result = subprocess.run(
                [self.python_path, '-m', 'pip', 'show', package_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        return True, f"Package '{package_name}' version: {line.split(':')[1].strip()}"
                return False, f"Version information not found for '{package_name}'"
            return False, f"Package '{package_name}' not found"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def list_packages(self) -> Tuple[bool, str]:
        """List all installed packages."""
        try:
            result = subprocess.run(
                [self.python_path, '-m', 'pip', 'list'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, result.stdout
            return False, f"Error listing packages: {result.stderr}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def update_python_path(self, new_path: str) -> Tuple[bool, str]:
        """Update the Python path."""
        if not os.path.exists(new_path):
            return False, "Invalid Python path: File does not exist"
        try:
            self.python_path = new_path
            self.save_config(new_path)
            return True, "Python path updated successfully!"
        except Exception as e:
            return False, f"Error updating Python path: {str(e)}"

def create_gradio_interface():
    pip_manager = PipManager()
    
    def handle_operation(operation: str, package_name: str = "", python_path: str = "") -> str:
        if operation == "Update PIP":
            success, message = pip_manager.update_pip()
        elif operation == "Install Package":
            if not package_name:
                return "Please enter a package name"
            success, message = pip_manager.install_package(package_name)
        elif operation == "Remove Package":
            if not package_name:
                return "Please enter a package name"
            success, message = pip_manager.remove_package(package_name)
        elif operation == "Check Version":
            if not package_name:
                return "Please enter a package name"
            success, message = pip_manager.check_version(package_name)
        elif operation == "List Packages":
            success, message = pip_manager.list_packages()
        elif operation == "Update Python Path":
            if not python_path:
                return "Please enter a Python path"
            success, message = pip_manager.update_python_path(python_path)
        else:
            return "Invalid operation"
        
        return message

    with gr.Blocks(theme=gr.themes.Default()) as interface:
        with gr.Column(scale=1):
            gr.Markdown(
                """
                # PIP Package Manager
                Manage Python packages in your environment
                """
            )
            gr.Markdown(f"**Current Python Path:** `{pip_manager.python_path}`")
            
            operation = gr.Radio(
                choices=["Update PIP", "Install Package", "Remove Package", 
                        "Check Version", "List Packages", "Update Python Path"],
                label="Select Operation",
                value="Update PIP",
                info="Choose the operation you want to perform"
            )
            
            with gr.Group():
                package_name = gr.Textbox(
                    label="Package Name",
                    placeholder="Enter package name (e.g., requests, pandas)",
                    visible=True,
                    info="Required for Install, Remove, and Check Version operations"
                )
                python_path = gr.Textbox(
                    label="Python Path",
                    placeholder="Full path to python.exe",
                    visible=True,
                    info="Required only for Update Python Path operation"
                )
            
            with gr.Row():
                submit_btn = gr.Button("Execute", variant="primary", scale=2)
                clear_btn = gr.Button("Clear Output", scale=1)
            
            output = gr.Textbox(
                label="Output",
                lines=10,
                max_lines=15,
                show_copy_button=True
            )

            # Show/hide input fields based on operation
            def update_visibility(operation):
                return {
                    package_name: operation in ["Install Package", "Remove Package", "Check Version"],
                    python_path: operation == "Update Python Path"
                }

            operation.change(
                fn=update_visibility,
                inputs=[operation],
                outputs=[package_name, python_path]
            )
            
            submit_btn.click(
                fn=handle_operation,
                inputs=[operation, package_name, python_path],
                outputs=output
            )
            
            clear_btn.click(
                fn=lambda: "",
                inputs=[],
                outputs=output
            )

            gr.Markdown(
                """
                ### Notes:
                - The package name is case-sensitive
                - For specific versions, use: package==version (e.g., requests==2.31.0)
                - The Python path should be the full path to python.exe
                """
            )

    return interface

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="PIP Package Manager")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    args = parser.parse_args()
    
    if args.cli:
        pip_manager = PipManager()
        while True:
            print("\nPIP Package Manager")
            print(f"Current Python Path: {pip_manager.python_path}")
            print("\nOperations:")
            print("1. Update PIP")
            print("2. Install Package")
            print("3. Remove Package")
            print("4. Check Version")
            print("5. List Packages")
            print("6. Update Python Path")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ")
            
            if choice == "1":
                success, message = pip_manager.update_pip()
                print(message)
            elif choice == "2":
                package = input("Enter package name: ")
                success, message = pip_manager.install_package(package)
                print(message)
            elif choice == "3":
                package = input("Enter package name: ")
                success, message = pip_manager.remove_package(package)
                print(message)
            elif choice == "4":
                package = input("Enter package name: ")
                success, message = pip_manager.check_version(package)
                print(message)
            elif choice == "5":
                success, message = pip_manager.list_packages()
                print(message)
            elif choice == "6":
                path = input("Enter new Python path: ")
                success, message = pip_manager.update_python_path(path)
                print(message)
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    else:
        # Run Gradio interface with secure settings
        interface = create_gradio_interface()
        interface.launch(
            server_name="127.0.0.1",  # Only accessible from localhost
            server_port=7860,         # Default Gradio port
            share=False,              # Disable public URL generation
            inbrowser=True           # Automatically open in default browser
        )

if __name__ == "__main__":
    main()