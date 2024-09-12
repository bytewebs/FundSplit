import os
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from data_processing import preprocess_data
from esg_analysis import generate_mock_esg_scores, esg_analysis
from sentiment_analysis import simulate_sentiment_analysis_impact, analyze_sentiment
from macro_analysis import generate_random_macro_data, macro_analysis
from technical_analysis import add_technical_indicators

# Define global variables
base_dir = os.path.dirname(os.path.dirname(os.path.abspath('nifty.csv')))
data_dir = os.path.join(base_dir, 'data')
default_path = 'nifty.csv'

# Investment Allocation Functions
def get_allocation(capital, time_horizon, risk_tolerance):
    # Define specific scenarios
    if capital < 100000 and risk_tolerance == 'low' and time_horizon > 5:
        safe = 55
        hedge = 25
        volatile = 20
    elif capital > 1000000 and risk_tolerance == 'low' and time_horizon > 5:
        safe = 55
        hedge = 25
        volatile = 20
    else:
        # General scenarios based on weighted score-like logic
        weighted_score = get_weighted_score(capital, time_horizon, risk_tolerance)

        if weighted_score <= 4:
            safe = 60 - (weighted_score * 3)
            hedge = 30 - (weighted_score * 2)
            volatile = 10 + (weighted_score * 5)
        elif weighted_score <= 7:
            safe = 50 - ((weighted_score - 4) * 5)
            hedge = 30 - ((weighted_score - 4) * 4)
            volatile = 20 + ((weighted_score - 4) * 9)
        else:
            safe = 30 - ((weighted_score - 7) * 6)
            hedge = 30 - ((weighted_score - 7) * 4)
            volatile = 40 + ((weighted_score - 7) * 10)

    return {'safe': safe, 'hedge': hedge, 'volatile': volatile}

def get_weighted_score(capital, time_horizon, risk_tolerance):
    # Define weights
    weights = {
        'capital': 0.30,
        'time_horizon': 0.30,
        'risk_tolerance': 0.40,
    }

    # Define scoring ranges
    capital_score = get_capital_score(capital)
    time_horizon_score = get_time_horizon_score(time_horizon)
    risk_tolerance_score = get_risk_tolerance_score(risk_tolerance)

    # Calculate the weighted score
    weighted_score = (
        capital_score * weights['capital'] +
        time_horizon_score * weights['time_horizon'] +
        risk_tolerance_score * weights['risk_tolerance']
    )

    return weighted_score

def get_capital_score(capital):
    if capital > 1000000:
        return 10
    elif capital >= 400000:
        return 7
    else:
        return 5

def get_time_horizon_score(time_horizon):
    if time_horizon > 5:
        return 10
    elif time_horizon >= 3:
        return 7
    else:
        return 5

def get_risk_tolerance_score(risk_tolerance):
    if risk_tolerance == 'high':
        return 10
    elif risk_tolerance == 'medium':
        return 7
    elif risk_tolerance == 'low':
        return 5
    else:
        return 0

# Stock Market Evaluation Functions
def evaluate_score(score):
    if score >= 0.7:
        return "Positive"
    elif score >= 0.3:
        return "Neutral"
    else:
        return "Negative"

