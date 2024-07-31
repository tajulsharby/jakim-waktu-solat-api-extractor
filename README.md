# JAKIM Waktu Solat API Extractor

## Description

This script extracts prayer times data from JAKIM's API for all Malaysian zones and saves the data into a CSV file. The data includes various prayer times and corresponding Hijri dates.

## Created by
- **TJ Sharby**

## Github
- [https://github.com/tajulsharby/jakim-waktu-solat-api-extractor](https://github.com/tajulsharby/jakim-waktu-solat-api-extractor)

## If you like, please treat me a coffee via Touch N Go Digital Wallet QR code: 
- [https://github.com/tajulsharby/treat-me-a-coffee-tng?tab=readme-ov-file](https://github.com/tajulsharby/treat-me-a-coffee-tng?tab=readme-ov-file)

## Requirements

- Python 3.x
- Required Python packages: `requests`

## Installation and Usage

### macOS

1. **Open Terminal**:
    - You can find Terminal in `Applications -> Utilities` or use Spotlight to search for "Terminal".

2. **Navigate to the directory**:
    ```sh
    cd /path/to/your/directory
    ```

3. **Install required packages**:
    ```sh
    python3 -m pip install requests
    ```

4. **Run the script**:
    ```sh
    python3 jakim_api_extractor.py
    ```

### Windows

1. **Open Command Prompt**:
    - Press `Win + R`, type `cmd`, and press `Enter`.

2. **Navigate to the directory**:
    ```sh
    cd \path\to\your\directory
    ```

3. **Install required packages**:
    ```sh
    python -m pip install requests
    ```

4. **Run the script**:
    ```sh
    python jakim_api_extractor.py
    ```

### Linux

1. **Open Terminal**:
    - On most Linux distributions, you can open Terminal by pressing `Ctrl + Alt + T`.

2. **Navigate to the directory**:
    ```sh
    cd /path/to/your/directory
    ```

3. **Install required packages**:
    ```sh
    python3 -m pip install requests
    ```

4. **Run the script**:
    ```sh
    python3 jakim_api_extractor.py
    ```

## Output

- The script will generate a CSV file with a name like `hijri_date_YYYYMMDDHHMMSS.csv` based on the current date and time.
- Logs will be saved to `data_extraction.log`.

## Example Output

- **CSV File Name**: `hijri_date_20240731123456.csv`
- **Log File**: `data_extraction.log`

## Script Introduction

Upon running the script, you will see the following introduction in the console:

