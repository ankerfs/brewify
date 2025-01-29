# Name: installer.py
# Author: stowyh
# Date: October 27, 2023
import subprocess
import sys

def check_xcode():
    """
    Checks if Xcode command line tools are installed.
    If not, attempts to initiate the installation process.
    """
    try:
        subprocess.check_output("xcode-select -p", shell=True)
        print("Xcode command line tools appear to be installed.")
    except subprocess.CalledProcessError:
        print("Xcode command line tools are NOT installed. Initiating installation...")
        try:
            subprocess.check_call("xcode-select --install", shell=True)
            print("Installation process for Xcode command line tools initiated.")
            print("Please follow any on-screen prompts to complete installation.")
        except subprocess.CalledProcessError as e:
            print("Xcode installation failed. Error:", e)
            sys.exit(1)

def check_homebrew():
    """
    Checks if Homebrew is installed. If not, attempts to install it.
    """
    try:
        subprocess.check_output("brew --version", shell=True)
        print("Homebrew is already installed on your system.")
    except subprocess.CalledProcessError:
        print("Homebrew is NOT installed. Attempting installation...")
        install_brew_cmd = (
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        )
        try:
            subprocess.check_call(install_brew_cmd, shell=True)
            print("Homebrew has been successfully installed.")
        except subprocess.CalledProcessError as e:
            print("Homebrew installation failed. Error:", e)
            sys.exit(1)

def check_and_install_fzf():
    """
    Checks if 'fzf' is installed. If not, uses Homebrew to install it.
    """
    try:
        subprocess.check_call(['command', '-v', 'fzf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("fzf is already installed.")
    except subprocess.CalledProcessError:
        print("'fzf' is not installed. Installing via Homebrew...")
        try:
            subprocess.check_call(['brew', 'install', 'fzf'])
            print("fzf has been successfully installed.")
        except subprocess.CalledProcessError as e:
            print("fzf installation failed. Error:", e)
            sys.exit(1)

def check_and_install_python_packages():
    """
    Checks for required Python packages, and installs them if missing.
    """
    # We cannot import at top-level if it might be missing, so do it inline
    def _install(package_name):
        """Helper to install a Python package quietly."""
        print(f"'{package_name}' is not installed. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name, '--quiet'])

    # Check pyfzf
    try:
        import pyfzf  # noqa
    except ImportError:
        _install('pyfzf')

    # Check requests
    try:
        import requests  # noqa
    except ImportError:
        _install('requests')
