import argparse
import sys
from pathlib import Path

import pandas as pd

from data_processor import DataProcessor
from excel_generator import ExcelGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arkansas futures data processing.')
    parser.add_argument('price_series_path', type=str, help='Path to the CSV file with all the hourly prices series.')
    parser.add_argument('destination_folder', type=str,
                        help='Path to the folder where all output files will be stored.')
    args = parser.parse_args()

    csv_path = Path(args.price_series_path)
    destination_folder = Path(args.destination_folder)
    if not csv_path.exists():
        raise ValueError(
            f'ArkansasCryptoFutures: File {csv_path.absolute()} do not exists, please check the path is correct.')

    print(f'ArkansasCryptoFutures: Reading hourly prices from {csv_path.absolute()}')
    hourly_price_series = pd.read_csv(csv_path.resolve(), index_col=0, parse_dates=True)
    data_processor = DataProcessor(hourly_price_series)
    excel_generator = ExcelGenerator(destination_folder, data_processor)

    try:
        excel_generator.run()
    except Exception as e:
        raise e

    print(f'ArkansasCryptoFutures: Done!')
    sys.exit(0)
