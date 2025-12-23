# Portfolio Optimization with Riskfolio-Lib, Plotly, and yfinance

A comprehensive Streamlit web application for portfolio optimization using Riskfolio-Lib, with real-time data from Yahoo Finance and interactive visualizations powered by Plotly.

## Features

This application provides multiple portfolio optimization models:

### Optimization Models
- **Maximum Return Portfolio**: Maximizes expected portfolio returns
- **Minimum Risk Portfolio**: Minimizes portfolio risk based on selected risk measure
- **Maximum Risk Adjusted Return Ratio Portfolio**: Maximizes Sharpe ratio (risk-adjusted returns)
- **Maximum Utility Portfolio**: Optimizes based on investor's utility function with risk aversion parameter
- **Risk Parity Portfolio**: Allocates weights so each asset contributes equally to portfolio risk
- **Relaxed Risk Parity Portfolio**: Flexible variant of risk parity optimization
- **Worst Case Mean Variance Portfolio Optimization**: Robust optimization accounting for parameter uncertainty
  - Maximum Return under uncertainty
  - Minimum Risk under uncertainty
  - Maximum Sharpe Ratio under uncertainty
  - Maximum Utility under uncertainty

### Risk Measures
- MV (Mean-Variance/Standard Deviation)
- CVaR (Conditional Value at Risk)
- MAD (Mean Absolute Deviation)
- And 10+ other risk measures

### Visualizations
- Portfolio weight distribution (bar chart and pie chart)
- Efficient frontier with optimal portfolio highlighted
- Interactive Plotly charts
- Portfolio performance metrics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DylaneTrader/Riskfolio_Yfinance.git
cd Riskfolio_Yfinance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## How to Use

1. **Configure Portfolio Settings** (Sidebar):
   - Enter stock tickers (comma-separated, e.g., AAPL,MSFT,GOOGL)
   - Select date range for historical data
   - Choose optimization model
   - Select risk measure
   - Set risk-free rate and other parameters

2. **Optimize Portfolio**:
   - Click the "Optimize Portfolio" button
   - Wait for data download and optimization to complete

3. **View Results**:
   - Portfolio performance metrics (expected return, volatility, Sharpe ratio)
   - Portfolio weights table
   - Visual representations (pie chart, bar chart)
   - Efficient frontier plot
   - Download optimized weights as CSV

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- riskfolio-lib >= 5.0.0
- yfinance >= 0.2.31
- plotly >= 5.17.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.11.0

## Technologies

- **Streamlit**: Web application framework
- **Riskfolio-Lib**: Portfolio optimization library
- **yfinance**: Yahoo Finance data API
- **Plotly**: Interactive visualization library
- **Pandas/NumPy**: Data manipulation and numerical computing

## Example Portfolio

Default tickers include major US stocks:
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- AMZN (Amazon)
- TSLA (Tesla)
- JPM (JPMorgan Chase)
- JNJ (Johnson & Johnson)
- V (Visa)
- PG (Procter & Gamble)
- NVDA (NVIDIA)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This application is for educational and research purposes only. It should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.