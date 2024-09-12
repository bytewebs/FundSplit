import tkinter as tk
from tkinter import ttk, messagebox

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
    if (capital > 1000000): return 10
    if (capital >= 400000): return 7
    return 5

def get_time_horizon_score(time_horizon):
    if (time_horizon > 5): return 10
    if (time_horizon >= 3): return 7
    return 5

def get_risk_tolerance_score(risk_tolerance):
    if (risk_tolerance == 'high'): return 10
    if (risk_tolerance == 'medium'): return 7
    if (risk_tolerance == 'low'): return 5
    return 0

def calculate_allocation():
    try:
        capital = float(capital_entry.get())
        time_horizon = int(time_horizon_entry.get())
        risk_tolerance = risk_tolerance_var.get().lower()

        allocation = get_allocation(capital, time_horizon, risk_tolerance)
        allocation_label.config(text=f"Safe: {allocation['safe']}%\nHedge: {allocation['hedge']}%\nVolatile: {allocation['volatile']}%")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numerical values for capital and time horizon.")

# Create the main application window
root = tk.Tk()
root.title("Investment Allocation Tool")

# Create a frame for the form
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add form fields
ttk.Label(frame, text="Capital (INR)").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
capital_entry = ttk.Entry(frame)
capital_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

ttk.Label(frame, text="Time Horizon (years)").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
time_horizon_entry = ttk.Entry(frame)
time_horizon_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

ttk.Label(frame, text="Risk Tolerance").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
risk_tolerance_var = tk.StringVar()
risk_tolerance_combobox = ttk.Combobox(frame, textvariable=risk_tolerance_var, state="readonly")
risk_tolerance_combobox['values'] = ("Low", "Medium", "High")
risk_tolerance_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
risk_tolerance_combobox.current(0)

# Add the calculate button
calculate_button = ttk.Button(frame, text="Calculate Allocation", command=calculate_allocation)
calculate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Add the results label
allocation_label = ttk.Label(frame, text="", font=("Arial", 12))
allocation_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Run the application
root.mainloop()
