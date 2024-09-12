import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from data_processing import preprocess_data
from esg_analysis import generate_mock_esg_scores, esg_analysis
from sentiment_analysis import simulate_sentiment_analysis_impact, analyze_sentiment
from macro_analysis import generate_random_macro_data, macro_analysis
from technical_analysis import add_technical_indicators
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Define global variables
base_dir = os.path.dirname(os.path.dirname(os.path.abspath('./data/nifty.csv')))
data_dir = os.path.join(base_dir, 'data')
default_path = r'C:\Users\91808\OneDrive\Desktop\hack\portfolio_analysis\data\nifty.csv'

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

    try:
        esg_scores = generate_mock_esg_scores(nifty_data)
    except ValueError as e:
        print(f"ValueError: {e}")
        return None

    sentiment_scores = simulate_sentiment_analysis_impact(nifty_data)
    macro_data = generate_random_macro_data()

    esg_result = esg_analysis(esg_scores)
    sentiment_result = analyze_sentiment(sentiment_scores)
    macro_result = macro_analysis(macro_data)

    overall_score = (esg_result + sentiment_result + macro_result) / 3
    market_outlook = evaluate_score(overall_score)

    return market_outlook

# Asset Selection Functions
def select_assets(sections, safe_percentage, hedge_percentage, volatile_percentage, market_outlook):
    selected_assets = {
        'safe': [],
        'hedge': [],
        'volatile': []
    }

    if market_outlook == "Positive":
        safe_assets = sections['A']['safe']
        hedge_assets = sections['B']['safe']
        volatile_assets = sections['C']['high_risk']
    else:
        safe_assets = sections['B']['safe']
        hedge_assets = sections['A']['safe']
        volatile_assets = sections['C']['high_risk']

    # Select 3 assets from each class dynamically
    selected_assets['safe'] = safe_assets[:3]
    selected_assets['hedge'] = hedge_assets[:3]
    selected_assets['volatile'] = volatile_assets[:3]

    return selected_assets

