import os
import subprocess

def check_emulator_path(sdk_path):
    emulator_path = os.path.join(sdk_path, 'emulator', 'emulator.exe')
    # Check if the emulator tool exists
    if os.path.isfile(emulator_path):
        return emulator_path
    else:
        return None

def get_emulator_path():
    # Define potential SDK paths
    local_sdk_paths = [
        os.path.expanduser("~/Android/Sdk"),
        os.path.join(os.environ['LOCALAPPDATA'], "Android", "Sdk")
    ]

    for sdk_path in local_sdk_paths:
        emulator_tool_path = check_emulator_path(sdk_path)
        if emulator_tool_path:
            return emulator_tool_path

    return None

def get_available_emulators(emulator_path):
    emulators = []
    try:
        result = subprocess.run([emulator_path, '-list-avds'], capture_output=True, text=True)
        if result.returncode == 0:
            emulators = result.stdout.strip().splitlines()
    except Exception:
        pass

    return emulators

def launch_emulator(emulator_name, emulator_path):
    try:
        print(emulator_name)
        subprocess.Popen([emulator_path, f"@{emulator_name}"])
    except Exception as e:
        print(f"Error launching emulator {emulator_name}: {e}")