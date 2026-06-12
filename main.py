import sys

from src.app import App


def main():
    app = App()
    exit_code = app.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
