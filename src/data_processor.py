import pandas as pd
import numpy as np


class DataProcessor:
    """
    Process historical time series of prices and generates statistic of correlation, positive and negative days, and
    price movement by hour.
    """

    def __init__(self, hourly_price_series: pd.DataFrame):
        """
        Initializes an instance of the DataProcessor class.

        :param hourly_price_series: a pandas DataFrame with hourly prices of multiple futures.
        """
        if not isinstance(hourly_price_series, pd.DataFrame):
            raise TypeError(
                f'DataProcessor.__init__(): This class expects a DataFrame as argument, received {type(hourly_price_series)} instead.')
        print(f'DataProcessor.main(): Processing data of {hourly_price_series.shape[1]} futures.')
        self.hourly_price_series = hourly_price_series.sort_index(axis=1)
        self.futures_list = sorted(hourly_price_series.columns.to_list())
        self.daily_price_series = hourly_price_series.resample('1D').last()
        self.daily_pct_change = self.daily_price_series.pct_change()
        self.daily_first_diff = self.daily_price_series.diff()
        self.correlation_matrix = self.estimate_correlation_matrix()

    def _get_top_correlated_securities_with(self, target, count=10):
        """
        Estimates the top strongest correlated futures with the target future.

        :param target: the target future.
        :param count: the count of the top strongest (weakest) correlated futures. Default: 10.
        :return: None
        """
        if target not in self.futures_list:
            raise TypeError(
                f'DataProcessor.get_highest_correlated_securities_with(): Security {target} not present in correlation matrix')
        count = min(len(self.futures_list) - 1, count)
        sorted_correlation_matrix = self.correlation_matrix.abs().sort_values(by=target)
        highest_correlated = sorted_correlation_matrix.index[-count - 1:-1][::-1]
        lowest_correlated = sorted_correlation_matrix.index[:count]
        return highest_correlated, lowest_correlated

    def get_correlation_matrices_respect_to(self, target, count=10):
        """
        Estimates the top strongest correlated futures with the target future and generates the correlation matrices.

        :param target: the target future.
        :param count: the count of the top strongest (weakest) correlated futures. Default: 10.
        :return: None
        """
        highest_correlated, lowest_correlated = self._get_top_correlated_securities_with(target, count)
        highest_correlated = [target, *highest_correlated]
        lowest_correlated = [target, *lowest_correlated]
        return {'HighestCorrelated': self.correlation_matrix.loc[highest_correlated, highest_correlated],
                'LowestCorrelated': self.correlation_matrix.loc[lowest_correlated, lowest_correlated]}

    def estimate_positive_negative_days_statistics(self):
        """
        Estimates the following statistics:
            - Days count
            - Days count (%)
            - Days changes mean (%)
            - Days changes mean (USDT)
        for positive and negative days.

        :return: a pandas DataFrame with the mentioned statistics for all futures.
        """
        positive_days = self.daily_pct_change[self.daily_pct_change > 0]
        positive_days_count = positive_days.count()
        positive_days_pct = positive_days_count / self.daily_pct_change.count()
        negative_days = self.daily_pct_change[self.daily_pct_change < 0]
        negative_days_count = negative_days.count()
        negative_days_pct = negative_days_count / self.daily_pct_change.count()
        dic_positive_days = {'Days count': positive_days_count,
                             'Days count (%)': positive_days_pct,
                             'Days changes mean (%)': positive_days.mean(),
                             'Days changes mean (USDT)': self.daily_first_diff[self.daily_first_diff > 0].mean()}
        dic_negative_days = {'Days count': negative_days_count,
                             'Days count (%)': negative_days_pct,
                             'Days changes mean (%)': negative_days.mean(),
                             'Days changes mean (USDT)': self.daily_first_diff[self.daily_first_diff < 0].mean()}
        positive_days_stats = pd.concat(dic_positive_days.values(), axis=1, keys=dic_positive_days.keys()).transpose()
        negative_days_stats = pd.concat(dic_negative_days.values(), axis=1, keys=dic_negative_days.keys()).transpose()
        df_dic = {'Positive days': positive_days_stats, 'Negative days': negative_days_stats}
        return (pd.concat(df_dic.values(), axis=1, keys=df_dic.keys())
                .swaplevel(axis=1)
                .reindex(self.futures_list, axis=1, level=0))

    def estimate_correlation_matrix(self, log_series=True):
        """
        Estiamtes the correlation matrix for all futures, by default it estimate the log of the prices first.

        :param log_series: if True, apply log to all prices series before estimating the correlation matrix. Default: True.
        :return: a pandas DataFrame with the correlation matrix.
        """
        price_series = self.hourly_price_series
        if log_series:
            price_series = np.log(price_series)
        return price_series.corr()

    def estimate_normalized_mean_movement_by_hour(self):
        """
        Estimates the mean movement by hour of the normalized prices series.

        :return: a pandas DataFrame with the mean movement by hour of the normalized prices series
        """
        return self._estimate_mean_movement_by_hour(normalize=True)

    def estimate_normalized_absolute_mean_movement_by_hour(self):
        """
        Estimates the mean movement in absolute value by hour of the normalized prices series.

        It's a measure of the price movement strength by hour.

        :return: a pandas DataFrame with the mean movement in absolute value by hour of the normalized prices series.
        """
        return self._estimate_mean_movement_by_hour(normalize=True, absolute_value=True)

    def estimate_mean_movement_and_strength_by_hour(self):
        """
        Estimates the mean movement in USDT by hour of the price series, and its strength.

        :return: a pandas DataFrame with the mean movement in USDT by hour of the price series, and its strength.
        """
        absolute_movement_by_hour = self._estimate_mean_movement_by_hour()
        movement_strength_by_hour = self._estimate_mean_movement_by_hour(absolute_value=True)
        movement_strength_by_hour = movement_strength_by_hour / movement_strength_by_hour.mean()
        df_dic = {'Mean Movement (USDT)': absolute_movement_by_hour, 'Movement Strength': movement_strength_by_hour}
        return (pd.concat(df_dic.values(), axis=1, keys=df_dic.keys())
                .swaplevel(axis=1)
                .reindex(self.futures_list, axis=1, level=0))

    def _estimate_mean_movement_by_hour(self, normalize=False, absolute_value=False):
        """
        Estimate the movement by hour for all the crypto futures in the price series.

        We extract three insights from this processing:
            1. A matrix with all crypto futures' mean movement. in this case the data should be normalized
                to make it comparable.
            2. A measure of the strength if the movement, this is similar to the previous one, but we use the
                absolute value of the first differences.
            3. The movement by hour for each crypto future and its strength, for this case we don't
                transform the first differences before processing. The insight in this case is that the mean movement
                by hour is in the quote currency (USDT)

        :param normalize: if True we normalize the prices before processing. Default False
        :param absolute_value: if True we use the absolute value of the first differences. It is a measurement of the
                               mean movement strength.
        :return: a pandas DataFrame with the mean movement by hour over the complete sample
        """

        price_series = self.hourly_price_series
        if normalize:
            price_series = ((self.hourly_price_series - self.hourly_price_series.mean()) /
                            self.hourly_price_series.std())

        first_diff = price_series.diff()

        if absolute_value:
            first_diff = first_diff.abs()

        hour = pd.to_timedelta(price_series.index.hour, unit='H')
        movement_by_hour = first_diff.groupby(hour).mean()
        movement_by_hour['Hour'] = movement_by_hour.index / np.timedelta64(1, 'h')
        normalized_movement_by_hour = movement_by_hour.astype({'Hour': int})
        return normalized_movement_by_hour.set_index('Hour')

    def estimate_price_and_std_ma(self, periods={'Monthly': '30D', 'Weekly': '7D', 'Daily': '1D'}, min_period_buffer=0.8):
        """
        Estimates the price and STD moving average for different periods.

        The default periods are Monthly, weekly and daily.

        :param periods: a dictionary with the period name as key and the offset string as value.
        :param min_period_buffer: what proportion of the period should be present to emit a ma value.
        :return: a pandas DataFrame with the price and STD moving average for the different periods.
        """
        prices_ma_df_dict = {}
        std_ma_df_dict = {}
        for period in periods:
            # Source data's frequency is hours, so we need to estimate the min periods for the rolling window in hours.
            min_periods = int(pd.tseries.frequencies.to_offset(periods[period]).delta * min_period_buffer /
                              pd.Timedelta('1 hour'))
            rolling = self.hourly_price_series.rolling(periods[period], min_periods=min_periods)
            prices_ma_df_dict[period] = rolling.mean()
            std_ma_df_dict[period] = rolling.std()

        prices = pd.concat(prices_ma_df_dict.values(), axis=1, keys=prices_ma_df_dict.keys())
        std = pd.concat(std_ma_df_dict.values(), axis=1, keys=std_ma_df_dict.keys())
        ma_dict = {'Prices': prices, 'STD': std}
        return (pd.concat(ma_dict.values(), axis=1, keys=ma_dict.keys())
                .swaplevel(0, axis=1)  # move futures to the top level
                .swaplevel(1, axis=1)  # move the kind of ma (price, std) to the second level
                .reindex(self.futures_list, axis=1, level=0)
                .dropna(how='all'))
