import csv
import json
import os
from typing import List, Dict, Any

import pandas as pd


def export_to_csv(items: List[Dict[str, Any]], path: str) -> None:
    """
    Export list of dicts to CSV. Nested structures are JSON-encoded into cells.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if not items:
        # create empty file
        open(path, "w", newline="", encoding="utf-8").close()
        return

    # determine full set of keys across all items
    keys = set()
    for it in items:
        keys.update(it.keys())
    keys = sorted(keys)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for it in items:
            row = {}
            for k in keys:
                v = it.get(k)
                if isinstance(v, (dict, list)):
                    row[k] = json.dumps(v, ensure_ascii=False)
                else:
                    row[k] = v
            writer.writerow(row)


def export_to_json(items: List[Dict[str, Any]], path: str, indent: int = 2) -> None:
    """
    Write items as pretty JSON.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=indent)


def export_to_excel(items: List[Dict[str, Any]], path: str) -> None:
    """
    Export items to an Excel file using pandas.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if not items:
        df = pd.DataFrame()
    else:
        # flatten nested dicts/lists into columns where possible
        df = pd.json_normalize(items)
    df.to_excel(path, index=False)
