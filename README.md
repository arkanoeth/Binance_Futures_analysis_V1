# Binance Futures Analysis V1

This tool is designed to analyze the cryptocurrency market and provide better tools to assemble a more balanced cryptocurrency investment portfolio.

# Requirements

To run this code you need to have the following dependencies installed: 

numpy==1.22.0,  

openpyxl==3.0.9, 

pandas==1.3.5, 

pytest==6.2.5, 

matplotlib==3.5.1.

# Input data

The code requires hourly price data, which is provided in the "hourly_data_raw.csv" file. This file contains price data for 120 cryptocurrencies over a 1-year time span.

The raw_data_reader.py code reads the file, sorts the data into a more convenient format for calculations, and creates the crypto_hourly_data.csv file.

# Data Processing

With the processed data, the data_processor.py class establishes the necessary functions to perform all the calculations that will be ultimately reflected in the output Excel file.

Here's a brief overview of what each of the methods does:

-**__init__(self, hourly_price_series: pd.DataFrame)**: 

This is the class constructor, which takes in a pandas DataFrame containing the data. It sorts the DataFrame by column name and creates several other DataFrames based on the input data.

-**_get_top_correlated_securities_with(self, target, count=10)**: 

This is a helper method that takes in a target future and returns the top strongest correlated futures with the target future. It sorts the correlation matrix by column and returns the top count values.

-**get_correlation_matrices_respect_to(self, target, count=10)**: 

This method calls the _get_top_correlated_securities_with method and generates the correlation matrices for the top strongest and weakest correlated futures with the target future.

-**estimate_positive_negative_days_statistics(self)**: 

This method calculates the following statistics for positive and negative days: Days count, Days count (%), Days changes mean (%), and Days changes mean (USDT). It returns a pandas DataFrame with these statistics for all futures.

-**estimate_correlation_matrix(self, log_series=True)**: 

This method estimates the correlation matrix for all futures. It takes in a boolean parameter, log_series, that determines whether the logarithm of the prices series should be estimated first.

-**estimate_normalized_mean_movement_by_hour(self)**: 

This method estimates the mean movement by hour of the normalized prices series. It normalizes the prices series before calculating the mean.

-**estimate_normalized_absolute_mean_movement_by_hour(self)**: 

This method estimates the mean movement in absolute value by hour of the normalized prices series. This is a measure of the price movement strength by hour.

The excel_generator.py module is responsible for formatting the output excel file where all the data is presented.

# Running the Code

The process_futures_data.py script runs everything together. To execute it from the command window, call it with the processed data file location and the output Excel file location as arguments in the following way:

"*_python process_futures_data.py C:\...\Binance_Futures_analysis_V1\data\crypto_hourly_data.csv C:\..\Binance_Futures_analysis_V1\data_*"

# Output Data

The code provides an .xlsx file with an index to navigate it. The following sheets are included:

![image](https://user-images.githubusercontent.com/62271657/233517973-982161e3-9d37-471c-978d-29c15d7bc113.png)

On the second sheet, we have the **hourly movement**.

![image](https://user-images.githubusercontent.com/62271657/233518121-10c84e77-14c9-4644-84ba-f6741a35de41.png)

**"Absolute hourly movement"** is provided. The training data for this example ranges from April 19th, 2022 to April 19th, 2023. As it was a bearish year in the market, we have all the absolute movements in red. The production model should use more than a year to be representative.

![image](https://user-images.githubusercontent.com/62271657/233518323-02de6de1-394e-461c-97d7-11d18489ef6e.png)

The **"Normalized Movement Strength by Hour"** sheet shows us which are the most volatile hours in the market. This data can be useful for traders if they want to expose themselves to volatility, **remembering that volatility means risk and if we take that risk in the right direction, we can achieve better profits.**

![image](https://user-images.githubusercontent.com/62271657/233518550-54ee2ec1-e1fa-48fc-8568-c0ba5ee7013c.png)

**All the timestamps are expressed in UTC.**

The **"Correlation Matrix"** sheet is especially useful for building investment portfolios because when we assemble an investment portfolio in this market, we should look for a balanced portfolio. 

Although the cryptocurrency market has been guided by Bitcoin, each cryptocurrency focuses on a different market and solution. Therefore, I hope that in the future, this correlation will change, and each currency in each market (Metaverse, AI, DeFi, CEX, DEX, etc.) will have its own correlation with its market.

For each cryptocurrency in the analysis, we will find a file with its specific data, such as:

**The top 10 coins with strong or positive correlation with the analyzed coin.**

![image](https://user-images.githubusercontent.com/62271657/233519064-63c793ef-dd98-4e29-9f2d-b60c2b796c05.png)

**The top 10 coins with a weak or negative correlation to the analyzed coin.**

![image](https://user-images.githubusercontent.com/62271657/233519338-58048db5-cfe3-48a0-ab2c-e116cf30a80d.png)

**Statistics for positive and negative days** with their average movement, percentage change, and change in dollars

![image](https://user-images.githubusercontent.com/62271657/233519488-3f6551cb-9dca-4f24-85e5-745f8593805d.png)

The **"Mean Movement by Hour"** shows us how much the cryptocurrency moved on average at a given time during the study period.

![image](https://user-images.githubusercontent.com/62271657/233519620-2605c1a8-dc12-41e0-935a-6793db0e0db3.png)

# Limitations:

-Only analyzes hourly price data, which may not be sufficient for some users who require more granular or long-term data.

-Only provides correlation analysis and some basic statistics, but does not take into account other factors that may affect cryptocurrency prices, such as news, social media sentiment, or regulatory changes.

-This tool assumes that the past performance of cryptocurrencies is indicative of their future performance, which may not always be the case.

-Only analyzes a specific set of cryptocurrencies and may not be relevant for users who want to analyze other cryptocurrencies or assets.

-**Having the data is certainly valuable, but without adequate knowledge of risk management, your investment strategy may not be effective. Therefore, it is crucial to utilize a robust risk management strategy while investing to mitigate potential risks and ensure successful outcomes.**

# Future improvements:

-Could include additional data sources or indicators, such as social media data, news sentiment analysis, or market data from other exchanges.
-Could include more advanced statistical models, such as machine learning algorithms, to better predict cryptocurrency prices and market trends.
-**This tool definitely should include a better user experience by adding a graphical interface, allowing users to easily view this data and interact with it in real-time.**


**This tool is intended for educational purposes only. The creator cannot be held responsible for any outcomes that may arise from its use in actual trading.**