def evaluate_stock_market():
    try:
        nifty_data = preprocess_data(default_path)
        nifty_data = nifty_data[nifty_data['Date'].dt.year.between(2000, 2023)]
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return None
    except KeyError as e:
        print(f"KeyError: {e}")
        return None

    # Add technical indicators to Nifty data
    nifty_data_with_indicators = add_technical_indicators(nifty_data)
    print("Nifty Data with Technical Indicators:")
    print(nifty_data_with_indicators.head())

    # Ensure 'MACD' and 'MACD_Signal' columns exist
    if 'MACD' not in nifty_data_with_indicators.columns or 'MACD_Signal' not in nifty_data_with_indicators.columns:
        print("MACD columns are missing in the data.")
        return

    # Evaluate Technical Indicators
    sma_50_above_sma_200 = (nifty_data_with_indicators['SMA_50'].iloc[-1] > nifty_data_with_indicators['SMA_200'].iloc[-1])
    rsi_below_70 = (nifty_data_with_indicators['RSI'].iloc[-1] < 70)
    rsi_above_30 = (nifty_data_with_indicators['RSI'].iloc[-1] > 30)
    macd_positive = (nifty_data_with_indicators['MACD'].iloc[-1] > nifty_data_with_indicators['MACD_Signal'].iloc[-1])

    technical_score = sum([sma_50_above_sma_200, rsi_below_70, rsi_above_30, macd_positive]) / 4
    technical_outlook = evaluate_score(technical_score)

    # Evaluate ESG Scores
    assets = ['Nifty']
    esg_scores = generate_mock_esg_scores(assets)
    high_esg_assets = esg_analysis(esg_scores)
    esg_score = len(high_esg_assets) / len(assets)
    esg_outlook = evaluate_score(esg_score)

    # Evaluate Macroeconomic Indicators
    macro_indicators = generate_random_macro_data(24)
    gdp_growth, interest_rate = macro_analysis(macro_indicators)
    macro_score = (gdp_growth > 0) and (interest_rate < 5)  # Simplified evaluation criteria
    macro_outlook = "Positive" if macro_score else "Negative"

    # Evaluate Sentiment Analysis
    news_data_with_sentiment = simulate_sentiment_analysis_impact()
    average_sentiment = news_data_with_sentiment['Sentiment'].mean()
    sentiment_score = average_sentiment > 0
    sentiment_outlook = "Positive" if sentiment_score else "Negative"

    # Combine Scores
    overall_score = (technical_score + esg_score + macro_score + sentiment_score) / 4
    overall_outlook = "Positive" if overall_score > 0.5 else "Negative"

    print(f"Technical Score: {technical_outlook} ({technical_score})")
    print(f"ESG Score: {esg_outlook} ({esg_score})")
    print(f"Macro Score: {macro_outlook} ({macro_score})")
    print(f"Sentiment Score: {sentiment_outlook} ({sentiment_score})")
    print(f"Overall Score: {overall_outlook} ({overall_score})")

    return {"overall": {"outlook": overall_outlook, "score": overall_score}}

# Asset Selection Functions
def select_assets(sections, safe_percentage, hedge_percentage, volatile_percentage, market_outlook):
    selected_assets = {'safe': [], 'hedge': [], 'volatile': []}

    if market_outlook == "Positive":
        safe_assets = sections['A']['safe'][:3]
        hedge_assets = sections['B']['hedge'][:3]
        volatile_assets = sections['C']['volatile'][:3]
    elif market_outlook == "Neutral":
        safe_assets = sections['A']['safe'][:3]
        hedge_assets = sections['B']['hedge'][:3]
        volatile_assets = sections['C']['volatile'][:3]
    else:
        safe_assets = sections['A']['safe'][:3]
        hedge_assets = sections['B']['hedge'][:3]
        volatile_assets = sections['C']['volatile'][:3]

    selected_assets['safe'] = safe_assets
    selected_assets['hedge'] = hedge_assets
    selected_assets['volatile'] = volatile_assets

    return selected_assets

