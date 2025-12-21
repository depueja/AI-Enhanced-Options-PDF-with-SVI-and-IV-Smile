"""
Options-Derived Probability Density Function Calculator
Core calculation engine with clean UI separation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import yfinance as yf
from scipy.optimize import minimize
from scipy.stats import norm
from datetime import datetime
import warnings
import re
warnings.filterwarnings('ignore')

# Import modules
try:
    from ai_analysis import analyze, is_ai_available
    AI_MODULE_AVAILABLE = True
except ImportError:
    AI_MODULE_AVAILABLE = False

try:
    from ui_components import (
        ThemeManager, FontManager, StyleConfigurator,
        enable_high_dpi, create_text_widget, 
        setup_matplotlib_style, style_plot_axes
    )
    UI_MODULE_AVAILABLE = True
except ImportError:
    UI_MODULE_AVAILABLE = False
    print("Warning: ui_components.py not found. Using basic styling.")

try:
    from features import FeatureMenu
    FEATURES_AVAILABLE = True
except ImportError:
    FEATURES_AVAILABLE = False
    print("Note: features.py not found. Advanced features disabled.")


class OptionsPDFCalculator:
    """Main application class - focuses on calculations"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Options PDF Calculator - SVI Method")
        self.root.geometry("1700x950")
        
        # Initialize UI components
        if UI_MODULE_AVAILABLE:
            enable_high_dpi()
            self.theme = ThemeManager(mode='dark')
            self.fonts = FontManager()
            self.style_config = StyleConfigurator(self.theme, self.fonts)
            self.style_config.configure_all()
            self.root.configure(bg=self.theme.get_color('bg'))
            setup_matplotlib_style(self.theme)
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.safe_quit)
        
        # State
        self.use_ai = tk.BooleanVar(value=False)
        self.last_results = None
        
        # Create UI
        self.create_interface()
        
        # Add feature menu if available
        if FEATURES_AVAILABLE and UI_MODULE_AVAILABLE:
            self.feature_menu = FeatureMenu(self.root, self)
    
    def create_interface(self):
        """Create main interface layout"""
        # Main paned window
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left and right frames
        if UI_MODULE_AVAILABLE:
            self.left_frame = ttk.Frame(self.main_paned, style='Card.TFrame')
            self.right_frame = ttk.Frame(self.main_paned, style='Card.TFrame')
        else:
            self.left_frame = ttk.Frame(self.main_paned)
            self.right_frame = ttk.Frame(self.main_paned)
        
        self.main_paned.add(self.left_frame, weight=1)
        self.main_paned.add(self.right_frame, weight=2)
        
        # Create sections
        self.create_input_section()
        self.create_output_section()
        self.create_plot_section()
    
    def create_input_section(self):
        """Create input controls"""
        style = 'Modern.TLabelframe' if UI_MODULE_AVAILABLE else 'TLabelframe'
        input_frame = ttk.LabelFrame(self.left_frame, text="  Input Parameters  ", 
                                     padding=15, style=style)
        input_frame.pack(fill="x", padx=8, pady=8)
        
        # Ticker input
        label_style = 'Modern.TLabel' if UI_MODULE_AVAILABLE else 'TLabel'
        ttk.Label(input_frame, text="Ticker Symbol:", style=label_style).grid(
            row=0, column=0, padx=8, pady=8, sticky="w")
        
        entry_style = 'Modern.TEntry' if UI_MODULE_AVAILABLE else 'TEntry'
        self.ticker_entry = ttk.Entry(input_frame, width=12, style=entry_style)
        self.ticker_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        self.ticker_entry.insert(0, "SPY")
        self.ticker_entry.bind('<Return>', lambda e: self.calculate_pdf())
        
        # AI toggle
        if AI_MODULE_AVAILABLE:
            ai_status = "✓ Ready" if is_ai_available() else "✗ SDK Missing"
        else:
            ai_status = "✗ Module Missing"
        
        check_style = 'Modern.TCheckbutton' if UI_MODULE_AVAILABLE else 'TCheckbutton'
        self.ai_checkbox = ttk.Checkbutton(
            input_frame,
            text=f"  AI Analysis ({ai_status})",
            variable=self.use_ai,
            style=check_style,
            command=self.on_ai_toggle
        )
        self.ai_checkbox.grid(row=0, column=2, padx=15, pady=8)
        
        if not AI_MODULE_AVAILABLE or not is_ai_available():
            self.ai_checkbox.state(['disabled'])
        
        # Buttons
        btn_style = 'Modern.TButton' if UI_MODULE_AVAILABLE else 'TButton'
        if UI_MODULE_AVAILABLE:
            btn_frame = ttk.Frame(input_frame, style='Card.TFrame')
        else:
            btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=0, columnspan=3, pady=15)
        
        self.calc_button = ttk.Button(btn_frame, text="Calculate PDF",
                                      command=self.calculate_pdf, style=btn_style)
        self.calc_button.pack(side="left", padx=8)
        
        self.quit_button = ttk.Button(btn_frame, text="Quit",
                                      command=self.safe_quit, style=btn_style)
        self.quit_button.pack(side="left", padx=8)
        
        # Status
        if UI_MODULE_AVAILABLE:
            fg_color = self.theme.get_color('success')
        else:
            fg_color = 'green'
        
        self.status_label = ttk.Label(input_frame, text="● Ready",
                                     foreground=fg_color, style=label_style)
        self.status_label.grid(row=2, column=0, columnspan=3, pady=8)
    
    def on_ai_toggle(self):
        """Handle AI toggle"""
        if self.use_ai.get():
            import os
            if not os.environ.get("ANTHROPIC_API_KEY"):
                messagebox.showwarning(
                    "API Key Not Found",
                    "ANTHROPIC_API_KEY not found.\n\n"
                    "Check your .env file or environment variables."
                )
                self.use_ai.set(False)
    
    def create_output_section(self):
        """Create output text areas"""
        self.output_paned = ttk.PanedWindow(self.left_frame, orient=tk.VERTICAL)
        self.output_paned.pack(fill="both", expand=True, padx=8, pady=8)
        
        style = 'Modern.TLabelframe' if UI_MODULE_AVAILABLE else 'TLabelframe'
        
        # Optimization details
        opt_frame = ttk.LabelFrame(self.output_paned, text="  Optimization Details  ",
                                   padding=10, style=style)
        self.output_paned.add(opt_frame, weight=1)
        
        if UI_MODULE_AVAILABLE:
            self.output_text = create_text_widget(opt_frame, self.theme, self.fonts, is_mono=True)
        else:
            from tkinter import scrolledtext
            self.output_text = scrolledtext.ScrolledText(opt_frame, height=8, width=50)
        
        self.output_text.pack(fill="both", expand=True)
        
        # Analysis
        analysis_frame = ttk.LabelFrame(self.output_paned, text="  Market Analysis  ",
                                       padding=10, style=style)
        self.output_paned.add(analysis_frame, weight=1)
        
        if UI_MODULE_AVAILABLE:
            self.analysis_text = create_text_widget(analysis_frame, self.theme, self.fonts, is_mono=False)
        else:
            from tkinter import scrolledtext
            self.analysis_text = scrolledtext.ScrolledText(analysis_frame, height=8, width=50)
        
        self.analysis_text.pack(fill="both", expand=True)
    
    def create_plot_section(self):
        """Create plot area"""
        style = 'Modern.TLabelframe' if UI_MODULE_AVAILABLE else 'TLabelframe'
        plot_frame = ttk.LabelFrame(self.right_frame, text="  Visualizations  ",
                                    padding=15, style=style)
        plot_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        if UI_MODULE_AVAILABLE:
            facecolor = self.theme.get_color('panel')
            subplot_color = self.theme.get_color('input')
        else:
            facecolor = '#161b22'
            subplot_color = '#21262d'
        
        self.fig = Figure(figsize=(11, 9), facecolor=facecolor, dpi=100)
        self.ax1 = self.fig.add_subplot(211, facecolor=subplot_color)
        self.ax2 = self.fig.add_subplot(212, facecolor=subplot_color)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def safe_quit(self):
        """Quit application"""
        if messagebox.askokcancel("Quit", "Quit application?"):
            self.root.quit()
            self.root.destroy()
    
    def log(self, message):
        """Log to optimization output"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def log_analysis(self, message):
        """Log to analysis output with bold support"""
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        
        # Parse **bold** syntax
        parts = re.split(r'(\*\*.*?\*\*)', message)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.analysis_text.insert(tk.END, part[2:-2], "bold")
            else:
                self.analysis_text.insert(tk.END, part)
        
        self.analysis_text.see(tk.END)
        self.root.update()
    
    # ==================== CALCULATION METHODS ====================
    
    def black_scholes_call(self, S, K, T, r, sigma):
        """Black-Scholes call option price"""
        if T <= 0 or sigma <= 0:
            return max(S - K, 0)
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    
    def implied_volatility(self, market_price, S, K, T, r):
        """Calculate implied volatility using Newton-Raphson"""
        if market_price <= max(S - K*np.exp(-r*T), 0):
            return np.nan
        sigma = 0.3
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
        """SVI model for total variance"""
        a, b, rho, m, sigma = params
        return a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
    
    def svi_objective(self, params, k_data, var_data):
        """Objective function for SVI fitting"""
        return np.sum((self.svi_variance(k_data, params) - var_data)**2)
    
    def fit_svi(self, strikes, IVs, forward, tau):
        """Fit SVI model to implied volatility smile"""
        self.log("\n=== Starting SVI Optimization ===")
        k = np.log(strikes / forward)
        total_var = IVs**2 * tau
        atm_var = np.median(total_var)
        initial_guess = [atm_var, 0.1, 0.0, 0.0, 0.1]
        
        self.log(f"Initial: a={initial_guess[0]:.4f}, b={initial_guess[1]:.4f}, " +
                f"rho={initial_guess[2]:.4f}, m={initial_guess[3]:.4f}, sigma={initial_guess[4]:.4f}")
        
        bounds = [(0, None), (0, None), (-1, 1), (None, None), (1e-6, None)]
        
        self.log("Running optimization (L-BFGS-B)...")
        result = minimize(self.svi_objective, initial_guess, 
                         args=(k, total_var), method='L-BFGS-B', bounds=bounds)
        
        self.log(f"Converged: {result.success}, Iterations: {result.nit}, Error: {result.fun:.6f}")
        self.log(f"\nOptimal: a={result.x[0]:.6f}, b={result.x[1]:.6f}, " +
                f"rho={result.x[2]:.6f}, m={result.x[3]:.6f}, sigma={result.x[4]:.6f}")
        
        return result.x, k
    
    def calculate_pdf_from_calls(self, strikes, call_prices, r, tau):
        """Extract PDF using Breeden-Litzenberger"""
        self.log("\n=== Extracting PDF via Breeden-Litzenberger ===")
        pdf_strikes = strikes[1:-1]
        pdf_values = np.zeros(len(pdf_strikes))
        
        for i in range(len(pdf_strikes)):
            dK = strikes[i+1] - strikes[i]
            second_deriv = (call_prices[i] - 2*call_prices[i+1] + call_prices[i+2]) / (dK**2)
            pdf_values[i] = np.exp(r * tau) * second_deriv
        
        pdf_values = np.maximum(pdf_values, 0)
        integral = np.trapz(pdf_values, pdf_strikes)
        if integral > 0:
            pdf_values = pdf_values / integral
        
        self.log(f"PDF extracted at {len(pdf_strikes)} points, integral: {np.trapz(pdf_values, pdf_strikes):.4f}")
        return pdf_strikes, pdf_values
    
    def calculate_pdf(self):
        """Main calculation pipeline"""
        try:
            self.output_text.delete(1.0, tk.END)
            self.analysis_text.delete(1.0, tk.END)
            
            if UI_MODULE_AVAILABLE:
                self.status_label.config(text="● Calculating...", 
                                       foreground=self.theme.get_color('warning'))
            else:
                self.status_label.config(text="● Calculating...", foreground='orange')
            
            self.root.update()
            
            ticker = self.ticker_entry.get().upper().strip()
            if not ticker:
                messagebox.showerror("Error", "Enter a ticker symbol.")
                return
            
            self.log(f"Fetching options data for {ticker}...")
            
            # Fetch data
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('currentPrice', stock.info.get('regularMarketPrice'))
            if current_price is None:
                hist = stock.history(period='1d')
                if hist.empty:
                    raise ValueError("Ticker not found")
                current_price = hist['Close'].iloc[-1]
            
            self.log(f"Current price: ${current_price:.2f}")
            
            expirations = stock.options
            if not expirations:
                raise ValueError("No options available")
            
            expiry = expirations[0]
            self.log(f"Expiration: {expiry}")
            
            # Get options chain
            calls = stock.option_chain(expiry).calls
            calls = calls[(calls['volume'] > 0) & (calls['bid'] > 0)].sort_values('strike')
            
            if len(calls) < 5:
                raise ValueError("Insufficient liquid options")
            
            self.log(f"Found {len(calls)} liquid calls")
            
            # Calculate time to expiration
            tau = (datetime.strptime(expiry, '%Y-%m-%d') - datetime.now()).days / 365.0
            self.log(f"Time to expiry: {tau:.4f} years ({tau*365:.0f} days)")
            
            r = 0.05  # Risk-free rate
            
            # Calculate IVs
            strikes, IVs = [], []
            for K, price in zip(calls['strike'].values, ((calls['bid'] + calls['ask'])/2).values):
                iv = self.implied_volatility(price, current_price, K, tau, r)
                if not np.isnan(iv) and 0.05 < iv < 2.0:
                    strikes.append(K)
                    IVs.append(iv)
            
            strikes, IVs = np.array(strikes), np.array(IVs)
            self.log(f"Calculated IV for {len(IVs)} options")
            
            # Fit SVI
            forward = current_price * np.exp(r * tau)
            optimal_params, k = self.fit_svi(strikes, IVs, forward, tau)
            
            # Generate smooth curve
            smooth_strikes = np.linspace(strikes.min(), strikes.max(), 200)
            k_smooth = np.log(smooth_strikes / forward)
            fitted_var = self.svi_variance(k_smooth, optimal_params)
            fitted_IVs = np.sqrt(fitted_var / tau)
            
            smooth_call_prices = np.array([
                self.black_scholes_call(current_price, K, tau, r, iv)
                for K, iv in zip(smooth_strikes, fitted_IVs)
            ])
            
            # Extract PDF
            pdf_strikes, pdf_values = self.calculate_pdf_from_calls(
                smooth_strikes, smooth_call_prices, r, tau
            )
            
            # Store results
            self.last_results = {
                'ticker': ticker, 'current_price': current_price,
                'strikes': strikes, 'IVs': IVs,
                'fitted_IVs': fitted_IVs, 'smooth_strikes': smooth_strikes,
                'pdf_strikes': pdf_strikes, 'pdf_values': pdf_values,
                'tau': tau, 'expiry': expiry, 'optimal_params': optimal_params
            }
            
            # Plot and analyze
            self.plot_results(strikes, IVs, smooth_strikes, fitted_IVs,
                            pdf_strikes, pdf_values, current_price, ticker)
            
            if AI_MODULE_AVAILABLE:
                analysis = analyze(self.last_results, use_ai=self.use_ai.get())
            else:
                analysis = "⚠️ ai_analysis.py not found."
            
            self.log_analysis(analysis)
            self.log("\n=== Complete ===")
            
            if UI_MODULE_AVAILABLE:
                self.status_label.config(text="● Complete!", 
                                       foreground=self.theme.get_color('success'))
            else:
                self.status_label.config(text="● Complete!", foreground='green')
            
        except Exception as e:
            self.log(f"\nERROR: {str(e)}")
            messagebox.showerror("Error", str(e))
            if UI_MODULE_AVAILABLE:
                self.status_label.config(text="● Error", 
                                       foreground=self.theme.get_color('error'))
            else:
                self.status_label.config(text="● Error", foreground='red')
    
    def plot_results(self, strikes, IVs, smooth_strikes, fitted_IVs,
                    pdf_strikes, pdf_values, current_price, ticker):
        """Plot IV smile and PDF"""
        self.ax1.clear()
        self.ax2.clear()
        
        # Get colors
        if UI_MODULE_AVAILABLE:
            market_color = self.theme.get_chart_color('market')
            fit_color = self.theme.get_chart_color('fit')
            current_color = self.theme.get_chart_color('current')
            pdf_color = self.theme.get_chart_color('pdf')
            fg = self.theme.get_color('fg')
        else:
            market_color, fit_color, current_color, pdf_color = '#58a6ff', '#f85149', '#3fb950', '#bc8cff'
            fg = '#e6edf3'
        
        # Plot 1: IV Smile
        self.ax1.scatter(strikes, IVs*100, alpha=0.8, s=60, 
                        color=market_color, edgecolors='white', linewidths=0.5, label='Market IVs')
        self.ax1.plot(smooth_strikes, fitted_IVs*100, color=fit_color, 
                     linewidth=3, alpha=0.9, label='SVI Fit')
        self.ax1.axvline(current_price, color=current_color, linestyle='--', 
                        alpha=0.7, linewidth=2.5, label='Current Price')
        self.ax1.set_xlabel('Strike Price ($)', fontsize=12, color=fg, fontweight='500')
        self.ax1.set_ylabel('Implied Volatility (%)', fontsize=12, color=fg, fontweight='500')
        self.ax1.set_title(f'{ticker} - Implied Volatility Smile', 
                          fontsize=14, color=fg, pad=20, fontweight='600')
        self.ax1.legend(fontsize=10)
        
        # Plot 2: PDF
        self.ax2.fill_between(pdf_strikes, pdf_values, alpha=0.4, color=pdf_color)
        self.ax2.plot(pdf_strikes, pdf_values, color=pdf_color, 
                     linewidth=3, alpha=0.9, label='Risk-Neutral PDF')
        self.ax2.axvline(current_price, color=current_color, linestyle='--', 
                        alpha=0.7, linewidth=2.5, label='Current Price')
        self.ax2.set_xlabel('Stock Price ($)', fontsize=12, color=fg, fontweight='500')
        self.ax2.set_ylabel('Probability Density', fontsize=12, color=fg, fontweight='500')
        self.ax2.set_title(f'{ticker} - Probability Density Function', 
                          fontsize=14, color=fg, pad=20, fontweight='600')
        self.ax2.legend(fontsize=10)
        
        # Apply theme styling
        if UI_MODULE_AVAILABLE:
            style_plot_axes(self.ax1, self.theme)
            style_plot_axes(self.ax2, self.theme)
        
        self.fig.tight_layout(pad=3.0)
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = OptionsPDFCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()