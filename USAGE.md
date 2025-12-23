# Portfolio Optimization Example Usage

This document provides examples of how to use the Portfolio Optimization Application.

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```

3. **Access the Application**
   - The app will open automatically in your default browser
   - Default URL: http://localhost:8501

## Usage Examples

### Example 1: Basic Portfolio Optimization

**Objective**: Create a diversified portfolio with maximum Sharpe ratio

1. Enter tickers in the sidebar:
   ```
   AAPL,MSFT,GOOGL,AMZN,TSLA
   ```

2. Select date range:
   - Start Date: 2 years ago
   - End Date: Today

3. Choose optimization model:
   - Select: "Maximum Risk Adjusted Return Ratio Portfolio"

4. Set parameters:
   - Risk Measure: MV (Standard Deviation)
   - Risk-Free Rate: 2.5%

5. Click "Optimize Portfolio"

**Expected Output**:
- Portfolio weights for each stock
- Expected annual return
- Annual volatility
- Sharpe ratio
- Visual charts (pie chart, bar chart, efficient frontier)

---

### Example 2: Conservative Portfolio (Minimum Risk)

**Objective**: Create a low-risk portfolio for capital preservation

1. Tickers (mix of stable stocks):
   ```
   JNJ,PG,KO,WMT,PEP,VZ
   ```

2. Optimization model:
   - Select: "Minimum Risk Portfolio"

3. Risk measure:
   - CVaR (Conditional Value at Risk) for better tail risk management

**Expected Result**: Portfolio concentrated in most stable, low-volatility stocks

---

### Example 3: Risk Parity Portfolio

**Objective**: Equal risk contribution from each asset

1. Tickers (different sectors):
   ```
   AAPL,XOM,JPM,JNJ,DIS,COST
   ```

2. Optimization model:
   - Select: "Risk Parity Portfolio"

**Expected Result**: Weights adjusted so each asset contributes equally to portfolio risk

---

### Example 4: Robust Optimization (Worst Case)

**Objective**: Portfolio that performs well even with parameter uncertainty

1. Tickers:
   ```
   SPY,TLT,GLD,VNQ,BND
   ```

2. Optimization model:
   - Select: "Worst Case Mean Variance - Maximum Sharpe Ratio"

3. Set uncertainty parameter:
   - Uncertainty Parameter (ε): 0.5

**Expected Result**: More conservative portfolio that accounts for estimation errors

---

## Risk Measures Explained

- **MV** (Mean-Variance): Standard deviation, most common risk measure
- **CVaR** (Conditional Value at Risk): Average loss in worst-case scenarios
- **MAD** (Mean Absolute Deviation): Average absolute deviation from mean
- **CDaR** (Conditional Drawdown at Risk): Average drawdown in worst cases

## Tips for Best Results

1. **Use at least 5-10 stocks** for better diversification
2. **Select 2+ years of data** for reliable statistics
3. **Mix different sectors** for better diversification
4. **Start with simpler models** (Minimum Risk, Maximum Sharpe) before trying advanced ones
5. **Adjust risk-free rate** to match current market conditions

## Common Use Cases

### Conservative Investor
- Model: Minimum Risk Portfolio
- Risk Measure: MV or CVaR
- Assets: Large-cap stocks, bonds, dividend aristocrats

### Aggressive Growth Investor
- Model: Maximum Return Portfolio or Maximum Utility (low risk aversion)
- Risk Measure: MV
- Assets: Growth stocks, tech sector

### Balanced Investor
- Model: Maximum Risk Adjusted Return Ratio Portfolio
- Risk Measure: MV
- Assets: Mix of growth and value stocks, multiple sectors

### Institutional Investor
- Model: Risk Parity or Worst Case Mean Variance
- Risk Measure: CVaR
- Assets: Multi-asset portfolio (stocks, bonds, commodities, REITs)

## Interpreting Results

### Portfolio Weights
- Weights sum to 100% (1.0)
- Values close to 0 indicate minimal or no allocation
- Concentrated weights may indicate high conviction or correlation

### Sharpe Ratio
- < 1: Poor risk-adjusted returns
- 1-2: Good risk-adjusted returns
- > 2: Excellent risk-adjusted returns

### Expected Return vs. Volatility
- Higher return usually comes with higher volatility
- The efficient frontier shows the optimal return/risk trade-offs
- Your optimized portfolio should be on or near the efficient frontier

## Troubleshooting

### "Optimization failed" Error
- Try different risk measure
- Increase the date range (need more data)
- Check that all tickers are valid
- Try a simpler model first

### Empty or Unrealistic Weights
- Some models may concentrate in few assets
- Try adding constraints (future feature)
- Use Risk Parity for more balanced allocation

### Data Download Fails
- Check internet connection
- Verify ticker symbols are correct
- Try fewer tickers
- Check if market is open (for latest data)

## Advanced Configuration

### Custom Parameters

**Risk-Free Rate**: 
- Use current Treasury bill rates (1-3 month)
- Default: 2.5% (adjust based on current rates)

**Risk Aversion (λ)**:
- Lower values (0.5-1): More aggressive
- Medium values (1-3): Balanced
- Higher values (3-10): More conservative

**Uncertainty Parameter (ε)**:
- Lower values (0.1-0.3): Less conservative
- Medium values (0.3-0.5): Balanced
- Higher values (0.5-1.0): More conservative

## API and Extensibility

The application is built with modular functions that can be reused:

```python
# Download data
prices = download_data(tickers, start_date, end_date)

# Optimize portfolio
weights, port = calculate_portfolio(prices, model, risk_measure, rf, risk_aversion, uncertainty)

# Calculate metrics
metrics = calculate_metrics(weights, port)
```

## References

- [Riskfolio-Lib Documentation](https://riskfolio-lib.readthedocs.io/)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Plotly Documentation](https://plotly.com/python/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Disclaimer**: This tool is for educational purposes only. Always consult with a financial advisor before making investment decisions.
