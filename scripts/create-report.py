import json
from datetime import datetime
from io import StringIO

import pandas as pd

from app.scrape import get_all_results


def main():
    filename = f"reports/{datetime.now().isoformat()}.csv"
    print(f"Creating report on '{filename}'")
    results = json.dumps(get_all_results())
    pd.read_json(StringIO(results)).to_csv(filename)


if __name__ == "__main__":
    main()
