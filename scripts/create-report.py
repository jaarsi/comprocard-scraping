import argparse
import json
import math
import os
import re
from datetime import datetime
from io import StringIO

import pandas as pd

from app.scrape import SCRAPER_ENGINES, ScrapedPageResult, scrape


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", default=os.cpu_count(), type=int)
    # parser.add_argument("--results_per_page", default=12, type=int)
    return parser.parse_args()


def normalize_geopoint(value: str, index: int = 0) -> float | tuple[float, float] | str:
    if not value:
        return value
    elif re.match(r"-?\d+\.\d+$", value) is not None:
        return float(value)
    elif (pattern := re.compile(r"(\d+).(\d+).(\d+\.\d+)")).match(value):  # 19°33'19.5"S
        matches = pattern.match(value)
        hours, minutes, seconds = (
            int(matches.group(1)),
            int(matches.group(2)),
            float(matches.group(3)),
        )
        result = hours + minutes / 60 + seconds / 3600
        if value[-1] in "SW":
            result *= -1
        return result
    elif (pattern := re.compile(r"(-?\d+\.\d+)")).search(
        value
    ):  # -20.646434548320997, -40.52329658650793
        if len(matches := pattern.findall(value)) == 1:
            return float(matches[0])
        return float(matches[index])
    elif (pattern := re.compile(r"-?\d+$")).match(value):  # 2084846291235996
        digits = int(math.log10(abs(int(pattern.search(value).group(0)))))
        result = int(value) / 10 ** (digits - 1)
        return result
    else:
        return value


def normalize_item(item: ScrapedPageResult) -> ScrapedPageResult:
    result = {
        **item,
        "latitude": normalize_geopoint(item["latitude"]),
        "longitude": normalize_geopoint(item["longitude"], 1),
    }
    return result


def main():
    try:
        args = parse_args()
        print(f"{args.concurrency=}")
        filename = f"reports/{datetime.now().isoformat()}"
        print(f"\033[0;36mCreating report on '{filename}'\033[0m")
        results = []

        for engine in SCRAPER_ENGINES:

            def handler(page: int):
                print(
                    f"\r[{engine.name}] \033[0;32mRetrieving data from page {page:04d}\033[0m",
                    end="",
                )

            _results, errors = scrape(engine, args.concurrency, handler)
            print(f" => \033[0;35m{len(_results)} results | {len(errors)} errors\033[0m")

            with open(f"{filename}-{engine.name}-raw.json", "w") as file:
                json.dump(_results, file, indent=4)

            if errors:
                with open(f"{filename}-{engine.name}-errors.json", "w") as file:
                    json.dump(errors, file, indent=4)

            results.extend(_results)

        print("Normalizing data")
        normalized_results = [normalize_item(_) for _ in results]
        normalized_results = sorted(
            normalized_results, key=lambda item: (item["_source"], item["_page"])
        )
        pd.read_json(StringIO(json.dumps(normalized_results))).to_csv(f"{filename}.csv")
        print(f"\033[0;35mCompleted with {len(results)} results and {len(errors)} errors\033[0m")
    except KeyboardInterrupt:
        print("\n\033[0;31mInterrupted\033[0m")
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    main()
