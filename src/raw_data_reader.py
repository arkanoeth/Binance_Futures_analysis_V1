import pandas as pd
from dateutil.parser import parse


def read_raw_data(file_path: str):
    '''
    Helper method for reading raw data.

    :param file_path: source file with raw data in a very unusual format
    :return: a pandas Dataframe with all pair's data.
    '''
    pair_counter = 0
    all_pairs_data = []

    with open(file_path) as f:
        for i, line in enumerate(f):
            # Ignore first rows
            if i < 2:
                continue
            # In the funky raw data format, observation's timestamp starts with an (')
            if not line.startswith('\''):
                # After a series is finished, there is a line with a single comma (,\n)
                if line.rstrip() == ',':
                    df = pd.DataFrame.from_dict(pair_hourly_data, orient='index', columns=[pair])
                    if df.shape[0] > 0:
                        pair_counter += 1
                        print(f'Load {df.shape[0]} observations from {pair}. {pair_counter} pairs read so far.')
                        all_pairs_data.append(df)
                    else:
                        print(f'Pair {pair} has no data, skipping.')
                    continue
                pair_hourly_data = {}
                pair = line.split(',')[0]
            else:
                # if there is no (') it may be the name of the pair...
                parts = line.strip().replace('\'', '').split(',')
                timestamp = parse(parts[0])
                pair_hourly_data[timestamp] = (parts[1])

    return pd.concat(all_pairs_data, axis=1, join='outer')


if __name__ == '__main__':
    raw_data_file_path = '../data/hourly_data_raw.csv'
    output_data_file_path = '../data/crypto_hourly_data.csv'
    crypto_data = read_raw_data(raw_data_file_path)
    crypto_data.to_csv(output_data_file_path)
    print(f'\nData saved as {output_data_file_path}')
    print(f'DONE!')
