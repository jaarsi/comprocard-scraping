import json
import sys
from io import StringIO

import pandas as pd

with open(sys.argv[1], "r") as file:
    data = json.load(file)

pd.read_json(StringIO(json.dumps(data["objects"]))).to_csv("reports/report.csv")
