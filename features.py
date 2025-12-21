"""
Extra Features for Options PDF Calculator
Handles exports, theme switching, and other non-essential features
"""

import os
from tkinter import filedialog, messagebox
from datetime import datetime


class ExportManager:
    """Handles exporting plots and data"""
    
    def __init__(self):
        self.last_export_dir = os.path.expanduser("~")
    
    def export_plot_png(self, fig, ticker):
        """Export current plot as PNG
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            Figure to export
        ticker : str
            Ticker symbol for filename
        
        Returns:
        --------
        bool : Success status
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"{ticker}_options_analysis_{timestamp}.png"
            
            filepath = filedialog.asksaveasfilename(
                initialdir=self.last_export_dir,
                title="Export Plot as PNG",
                defaultextension=".png",
                initialfile=default_name,
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if filepath:
                fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                           facecolor=fig.get_facecolor())
                self.last_export_dir = os.path.dirname(filepath)
                messagebox.showinfo("Export Successful", 
                                  f"Plot saved to:\n{filepath}")
                return True
            return False
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export plot:\n{str(e)}")
            return False
    
    def export_plot_pdf(self, fig, ticker):
        """Export current plot as PDF
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            Figure to export
        ticker : str
            Ticker symbol for filename
        
        Returns:
        --------
        bool : Success status
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"{ticker}_options_analysis_{timestamp}.pdf"
            
            filepath = filedialog.asksaveasfilename(
                initialdir=self.last_export_dir,
                title="Export Plot as PDF",
                defaultextension=".pdf",
                initialfile=default_name,
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if filepath:
                fig.savefig(filepath, format='pdf', bbox_inches='tight',
                           facecolor=fig.get_facecolor())
                self.last_export_dir = os.path.dirname(filepath)
                messagebox.showinfo("Export Successful", 
                                  f"Plot saved to:\n{filepath}")
                return True
            return False
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export PDF:\n{str(e)}")
            return False
    
    def export_data_csv(self, results):
        """Export analysis data as CSV
        
        Parameters:
        -----------
        results : dict
            Results dictionary with strikes, IVs, PDF data
        
        Returns:
        --------
        bool : Success status
        """
        try:
            import csv
            
            ticker = results.get('ticker', 'UNKNOWN')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"{ticker}_data_{timestamp}.csv"
            
            filepath = filedialog.asksaveasfilename(
                initialdir=self.last_export_dir,
                title="Export Data as CSV",
                defaultextension=".csv",
                initialfile=default_name,
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filepath:
                with open(filepath, 'w', newline='') as f:
                    writer = csv.writer(f)
                    
                    # Header
                    writer.writerow([f"Options Analysis Data for {ticker}"])
                    writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                    writer.writerow([])
                    
                    # IV Smile Data
                    writer.writerow(["Implied Volatility Smile"])
                    writer.writerow(["Strike", "Implied Volatility (%)"])
                    for strike, iv in zip(results['strikes'], results['IVs']):
                        writer.writerow([f"{strike:.2f}", f"{iv*100:.2f}"])
                    
                    writer.writerow([])
                    
                    # PDF Data
                    writer.writerow(["Probability Density Function"])
                    writer.writerow(["Price", "Probability Density"])
                    for price, prob in zip(results['pdf_strikes'], results['pdf_values']):
                        writer.writerow([f"{price:.2f}", f"{prob:.6f}"])
                
                self.last_export_dir = os.path.dirname(filepath)
                messagebox.showinfo("Export Successful", 
                                  f"Data saved to:\n{filepath}")
                return True
            return False
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
            return False


class ThemeSwitcher:
    """Handles theme switching and custom themes"""
    
    def __init__(self, app):
        self.app = app
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        # Toggle theme manager
        new_mode = self.app.theme.toggle_mode()
        
        # Reconfigure all styles
        self.app.style_config.configure_all()
        
        # Update root background
        self.app.root.configure(bg=self.app.theme.get_color('bg'))
        
        # Update matplotlib
        from ui_components import setup_matplotlib_style
        setup_matplotlib_style(self.app.theme)
        
        # Re-plot if results exist
        if self.app.last_results:
            self.app.plot_results(
                self.app.last_results['strikes'],
                self.app.last_results['IVs'],
                self.app.last_results['smooth_strikes'],
                self.app.last_results['fitted_IVs'],
                self.app.last_results['pdf_strikes'],
                self.app.last_results['pdf_values'],
                self.app.last_results['current_price'],
                self.app.last_results['ticker']
            )
        
        mode_name = "Light" if new_mode == "light" else "Dark"
        messagebox.showinfo("Theme Changed", f"Switched to {mode_name} mode!")
    
    def apply_custom_colors(self, color_dict):
        """Apply custom color scheme
        
        Parameters:
        -----------
        color_dict : dict
            Dictionary with color values for different elements
        """
        # Update theme colors
        for key, value in color_dict.items():
            if key in self.app.theme.current_theme:
                self.app.theme.current_theme[key] = value
        
        # Reconfigure styles
        self.app.style_config.configure_all()
        
        # Update display
        if self.app.last_results:
            self.app.plot_results(
                self.app.last_results['strikes'],
                self.app.last_results['IVs'],
                self.app.last_results['smooth_strikes'],
                self.app.last_results['fitted_IVs'],
                self.app.last_results['pdf_strikes'],
                self.app.last_results['pdf_values'],
                self.app.last_results['current_price'],
                self.app.last_results['ticker']
            )


class FontSizeController:
    """Controls application font sizes"""
    
    def __init__(self, font_manager):
        self.fonts = font_manager
        self.base_size = 10
    
    def increase_size(self):
        """Increase all font sizes"""
        self.base_size += 1
        self._update_fonts()
    
    def decrease_size(self):
        """Decrease all font sizes"""
        if self.base_size > 8:
            self.base_size -= 1
            self._update_fonts()
    
    def reset_size(self):
        """Reset to default font size"""
        self.base_size = 10
        self._update_fonts()
    
    def _update_fonts(self):
        """Update all font objects"""
        try:
            self.fonts.title_font.configure(size=self.base_size + 1)
            self.fonts.normal_font.configure(size=self.base_size)
            self.fonts.mono_font.configure(size=self.base_size - 1)
            self.fonts.button_font.configure(size=self.base_size)
        except:
            pass


class FeatureMenu:
    """Creates menu bar with extra features"""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)
        
        # Initialize managers
        self.export_manager = ExportManager()
        self.theme_switcher = ThemeSwitcher(app)
        self.font_controller = FontSizeController(app.fonts)
        
        self.create_menus()
    
    def create_menus(self):
        """Create all menu items"""
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Plot as PNG", 
                            command=self.export_png)
        file_menu.add_command(label="Export Plot as PDF", 
                            command=self.export_pdf)
        file_menu.add_command(label="Export Data as CSV", 
                            command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.app.safe_quit)
        
        # View menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark/Light Mode", 
                            command=self.theme_switcher.toggle_theme)
        view_menu.add_separator()
        view_menu.add_command(label="Increase Font Size", 
                            command=self.increase_font)
        view_menu.add_command(label="Decrease Font Size", 
                            command=self.decrease_font)
        view_menu.add_command(label="Reset Font Size", 
                            command=self.font_controller.reset_size)
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts", 
                            command=self.show_shortcuts)
    
    def export_png(self):
        """Export plot as PNG"""
        if not self.app.last_results:
            messagebox.showwarning("No Data", "Please calculate a PDF first!")
            return
        self.export_manager.export_plot_png(
            self.app.fig, 
            self.app.last_results['ticker']
        )
    
    def export_pdf(self):
        """Export plot as PDF"""
        if not self.app.last_results:
            messagebox.showwarning("No Data", "Please calculate a PDF first!")
            return
        self.export_manager.export_plot_pdf(
            self.app.fig, 
            self.app.last_results['ticker']
        )
    
    def export_csv(self):
        """Export data as CSV"""
        if not self.app.last_results:
            messagebox.showwarning("No Data", "Please calculate a PDF first!")
            return
        self.export_manager.export_data_csv(self.app.last_results)
    
    def increase_font(self):
        """Increase font size"""
        self.font_controller.increase_size()
        messagebox.showinfo("Font Size", 
                          f"Font size increased to {self.font_controller.base_size}")
    
    def decrease_font(self):
        """Decrease font size"""
        self.font_controller.decrease_size()
        messagebox.showinfo("Font Size", 
                          f"Font size decreased to {self.font_controller.base_size}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Options PDF Calculator
Version 1.0

SVI-based probability density function extraction from options markets.

Created with:
• Python
• NumPy, SciPy
• Matplotlib
• yfinance
• Anthropic Claude API

© 2024"""
        messagebox.showinfo("About", about_text)
    
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts_text = """Keyboard Shortcuts:

Enter - Calculate PDF
Ctrl+Q - Quit

File Menu:
Ctrl+E - Export PNG
Ctrl+Shift+E - Export PDF
Ctrl+D - Export Data

View Menu:
Ctrl+T - Toggle Theme
Ctrl++ - Increase Font
Ctrl+- - Decrease Font"""
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)


import tkinter as tk