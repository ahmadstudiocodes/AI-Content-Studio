import shutil
import platform


def check_environment():
    print("\nChecking Environment...\n")

    print("Python : OK")
    print(f"OS : {platform.system()}")

    if shutil.which("git"):
        print("Git : OK")
    else:
        print("Git : Not Installed")

    if shutil.which("docker"):
        print("Docker : OK")
    else:
        print("Docker : Not Installed")