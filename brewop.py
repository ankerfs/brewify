# Name: brewop.py
# Author: stowyh
# Date: October 27, 2023
import subprocess
def search_formulas():
    """
    Fetch and return a list of all available Homebrew formulas.
    If fetching fails, returns an empty list.
    """
    import requests
    url = "https://formulae.brew.sh/api/formula.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError if status != 200
        data = response.json()
        return [app["name"] for app in data]
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching formula data from {url}: {e}")
        return []

def search_casks():
    """
    Fetch and return a list of all available Homebrew casks.
    If fetching fails, returns an empty list.
    """
    import requests
    url = "https://formulae.brew.sh/api/cask.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [app["token"] for app in data]
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching cask data from {url}: {e}")
        return []

def search_and_select_item(items, prompt_message="Select an item:"):
    """
    Prompts the user with an interactive fuzzy finder (fzf) and returns the chosen item.
    If nothing is selected or the list is empty, returns None.
    """
    from pyfzf import FzfPrompt

    if not items:
        print("No items to select from.")
        return None

    fzf = FzfPrompt()
    # The --prompt option sets the prompt text within the fzf interface
    # We also print it on screen just as a user message before launching fzf
    print(prompt_message)
    try:
        selected_items = fzf.prompt(items, fzf_options=f'--prompt="{prompt_message} "')
        return selected_items[0] if selected_items else None
    except Exception as e:
        print("Error using fzf prompt:", e)
        return None
def install_application():
    """
    Install a Homebrew formula by letting the user select from the entire formula list.
    """
    formulas = search_formulas()
    if not formulas:
        print("No formulas found (or unable to fetch). Cannot install.")
        return

    form_name = search_and_select_item(formulas, "Select a formula to install")
    if form_name:
        try:
            subprocess.check_call(['brew', 'install', form_name])
            print(f"{form_name} has been successfully installed.")
        except subprocess.CalledProcessError as e:
            print(f"Installation of {form_name} failed. Error: {e}")

def install_cask():
    """
    Install a Homebrew cask by letting the user select from the entire cask list.
    """
    casks = search_casks()
    if not casks:
        print("No casks found (or unable to fetch). Cannot install.")
        return

    cask_name = search_and_select_item(casks, "Select a cask to install")
    if cask_name:
        try:
            subprocess.check_call(['brew', 'install', '--cask', cask_name])
            print(f"{cask_name} has been successfully installed.")
        except subprocess.CalledProcessError as e:
            print(f"Installation of cask {cask_name} failed. Error: {e}")

def uninstall_package():
    """
    Uninstall a Homebrew package (formula or cask) by selecting from already-installed ones.
    Uses 'brew list' to find installed packages and casks.
    """
    try:
        installed_packages = (
            subprocess.check_output(["brew", "list"])
            .decode("utf-8", errors="ignore")
            .splitlines()
        )
    except subprocess.CalledProcessError as e:
        print("Error listing brew packages:", e)
        return

    if not installed_packages:
        print("No Homebrew packages (formulas or casks) are installed on this system.")
        return

    package_to_uninstall = search_and_select_item(installed_packages, "Select a package to uninstall")
    if package_to_uninstall:
        try:
            subprocess.check_call(['brew', 'uninstall', '--zap', package_to_uninstall])
            print(f"{package_to_uninstall} has been successfully uninstalled.")
        except subprocess.CalledProcessError as e:
            print(f"Uninstallation of {package_to_uninstall} failed. Error: {e}")

def install_bundle():
    """
    Allows the user to repeatedly add formulae or casks to a bundle.
    The user can either continue adding or finish at any time.
    If no packages are selected by the time they're done, the process aborts.
    """
    package_list = []  # Will hold tuples of (package_type, package_name)

    while True:
        print("\n--- Add items to your bundle ---")
        choice = input(
            "(F)ormula, (C)ask, (D)one, or (A)bort bundle creation?\n"
            "Enter your choice: "
        ).strip().lower()

        # A) Abort the entire bundle creation
        if choice == 'a':
            print("Aborted bundle creation. Returning to main menu.")
            return

        # D) Done adding items
        if choice == 'd':
            if not package_list:
                # No packages were selected yet
                print("You haven't added any packages to this bundle. Aborting.")
                return
            break  # proceed to install everything in `package_list`

        # Must be formula or cask
        if choice not in ('f', 'c'):
            print("Invalid choice. Please pick (F), (C), (D), or (A).")
            continue

        # Retrieve the correct list of available packages
        if choice == 'f':
            available_packages = search_formulas()
            ptype_description = "formula"
        else:  # 'c'
            available_packages = search_casks()
            ptype_description = "cask"

        if not available_packages:
            print(f"No {ptype_description}s found (or unable to fetch). Try something else.")
            continue

        # Now let the user pick from fzf
        while True:
            pkg = search_and_select_item(
                available_packages,
                prompt_message=f"Select the {ptype_description} you want to add"
            )
            if pkg:
                # A valid package was selected
                package_list.append((choice, pkg))
                print(f"Added '{pkg}' to the bundle.")

                # Ask if user wants to add another one of the same type
                more = input(f"Add another {ptype_description}? (Y)es/(N)o: ").lower()
                if more != 'y':
                    # Stop picking from this type; go back to top-level menu
                    break
            else:
                # Nothing was selected in fzf
                print(f"No {ptype_description} selected.")
                retry_or_done = input("(R)etry selecting or (D)one with this category? ").lower()
                if retry_or_done == 'r':
                    # Re-run the fzf selection for the same category
                    continue
                else:
                    # 'done' means break out and ask top-level question (F, C, D, A).
                    break

    # If we reach here, the user typed 'd' => they are done adding
    print("\nInstalling your selected bundle packages...")

    # Check currently installed packages
    try:
        installed_packages = (
            subprocess.check_output(["brew", "list"])
            .decode("utf-8", errors="ignore")
            .splitlines()
        )
    except subprocess.CalledProcessError as e:
        print("Error listing currently installed packages:", e)
        return

    # Install each package if not already installed
    for ptype, pname in package_list:
        if pname in installed_packages:
            print(f"{pname} is already installed. Skipping.")
            continue

        if ptype == "f":
            cmd = ["brew", "install", pname]
        else:  # ptype == "c"
            cmd = ["brew", "install", "--cask", pname]

        print(f"Installing '{pname}'...")
        try:
            subprocess.check_call(cmd)
            print(f"{pname} has been successfully installed.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {pname}. Error: {e}")
