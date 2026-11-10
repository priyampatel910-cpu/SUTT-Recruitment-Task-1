from pathlib import Path
from storage import load_cabs_csv
from pool import CabPool
from cli import run_menu

PROJECT_DIRECTORY = Path(__file__).resolve().parent
CABS_PATH = PROJECT_DIRECTORY / "data" / "cabs.csv"

def main():
    cab_list = load_cabs_csv(CABS_PATH)
    pool = CabPool(cab_list)

    try:
        run_menu(pool)

    except(KeyboardInterrupt):
        print("\nExiting. Goodbye")


if __name__ == "__main__":
    main()    