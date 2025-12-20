"""
Options-Derived Probability Density Function Calculator
Using SVI (Stochastic Volatility Inspired) fitting and Breeden-Litzenberger formula
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import yfinance as yf
from scipy.optimize import minimize
from scipy.stats import norm
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class OptionsPDFCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Options PDF Calculator - SVI Method")
        self.root.geometry("1400x900")
        
        # Create main frames
        self.create_input_frame()
        self.create_output_frame()
        self.create_plot_frame()
        
    def create_input_frame(self):
        """Create input controls"""
        input_frame = ttk.LabelFrame(self.root, text="Input Parameters", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Ticker input
        ttk.Label(input_frame, text="Ticker Symbol:").grid(row=0, column=0, padx=5, pady=5)
        self.ticker_entry = ttk.Entry(input_frame, width=15)
        self.ticker_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ticker_entry.insert(0, "SPY")
        
        # Calculate button
        self.calc_button = ttk.Button(input_frame, text="Calculate PDF", command=self.calculate_pdf)
        self.calc_button.grid(row=0, column=2, padx=20, pady=5)
        
        # Status label
        self.status_label = ttk.Label(input_frame, text="Ready", foreground="blue")
        self.status_label.grid(row=0, column=3, padx=5, pady=5)
        
    def create_output_frame(self):
        """Create output log area"""
        output_frame = ttk.LabelFrame(self.root, text="Optimization Details", padding=10)
        output_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, width=60)
        self.output_text.pack(fill="both", expand=True)
        
    def create_plot_frame(self):
        """Create plotting area"""
        plot_frame = ttk.LabelFrame(self.root, text="Visualizations", padding=10)
        plot_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        # Create figure with subplots
        self.fig = Figure(figsize=(10, 8))
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
        
    def log(self, message):
        """Add message to output log"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
        
    def black_scholes_call(self, S, K, T, r, sigma):
        """Black-Scholes call option price"""
        if T <= 0 or sigma <= 0:
            return max(S - K, 0)
        
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        call_price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
        return call_price
    
    def implied_volatility(self, market_price, S, K, T, r):
        """Calculate implied volatility using Newton-Raphson"""
        if market_price <= max(S - K*np.exp(-r*T), 0):
            return np.nan
            
        sigma = 0.3  # Initial guess
        
        for i in range(100):
            price = self.black_scholes_call(S, K, T, r, sigma)
            vega = S * norm.pdf((np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))) * np.sqrt(T)
            
            if abs(vega) < 1e-10:
                break
                
            diff = market_price - price
            
            if abs(diff) < 1e-6:
                return sigma
                
            sigma = sigma + diff/vega
            
            if sigma <= 0:
                return np.nan
                
        return sigma if sigma > 0 else np.nan
    
    def svi_variance(self, k, params):
        """SVI model for total variance: w(k) = a + b[ρ(k-m) + sqrt((k-m)^2 + σ^2)]"""
        a, b, rho, m, sigma = params
        return a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
    
    def svi_objective(self, params, k_data, var_data):
        """Objective function for SVI fitting"""
        predicted_var = self.svi_variance(k_data, params)
        return np.sum((predicted_var - var_data)**2)
    
    def fit_svi(self, strikes, IVs, forward, tau):
        """Fit SVI model to implied volatility smile"""
        self.log("\n=== Starting SVI Optimization ===")
        
        # Convert to log-moneyness
        k = np.log(strikes / forward)
        
        # Convert IV to total variance
        total_var = IVs**2 * tau
        
        # Initial guess for parameters [a, b, rho, m, sigma]
        atm_var = np.median(total_var)
        initial_guess = [atm_var, 0.1, 0.0, 0.0, 0.1]
        
        self.log(f"Initial guess: a={initial_guess[0]:.4f}, b={initial_guess[1]:.4f}, " +
                f"rho={initial_guess[2]:.4f}, m={initial_guess[3]:.4f}, sigma={initial_guess[4]:.4f}")
        
        # Constraints to prevent arbitrage
        bounds = [
            (0, None),      # a >= 0
            (0, None),      # b >= 0
            (-1, 1),        # -1 <= rho <= 1
            (None, None),   # m unbounded
            (1e-6, None)    # sigma > 0
        ]
        
        # Optimize
        self.log("Running optimization (L-BFGS-B algorithm)...")
        result = minimize(
            self.svi_objective,
            initial_guess,
            args=(k, total_var),
            method='L-BFGS-B',
            bounds=bounds
        )
        
        self.log(f"Optimization converged: {result.success}")
        self.log(f"Number of iterations: {result.nit}")
        self.log(f"Final error (SSE): {result.fun:.6f}")
        
        optimal_params = result.x
        self.log(f"\nOptimal parameters:")
        self.log(f"  a = {optimal_params[0]:.6f}")
        self.log(f"  b = {optimal_params[1]:.6f}")
        self.log(f"  rho = {optimal_params[2]:.6f}")
        self.log(f"  m = {optimal_params[3]:.6f}")
        self.log(f"  sigma = {optimal_params[4]:.6f}")
        
        return optimal_params, k
    
    def calculate_pdf_from_calls(self, strikes, call_prices, r, tau):
        """Extract PDF using Breeden-Litzenberger formula"""
        self.log("\n=== Extracting PDF via Breeden-Litzenberger ===")
        
        # Use finite differences for second derivative
        pdf_strikes = strikes[1:-1]
        pdf_values = np.zeros(len(pdf_strikes))
        
        for i in range(len(pdf_strikes)):
            # Second derivative: [C(K-h) - 2C(K) + C(K+h)] / h^2
            dK = strikes[i+1] - strikes[i]
            second_deriv = (call_prices[i] - 2*call_prices[i+1] + call_prices[i+2]) / (dK**2)
            
            # Multiply by discount factor
            pdf_values[i] = np.exp(r * tau) * second_deriv
        
        # Ensure non-negative and normalize
        pdf_values = np.maximum(pdf_values, 0)
        
        # Numerical integration for normalization
        integral = np.trapz(pdf_values, pdf_strikes)
        if integral > 0:
            pdf_values = pdf_values / integral
            
        self.log(f"PDF extracted at {len(pdf_strikes)} points")
        self.log(f"PDF integral (should be ~1.0): {np.trapz(pdf_values, pdf_strikes):.4f}")
        
        return pdf_strikes, pdf_values
    
    def calculate_pdf(self):
        """Main calculation pipeline"""
        try:
            self.output_text.delete(1.0, tk.END)
            self.status_label.config(text="Calculating...", foreground="orange")
            
            ticker = self.ticker_entry.get().upper().strip()
            self.log(f"Fetching options data for {ticker}...")
            
            # Fetch data
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('currentPrice', stock.info.get('regularMarketPrice'))
            
            if current_price is None:
                hist = stock.history(period='1d')
                current_price = hist['Close'].iloc[-1]
            
            self.log(f"Current stock price: ${current_price:.2f}")
            
            # Get options expirations
            expirations = stock.options
            if len(expirations) == 0:
                raise ValueError("No options data available")
            
            expiry = expirations[0]  # Use nearest expiration
            self.log(f"Using expiration: {expiry}")
            
            # Get options chain
            opt_chain = stock.option_chain(expiry)
            calls = opt_chain.calls
            
            # Filter and clean data
            calls = calls[calls['volume'] > 0]
            calls = calls[calls['bid'] > 0]
            calls = calls.sort_values('strike')
            
            self.log(f"Found {len(calls)} liquid call options")
            
            # Calculate time to expiration
            expiry_date = datetime.strptime(expiry, '%Y-%m-%d')
            today = datetime.now()
            tau = (expiry_date - today).days / 365.0
            
            self.log(f"Time to expiration: {tau:.4f} years ({tau*365:.0f} days)")
            
            # Risk-free rate (approximate)
            r = 0.05
            
            # Calculate implied volatilities
            strikes = calls['strike'].values
            market_prices = (calls['bid'] + calls['ask']).values / 2
            
            IVs = []
            valid_strikes = []
            valid_prices = []
            
            for i, (K, price) in enumerate(zip(strikes, market_prices)):
                iv = self.implied_volatility(price, current_price, K, tau, r)
                if not np.isnan(iv) and 0.05 < iv < 2.0:
                    IVs.append(iv)
                    valid_strikes.append(K)
                    valid_prices.append(price)
            
            strikes = np.array(valid_strikes)
            IVs = np.array(IVs)
            market_prices = np.array(valid_prices)
            
            self.log(f"Calculated IV for {len(IVs)} options")
            
            # Fit SVI model
            forward = current_price * np.exp(r * tau)
            optimal_params, k = self.fit_svi(strikes, IVs, forward, tau)
            
            # Generate smooth strikes for PDF extraction
            strike_min = strikes.min()
            strike_max = strikes.max()
            smooth_strikes = np.linspace(strike_min, strike_max, 200)
            
            # Calculate fitted IVs
            k_smooth = np.log(smooth_strikes / forward)
            fitted_var = self.svi_variance(k_smooth, optimal_params)
            fitted_IVs = np.sqrt(fitted_var / tau)
            
            # Generate smooth call prices from fitted IVs
            smooth_call_prices = np.array([
                self.black_scholes_call(current_price, K, tau, r, iv)
                for K, iv in zip(smooth_strikes, fitted_IVs)
            ])
            
            # Extract PDF
            pdf_strikes, pdf_values = self.calculate_pdf_from_calls(
                smooth_strikes, smooth_call_prices, r, tau
            )
            
            # Plot results
            self.plot_results(strikes, IVs, smooth_strikes, fitted_IVs, 
                            pdf_strikes, pdf_values, current_price)
            
            self.log("\n=== Calculation Complete ===")
            self.status_label.config(text="Complete!", foreground="green")
            
        except Exception as e:
            self.log(f"\nERROR: {str(e)}")
            self.status_label.config(text="Error", foreground="red")
            import traceback
            self.log(traceback.format_exc())
    
    def plot_results(self, strikes, IVs, smooth_strikes, fitted_IVs, 
                    pdf_strikes, pdf_values, current_price):
        """Plot IV smile and PDF"""
        self.ax1.clear()
        self.ax2.clear()
        
        # Plot 1: IV Smile with SVI fit
        self.ax1.scatter(strikes, IVs*100, alpha=0.6, s=50, label='Market IVs', color='blue')
        self.ax1.plot(smooth_strikes, fitted_IVs*100, 'r-', linewidth=2, label='SVI Fit')
        self.ax1.axvline(current_price, color='green', linestyle='--', alpha=0.5, label='Current Price')
        self.ax1.set_xlabel('Strike Price ($)')
        self.ax1.set_ylabel('Implied Volatility (%)')
        self.ax1.set_title('Implied Volatility Smile with SVI Fit')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # Plot 2: Probability Density Function
        self.ax2.fill_between(pdf_strikes, pdf_values, alpha=0.3, color='purple')
        self.ax2.plot(pdf_strikes, pdf_values, 'purple', linewidth=2, label='Risk-Neutral PDF')
        self.ax2.axvline(current_price, color='green', linestyle='--', alpha=0.5, label='Current Price')
        self.ax2.set_xlabel('Stock Price ($)')
        self.ax2.set_ylabel('Probability Density')
        self.ax2.set_title('Options-Derived Probability Density Function')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        
        self.fig.tight_layout()
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = OptionsPDFCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
