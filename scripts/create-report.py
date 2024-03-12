import json
import math
import re
from datetime import datetime
from io import StringIO

import pandas as pd

from app.scrape.core import scrape
from app.scrape.types import ScrapedPageResult


def normalize_geopoint(value: str, index: int = 0) -> float | tuple[float, float] | str:
    if not value:
        return value
    elif isinstance(value, float):
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
        filename = f"{datetime.now().isoformat()}"
        print(f"\033[0;36mCreating report on '{filename}'\033[0m")
        results = scrape()
        print("Normalizing data")
        normalized_results = [normalize_item(_) for _ in results if _["uf"].upper().strip() == "ES"]
        normalized_results = sorted(
            normalized_results, key=lambda item: (item["_source"], item["_page"], item["nome"])
        )
        df = pd.read_json(StringIO(json.dumps(normalized_results)))
        df = df.drop_duplicates()
        df.to_csv(f"reports/{filename}.csv")
        print(
            "\033[0mCompleted with => "
            f"\033[0;35m[total \033[0m{len(results)}"
            f"\033[0;35m] [normalized \033[0m{len(normalized_results)}"
            f"\033[0;35m] [unique \033[0m{len(df)}"
            "\033[0;35m]"
        )
    except KeyboardInterrupt:
        print("\n\033[0;31mInterrupted\033[0m")
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    main()
