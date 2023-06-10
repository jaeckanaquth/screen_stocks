# Screen Stocks

Screen Stocks is a Python script that screens stocks based on specified criteria and generates a list of filtered stocks. It utilizes historical stock data from Yahoo Finance and applies various indicators and conditions to identify potentially promising stocks for further analysis.

## Prerequisites

- Python 3.6 or above
- Pandas library
- Pandas DataReader library
- yfinance library
- gspread library
- gspread-dataframe library
- BeautifulSoup library

## Installation

1. Clone the repository:

```
git clone https://github.com/jaeckanaquth/screen_stocks.git
```

2. Install the required dependencies:

```
pip install pandas pandas_datareader yfinance gspread gspread_dataframe beautifulsoup4
```

3. Obtain the necessary API credentials:
   - For Yahoo Finance data: Obtain an API key from [https://rapidapi.com/apidojo/api/yahoo-finance1/](https://rapidapi.com/apidojo/api/yahoo-finance1/) and update the `config.py` file with your API key.
   - For Google Sheets integration: Create a service account and generate a JSON key file. Rename the key file to `service_account.json` and place it in the project's root directory.

## Usage

1. Open the `config.py` file and set the desired configuration options:
   - `head`: Choose from "Chosen from NIFTY 50" or "Chosen from NIFTY 500" to specify the index to screen stocks from.
   - `count`: Set the count value (0-4) to determine the number of stocks to screen (only applicable for NIFTY 500).

2. Run the `main.py` script:

```
python main.py
```

3. The script will fetch stock data, screen the stocks based on the specified criteria, and publish the results to a Google Sheets document named "QuthsStocks". The filtered stocks will be added as worksheets in the document.

4. If the count is set to 4, the script will also generate an HTML content with the screened stocks and post it to a WordPress website.

## Contributing

Contributions to the Screen Stocks project are welcome. If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure that your code follows the existing code style and includes appropriate tests.

## License

Screen Stocks is open-source software licensed under the [MIT License](LICENSE).

## Disclaimer

The information provided by Screen Stocks is for informational purposes only and should not be considered financial advice. Always do your own research and consult with a qualified investment professional before making any investment decisions.

---

Please note that the README assumes the presence of a `config.py` file and a `service_account.json` file, as mentioned in the provided code snippets. Make sure to create and configure these files accordingly to match your specific setup.
