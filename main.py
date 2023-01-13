import requests
import csv
from shutil import rmtree
from pathlib import Path

CODES_FILE_PATH = Path.cwd() / 'state_codes.csv'
TEMPLATE_URL: str = 'https://nassgeodata.gmu.edu/nass_data_cache/byfips/CDL_{}_{}.zip'
CWD: Path = Path.cwd()
YEARS: range = range(2008, 2022)


def get_state_code_dict_from_csv() -> dict:
    state_code_dict = {}
    with open(CODES_FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'STATEFP' or row[1] == 'STUSPS':
                continue

            state_code_dict[row[1]] = row[0]

    return state_code_dict


def clear_and_create_folder():
    folder = CWD / 'data'
    if not folder.exists():
        folder.mkdir()
    else:
        for item in folder.iterdir():
            if item.is_dir():
                rmtree(item)
            else:
                item.unlink()


def get_and_create_subfolder(state: str):
    folder = CWD / 'data' / state
    if not folder.exists():
        folder.mkdir()
    return folder


def download_files(state_code_dict: dict):
    for year in YEARS:
        for state, code in state_code_dict.items():
            file_name = f'CDL_{year}_{state}.zip'
            subfolder = get_and_create_subfolder(state)
            file_location = subfolder / file_name
            url = TEMPLATE_URL.format(year, code)
            print(f'Downloading {url}')
            data = requests.get(url)

            with open(file_location, 'wb') as f:
                f.write(data.content)


def main():
    clear_and_create_folder()
    state_code_dict = get_state_code_dict_from_csv()
    download_files(state_code_dict)


if __name__ == '__main__':
    main()