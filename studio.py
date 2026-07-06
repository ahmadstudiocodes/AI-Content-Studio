from core.checker import check_environment
from core.folder_manager import create_project_structure


def main():
    print("=" * 50)
    print(" AI Content Studio")
    print(" StudioOS v0.0.1-prealpha")
    print("=" * 50)

    check_environment()
    create_project_structure()

    print("\nStudio Ready.")
    print("Welcome Ahmad 🚀")


if __name__ == "__main__":
    main()
    from core.startup import startup
from core.shutdown import shutdown


def main():

    startup()

    print("\nWelcome Ahmad 👋")
    print("AI Content Studio Started.\n")

    shutdown()


if __name__ == "__main__":
    main()