# Sisense Dashboard Data Extractor

A simple, powerful Python script to extract widget- and dashboard-level metadata from your Sisense `.dash` (JSON) files and output it all to a single CSV for easy reference.

## 📌 What It Does

This script parses all the `.json` (converted `.dash`) files in a folder and extracts useful details such as:

- Widget titles  
- Widget IDs  
- Dashboard titles  
- Associated labels  
- Direct URLs (relative to your Sisense instance)  

It compiles everything into one neat CSV so you can audit, review, or repurpose your Sisense dashboard content efficiently.

## 📁 Files It Works With

These must be JSON exports of your Sisense dashboards (`.dash` files saved as `.json`). The script is designed to work locally with those files, not by querying the Sisense API.

---

## 🚀 How to Use

1. **Convert your `.dash` files to `.json`** (if needed).  
2. **Place `dash_data_extractor.py` in the same folder** as your JSON files.  
3. **Update the `SENSIBLE_URL` constant** in the script to match your Sisense instance URL.  
4. **Run the script**:

    ```bash
    python dash_data_extractor.py
    ```

5. A CSV file will be created in the same directory with all the extracted metadata.

---

## 📦 Output Example

The output CSV includes:

| Dashboard Title | Widget Title | Widget ID | Label(s) | URL |
|-----------------|--------------|-----------|----------|-----|
| Sales Overview  | Total Revenue | abc123    | Q1, Sales | https://yoursisense.com/app/main#/dashboards/... |

---

## 🛠️ Requirements

- Python 3.x  
- No external libraries needed (uses standard Python modules)

---

## 🧾 Why Use This?

- Quickly document dashboard contents  
- Audit widget labeling consistency  
- Prepare for dashboard refactors  
- Make sharing and discussing widget locations easier

---

## 🙌 Contributions

Pull requests and improvements welcome. If you've got a way to make this faster or more powerful, send it in.
