from .scrape import get_report
import json


def main():
    report = get_report()

    with open(f"reports/{report['created_at']}.json", "w") as file:
        json.dump(report, file, indent=4)


if __name__ == "__main__":
    main()
