# dash_data_extractor.py
# Extracts useful data from .dash JSON files (widget titles, URLs, labels, etc.)
# Usage:
#   1. Place this script in the same folder as your .json (converted .dash) files
#   2. Update the SENSIBLE_URL constant below with your Sisense URL
#   3. Run script: python dash_data_extractor.py

import json
import os
import csv
from typing import Any, Dict, List, Tuple

# === CONFIG ===
SENSIBLE_URL = "YourSisenseURL"
OUTPUT_CSV = "results.csv"

# === UTILS ===
def safe_get(d: Dict, path: List[str], default: Any = None) -> Any:
    for key in path:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def parse_panels(widget_type: str, panels: List[Dict]) -> Tuple[List[str], List[str], List[str]]:
    dim_list, filter_list, panel_name_list = [], [], []
    for idx, panel in enumerate(panels):
        panel_name = panel.get('name', '')
        items = panel.get('items', [])

        for item in items:
            if idx == 1 and widget_type != "pivot":
                context = safe_get(item, ['jaql', 'context'], {})
                for ctx in context.values():
                    dim = ctx.get('dim')
                    if dim:
                        dim_list.append(str(dim))
                        filter_list.append("")
                        panel_name_list.append(panel_name)
            else:
                dim = safe_get(item, ['jaql', 'dim'])
                if dim:
                    dim_list.append(str(dim))
                    panel_name_list.append(panel_name)
                    filter_val = str(safe_get(item, ['jaql', 'filter'], "")) if idx in [3, 4] else ""
                    filter_list.append(filter_val)
    return dim_list, filter_list, panel_name_list

def process_file(filepath: str, writer: csv.writer) -> None:
    try:
        with open(filepath, 'r') as f:
            j = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Failed to process {filepath}: {e}")
        return

    dashboard_id = j.get('oid')
    dashboard_title = j.get('title')

    for widget in j.get('widgets', []):
        widget_title = widget.get('title')
        widget_id = widget.get('oid')
        widget_type = widget.get('type')
        widget_url = f"{SENSIBLE_URL}/dashboards/{dashboard_id}/widgets/{widget_id}"
        panels = safe_get(widget, ['metadata', 'panels'], [])

        dim_list, filter_list, panel_name_list = parse_panels(widget_type, panels)

        for i, dim in enumerate(dim_list):
            row = [
                dashboard_title,
                widget_title,
                widget_url,
                widget_id,
                widget_type,
                panel_name_list[i],
                dim,
                filter_list[i]
            ]
            writer.writerow(row)

def main():
    header = ['dash_title', 'widget_title', 'widget_url', 'widget_id', 'widget_type', 'panel_name','dim', 'filter']
    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for filename in os.listdir():
            if filename.endswith('.json'):
                process_file(filename, writer)

if __name__ == '__main__':
    main()
