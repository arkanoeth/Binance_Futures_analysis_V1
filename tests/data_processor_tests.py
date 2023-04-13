import pandas as pd
from pandas.testing import assert_frame_equal

from ArkansasCryptoFutures.src.data_processor import DataProcessor


def test_correlation_matrices():
    # Arrange
    target = 'BTCUSDT'
    testing_data = pd.read_csv('test_data/testing_data_five_series.csv', index_col=0, parse_dates=True)
    high_correlation_expected_results = pd.read_csv('test_data/highest_correlated_expected_results.csv', index_col=0)
    low_correlation_expected_results = pd.read_csv('test_data/lowest_correlated_expected_results.csv', index_col=0)
    kpv = {'HighestCorrelated': high_correlation_expected_results, 'LowestCorrelated': low_correlation_expected_results}
    data_processor = DataProcessor(testing_data)

    # Act
    actual_results = data_processor.get_correlation_matrices_respect_to(target, 2)

    # Assert
    for (key, expected_results) in kpv.items():
        assert_frame_equal(expected_results, actual_results[key])


def test_mean_movement_and_strength_by_hour():
    # Arrange
    testing_data = pd.read_csv('test_data/testing_data_single_series.csv', index_col=0, parse_dates=True)
    expected_results = pd.read_csv('test_data/mean_movement_and_strength_expecting_results.csv', index_col=0,
                                   parse_dates=True)
    data_processor = DataProcessor(testing_data)

    # Act
    actual_results = data_processor.estimate_mean_movement_and_strength_by_hour()['BTCUSDT']

    # Assert
    assert_frame_equal(expected_results, actual_results)


def test_positive_negative_days_statistics():
    # Arrange
    testing_data = pd.read_csv('test_data/testing_data_two_series.csv', index_col=0, parse_dates=True)
    expected_results = pd.read_csv('test_data/positive_and_negative_days_expected_results.csv', header=[0, 1],
                                   index_col=0)
    data_processor = DataProcessor(testing_data)

    # Act
    actual_results = data_processor.estimate_positive_negative_days_statistics()

    # Assert
    assert_frame_equal(expected_results, actual_results)


def test_price_std_ma_series():
    # Arrange
    testing_data = pd.read_csv('test_data/testing_data_two_series_two_months.csv', index_col=0, parse_dates=True)
    expected_results = pd.read_csv('test_data/price_and_std_ma_expected_results.csv', header=[0, 1, 2], index_col=0,
                                   parse_dates=True)
    data_processor = DataProcessor(testing_data)

    # Act
    actual_results = data_processor.estimate_price_and_std_ma()

    # Assert
    assert_frame_equal(expected_results, actual_results)
