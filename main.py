#!/usr/bin/env python3
# Name: main.py
# Author: stowyh
# Date: October 27, 2023
from installer import (
    check_xcode, check_homebrew,
    check_and_install_fzf, check_and_install_python_packages,
)
from brewop import (
    install_application, install_cask, uninstall_package,
    install_bundle,
)

def main():
    while True:
        operation = input("\nOperation: (I)nstall, (U)ninstall, or (E)xit? ").strip().lower()
        if operation == "e":
            print("Exiting. Goodbye!")
            break
        elif operation == "i":
            op_type = input("Install (F)ormula, (C)ask, or (B)undle? (A)bort: ").strip().lower()
            if op_type == "f":
                install_application()
            elif op_type == "c":
                install_cask()
            elif op_type == "b":
                install_bundle()
            elif op_type == "a":
                print("Aborted installation.")
            else:
                print("Invalid operation. Try again.")
        elif operation == "u":
            uninstall_package()
        else:
            print("Invalid operation. Try again.")

if __name__ == "__main__":
    check_xcode()
    check_homebrew()
    check_and_install_fzf()
    check_and_install_python_packages()
    main()