# GUI Application
def submit_allocation():
    capital = float(capital_entry.get())
    risk_tolerance = risk_tolerance_var.get()
    time_horizon = int(time_horizon_entry.get())

    allocation = get_allocation(capital, time_horizon, risk_tolerance)
    market_outlook = evaluate_stock_market()

    if market_outlook is None:
        output_text.set("Error in evaluating market conditions.")
        return

    sections = {
        'A': {
            'safe': ['Reliance Industries Limited (RELIANCE) - Stock', 'Tata Consultancy Services (TCS) - Stock', 'HDFC Bank Limited (HDFCBANK) - Stock',
                     'Nippon India ETF Nifty BeES (NIFTYBEES) - ETF', 'SBI ETF Nifty 50 (SETFNIF50) - ETF', 'HDFC NIFTY ETF (HDFCNIFTY) - ETF',
                     'ICICI Prudential Nifty ETF (ICICINIFTY) - ETF', 'UTI Nifty Next 50 ETF (UTINEXT50) - ETF'],
            'medium_risk': ['Tata Consultancy Services (TCS) - Stock', 'HDFC Bank Limited (HDFCBANK) - Stock', 'Infosys Limited (INFY) - Stock',
                            'Hindustan Unilever Limited (HINDUNILVR) - Stock', 'Aditya Birla Capital Limited (ABCAPITAL) - Stock', 'Bharat Forge Limited (BHARATFORG) - Stock',
                            'Glenmark Pharmaceuticals Limited (GLENMARK) - Stock', 'Muthoot Finance Limited (MUTHOOTFIN) - Stock', 'Page Industries Limited (PAGEIND) - Stock'],
            'high_risk': ['Alok Industries Limited (ALOKINDS) - Stock', 'South Indian Bank Limited (SOUTHBANK) - Stock', 'Himachal Futuristic Communications Limited (HFCL) - Stock',
                          'Vodafone Idea Limited (IDEA) - Stock', 'GTL Infrastructure Limited (GTLINFRA) - Stock', 'Glenmark Pharmaceuticals Limited (GLENMARK) - Stock',
                          'Muthoot Finance Limited (MUTHOOTFIN) - Stock', 'Page Industries Limited (PAGEIND) - Stock']
        },
        'B': {
            'safe': ['Government of India 7.26% 2029 Bond (IN0020180017) - Bond', 'Government of India 7.72% 2051 Bond (IN0020220074) - Bond', 'Government of India 6.84% 2022 Bond (IN0020160041) - Bond',
                     'Government of India 6.10% 2031 Bond (IN0020210058) - Bond', 'Government of India 5.63% 2026 Bond (IN0020210074) - Bond', 'Government of India 7.17% 2028 Bond (IN0020170043) - Bond',
                     'Government of India 6.19% 2034 Bond (IN0020210090) - Bond', 'Government of India 7.88% 2030 Bond (IN0020150036) - Bond', 'Government of India 6.79% 2029 Bond (IN0020180033) - Bond',
                     'Government of India 7.95% 2032 Bond (IN0020120043) - Bond'],
            'medium_risk': ['Ahmedabad Municipal Corporation Bond - Bond', 'Pune Municipal Corporation Bond - Bond', 'Hyderabad Municipal Corporation Bond - Bond',
                            'Indore Municipal Corporation Bond - Bond', 'Visakhapatnam Municipal Corporation Bond - Bond', 'Lucknow Municipal Corporation Bond - Bond',
                            'Surat Municipal Corporation Bond - Bond', 'Kolkata Municipal Corporation Bond - Bond', 'Bangalore Municipal Corporation Bond - Bond',
                            'Chennai Municipal Corporation Bond - Bond']
        },
        'C': {
            'safe': ['Gold (XAU) - Commodity', 'Silver (XAG) - Commodity', 'Platinum (XPT) - Commodity', 'Palladium (XPD) - Commodity', 'Oil (WTI) - Commodity'],
            'medium_risk': ['Bitcoin (BTC) - Cryptocurrency', 'Ethereum (ETH) - Cryptocurrency', 'Ripple (XRP) - Cryptocurrency', 'Litecoin (LTC) - Cryptocurrency',
                            'Bitcoin Cash (BCH) - Cryptocurrency', 'Cardano (ADA) - Cryptocurrency', 'Solana (SOL) - Cryptocurrency'],
            'high_risk': ['Indian Rupee (INR) - Currency Pair', 'US Dollar (USD) - Currency Pair', 'Euro (EUR) - Currency Pair', 'British Pound (GBP) - Currency Pair',
                          'Japanese Yen (JPY) - Currency Pair', 'Australian Dollar (AUD) - Currency Pair', 'Canadian Dollar (CAD) - Currency Pair', 'Swiss Franc (CHF) - Currency Pair']
        }
    }

    safe_assets, hedge_assets, volatile_assets = select_assets(sections, allocation['safe'], allocation['hedge'], allocation['volatile'], market_outlook)

    safe_percentage = allocation['safe']
    hedge_percentage = allocation['hedge']
    volatile_percentage = allocation['volatile']

    output_text.set(f"Safe Assets ({safe_percentage}%): {', '.join(safe_assets)}\n"
                    f"Hedge Assets ({hedge_percentage}%): {', '.join(hedge_assets)}\n"
                    f"Volatile Assets ({volatile_percentage}%): {', '.join(volatile_assets)}\n"
                    f"Market Outlook: {market_outlook}")

# GUI Setup
app = tk.Tk()
app.title("Portfolio Allocation")

capital_label = tk.Label(app, text="Capital:")
capital_label.grid(row=0, column=0)
capital_entry = tk.Entry(app)
capital_entry.grid(row=0, column=1)

time_horizon_label = tk.Label(app, text="Time Horizon (years):")
time_horizon_label.grid(row=1, column=0)
time_horizon_entry = tk.Entry(app)
time_horizon_entry.grid(row=1, column=1)

risk_tolerance_label = tk.Label(app, text="Risk Tolerance:")
risk_tolerance_label.grid(row=2, column=0)
risk_tolerance_var = tk.StringVar()
risk_tolerance_dropdown = ttk.Combobox(app, textvariable=risk_tolerance_var)
risk_tolerance_dropdown['values'] = ('low', 'medium', 'high')
risk_tolerance_dropdown.grid(row=2, column=1)

submit_button = tk.Button(app, text="Submit", command=submit_allocation)
submit_button.grid(row=3, column=1)

output_text = tk.StringVar()
output_label = tk.Label(app, textvariable=output_text, wraplength=400)
output_label.grid(row=4, column=0, columnspan=2)

app.mainloop()
