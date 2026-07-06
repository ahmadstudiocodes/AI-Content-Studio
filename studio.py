from core.checker import check_environment
from core.folder_manager import create_project_structure
from core.startup import startup
from core.runtime import runtime
from shell import Shell


def main():

    print("=" * 50)
    print("        Arman StudioOS")
    print("        Version 0.2.0")
    print("=" * 50)

    check_environment()

    create_project_structure()

    startup()

    runtime.start()

    print()
    print("=" * 50)
    print("Arman Online")
    print("=" * 50)

    Shell().start()


if __name__ == "__main__":
    main()