# GUI Application
def submit_allocation():
    capital = float(capital_entry.get())
    risk_tolerance = risk_tolerance_var.get()
    time_horizon = int(time_horizon_entry.get())

    allocation = get_allocation(capital, time_horizon, risk_tolerance)
    market_evaluation = evaluate_stock_market()

    if market_evaluation is None:
        output_text.set("Error in evaluating market conditions.")
        return

    market_outlook = market_evaluation["overall"]["outlook"]

    sections = {
        'A': {
            'safe': ['Reliance Industries Limited (RELIANCE) - Stock', 'Tata Consultancy Services (TCS) - Stock', 'HDFC Bank Limited (HDFCBANK) - Stock',
                     'Government of India 7.26% 2029 Bond (IN0020180017)', 'Government of India 7.72% 2051 Bond (IN0020220074)',
                     'Government of India 6.84% 2022 Bond (IN0020160041)', 'Government of India 6.10% 2031 Bond (IN0020210058)',
                     'Government of India 5.63% 2026 Bond (IN0020210074)', 'Nippon India ETF Nifty BeES (NIFTYBEES)', 'SBI ETF Nifty 50 (SETFNIF50)',
                     'HDFC NIFTY ETF (HDFCNIFTY)', 'ICICI Prudential Nifty ETF (ICICINIFTY)', 'UTI Nifty Next 50 ETF (UTINEXT50)'],
            'hedge': [],
            'volatile': ['Adani Enterprises Limited (ADANIENT) - Stock', 'Bharti Airtel Limited (BHARTIARTL) - Stock', 'Infosys Limited (INFY) - Stock',
                         'Kotak Banking ETF (KOTAKBKETF) - ETF', 'ICICI Prudential Nifty ETF (ICICINETF) - ETF',
                         'Aditya Birla Sun Life Nifty ETF (ABSLNIFTY) - ETF', 'BBB-rated Corporate Bonds (BBB-CORP) - Bond',
                         'High-Yield Municipal Bonds (HY-MUNI) - Bond', 'Emerging Market Bonds (EM-BOND) - Bond']
        },
        'B': {
            'safe': ['Gold', 'Silver', 'Platinum', 'Palladium', 'Copper', 'Crude Oil (Brent)', 'Natural Gas',
                     'US Dollar (USD)', 'Euro (EUR)', 'Japanese Yen (JPY)', 'Swiss Franc (CHF)',
                     'British Pound (GBP)', 'Canadian Dollar (CAD)', 'Australian Dollar (AUD)'],
            'hedge': ['Aluminum', 'Zinc', 'Nickel', 'Corn', 'Soybeans', 'Wheat', 'Coffee',
                      'Singapore Dollar (SGD)', 'Hong Kong Dollar (HKD)', 'New Zealand Dollar (NZD)',
                      'South Korean Won (KRW)', 'Norwegian Krone (NOK)', 'Swedish Krona (SEK)',
                      'Danish Krone (DKK)'],
            'volatile': ['Cocoa', 'Cotton', 'Sugar', 'Rubber', 'Ethanol', 'Lumber', 'Lithium',
                         'South African Rand (ZAR)', 'Turkish Lira (TRY)', 'Brazilian Real (BRL)',
                         'Russian Ruble (RUB)', 'Indian Rupee (INR)', 'Mexican Peso (MXN)',
                         'Argentine Peso (ARS)', 'Aluminum', 'Zinc', 'Nickel', 'Corn', 'Soybeans', 'Wheat', 'Coffee',
                         'Singapore Dollar (SGD)', 'Hong Kong Dollar (HKD)', 'New Zealand Dollar (NZD)',
                         'South Korean Won (KRW)', 'Norwegian Krone (NOK)', 'Swedish Krona (SEK)',
                         'Danish Krone (DKK)']
        },
        'C': {
            'safe': ['Bitcoin (BTC)', 'Ethereum (ETH)', 'Binance Coin (BNB)', 'USD Coin (USDC)',
                     'Tether (USDT)', 'Cardano (ADA)', 'Polkadot (DOT)'],
            'hedge': ['Solana (SOL)', 'Chainlink (LINK)', 'Polygon (MATIC)', 'Avalanche (AVAX)',
                      'Litecoin (LTC)', 'Algorand (ALGO)', 'VeChain (VET)'],
            'volatile': ['Dogecoin (DOGE)', 'Shiba Inu (SHIB)', 'SafeMoon (SAFEMOON)', 'Elrond (EGLD)',
                         'Theta (THETA)', 'Hedera Hashgraph (HBAR)', 'Zilliqa (ZIL)', 'Solana (SOL)', 'Chainlink (LINK)', 'Polygon (MATIC)', 'Avalanche (AVAX)',
                         'Litecoin (LTC)', 'Algorand (ALGO)', 'VeChain (VET)']
        }
    }
    selected_assets = select_assets(sections, allocation['safe'], allocation['hedge'], allocation['volatile'], market_outlook)

    result_text = f"Allocation:\nSafe: {allocation['safe']}%\nHedge: {allocation['hedge']}%\nVolatile: {allocation['volatile']}%\n\nSelected Assets:\n"
    for category, assets in selected_assets.items():
        result_text += f"{category.capitalize()}:\n"
        for asset in assets:
            result_text += f"  - {asset}\n"

    output_text.set(result_text)

# Create the main Tkinter window
window = tk.Tk()
window.title("Investment Allocation Tool")
window.geometry("500x400")
window.resizable(False, False)

# Create a frame for the form inputs
form_frame = tk.Frame(window, padx=10, pady=10)
form_frame.grid(row=0, column=0, padx=10, pady=10)

# Capital input
tk.Label(form_frame, text="Capital:").grid(row=0, column=0, sticky='w')
capital_entry = tk.Entry(form_frame)
capital_entry.grid(row=0, column=1)

# Risk tolerance input
tk.Label(form_frame, text="Risk Tolerance:").grid(row=1, column=0, sticky='w')
risk_tolerance_var = tk.StringVar()
risk_tolerance_combobox = ttk.Combobox(form_frame, textvariable=risk_tolerance_var)
risk_tolerance_combobox['values'] = ('low', 'medium', 'high')
risk_tolerance_combobox.grid(row=1, column=1)

# Time horizon input
tk.Label(form_frame, text="Time Horizon (years):").grid(row=2, column=0, sticky='w')
time_horizon_entry = tk.Entry(form_frame)
time_horizon_entry.grid(row=2, column=1)

# Submit button
submit_button = tk.Button(form_frame, text="Submit", command=submit_allocation)
submit_button.grid(row=3, columnspan=2, pady=10)

# Output text
output_text = tk.StringVar()
output_label = tk.Label(window, textvariable=output_text, justify='left', anchor='w', padx=10, pady=10)
output_label.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

# Start the Tkinter event loop
window.mainloop()