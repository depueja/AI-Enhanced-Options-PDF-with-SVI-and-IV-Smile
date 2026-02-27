"""
UI Components and Styling for Options PDF Calculator
Handles all visual elements, themes, and styling
"""

import tkinter as tk
from tkinter import ttk, font

# Modern dark theme colors (GitHub Dark inspired)
DARK_THEME = {
    'bg': '#0d1117',
    'fg': '#e6edf3',
    'panel': '#161b22',
    'input': '#21262d',
    'button': '#238636',
    'button_hover': '#2ea043',
    'button_fg': '#ffffff',
    'accent': '#58a6ff',
    'success': '#3fb950',
    'error': '#f85149',
    'warning': '#d29922',
    'border': '#30363d',
}

# Light theme colors
LIGHT_THEME = {
    'bg': '#ffffff',
    'fg': '#24292f',
    'panel': '#f6f8fa',
    'input': '#ffffff',
    'button': '#2da44e',
    'button_hover': '#2c974b',
    'button_fg': '#ffffff',
    'accent': '#0969da',
    'success': '#1a7f37',
    'error': '#cf222e',
    'warning': '#9a6700',
    'border': '#d0d7de',
}

# Chart colors for dark mode
DARK_CHART_COLORS = {
    'market': '#58a6ff',
    'fit': '#f85149',
    'current': '#3fb950',
    'pdf': '#bc8cff',
    'grid': 'gray',
}

# Chart colors for light mode
LIGHT_CHART_COLORS = {
    'market': '#0969da',
    'fit': '#cf222e',
    'current': '#1a7f37',
    'pdf': '#8250df',
    'grid': '#d0d7de',
}


class ThemeManager:
    """Manages application themes"""
    
    def __init__(self, mode='dark'):
        self.mode = mode
        self.current_theme = DARK_THEME if mode == 'dark' else LIGHT_THEME
        self.chart_colors = DARK_CHART_COLORS if mode == 'dark' else LIGHT_CHART_COLORS
    
    def get_color(self, key):
        """Get a color from current theme"""
        return self.current_theme.get(key, '#000000')
    
    def get_chart_color(self, key):
        """Get a chart color from current theme"""
        return self.chart_colors.get(key, '#000000')
    
    def toggle_mode(self):
        """Switch between dark and light mode"""
        self.mode = 'light' if self.mode == 'dark' else 'dark'
        self.current_theme = DARK_THEME if self.mode == 'dark' else LIGHT_THEME
        self.chart_colors = DARK_CHART_COLORS if self.mode == 'dark' else LIGHT_CHART_COLORS
        return self.mode


class FontManager:
    """Manages application fonts"""
    
    def __init__(self):
        self.setup_fonts()
    
    def setup_fonts(self):
        """Initialize font objects"""
        try:
            # Try to use modern system fonts
            self.title_font = font.Font(family="Segoe UI", size=11, weight="bold")
            self.normal_font = font.Font(family="Segoe UI", size=12)  # Increased from 10
            self.mono_font = font.Font(family="Consolas", size=11)    # Increased from 9
            self.button_font = font.Font(family="Segoe UI", size=10, weight="bold")
        except:
            # Fallback to default fonts
            self.title_font = font.Font(size=11, weight="bold")
            self.normal_font = font.Font(size=12)  # Increased from 10
            self.mono_font = font.Font(family="Courier", size=11)  # Increased from 9
            self.button_font = font.Font(size=10, weight="bold")
    
    def get_bold_font(self):
        """Get bold version of normal font"""
        return font.Font(
            family=self.normal_font.cget("family"),
            size=self.normal_font.cget("size"),
            weight="bold"
        )


class StyleConfigurator:
    """Configures ttk styles based on theme"""
    
    def __init__(self, theme_manager, font_manager):
        self.theme = theme_manager
        self.fonts = font_manager
        self.style = ttk.Style()
        self.style.theme_use('clam')
    
    def configure_all(self):
        """Configure all widget styles"""
        self.configure_frames()
        self.configure_labels()
        self.configure_buttons()
        self.configure_entries()
        self.configure_checkbuttons()
        self.configure_labelframes()
    
    def configure_frames(self):
        """Configure frame styles"""
        self.style.configure('Card.TFrame',
                           background=self.theme.get_color('panel'),
                           relief='flat',
                           borderwidth=1)
    
    def configure_labels(self):
        """Configure label styles"""
        self.style.configure('Modern.TLabel',
                           background=self.theme.get_color('panel'),
                           foreground=self.theme.get_color('fg'),
                           font=self.fonts.normal_font)
        
        self.style.configure('Title.TLabel',
                           background=self.theme.get_color('panel'),
                           foreground=self.theme.get_color('accent'),
                           font=self.fonts.title_font)
    
    def configure_buttons(self):
        """Configure button styles"""
        self.style.configure('Modern.TButton',
                           background=self.theme.get_color('button'),
                           foreground=self.theme.get_color('button_fg'),
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 10),
                           font=self.fonts.button_font)
        
        self.style.map('Modern.TButton',
                     background=[
                         ('active', self.theme.get_color('button_hover')),
                         ('pressed', self.theme.get_color('button'))
                     ],
                     relief=[('pressed', 'flat'), ('!pressed', 'flat')])
    
    def configure_entries(self):
        """Configure entry styles"""
        self.style.configure('Modern.TEntry',
                           fieldbackground=self.theme.get_color('input'),
                           foreground=self.theme.get_color('fg'),
                           bordercolor=self.theme.get_color('border'),
                           lightcolor=self.theme.get_color('input'),
                           darkcolor=self.theme.get_color('input'),
                           insertcolor=self.theme.get_color('fg'))
    
    def configure_checkbuttons(self):
        """Configure checkbutton styles"""
        self.style.configure('Modern.TCheckbutton',
                           background=self.theme.get_color('panel'),
                           foreground=self.theme.get_color('fg'),
                           font=self.fonts.normal_font)
    
    def configure_labelframes(self):
        """Configure labelframe styles"""
        self.style.configure('Modern.TLabelframe',
                           background=self.theme.get_color('panel'),
                           foreground=self.theme.get_color('fg'),
                           bordercolor=self.theme.get_color('border'),
                           relief='solid',
                           borderwidth=1)
        
        self.style.configure('Modern.TLabelframe.Label',
                           background=self.theme.get_color('panel'),
                           foreground=self.theme.get_color('accent'),
                           font=self.fonts.title_font)


def enable_high_dpi():
    """Enable high DPI awareness on Windows"""
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass


def create_text_widget(parent, theme, fonts, is_mono=False):
    """Create a styled text widget
    
    Parameters:
    -----------
    parent : tk.Widget
        Parent widget
    theme : ThemeManager
        Theme manager instance
    fonts : FontManager
        Font manager instance
    is_mono : bool
        Whether to use monospace font
    
    Returns:
    --------
    tk.Text : Configured text widget
    """
    from tkinter import scrolledtext
    
    widget_font = fonts.mono_font if is_mono else fonts.normal_font
    
    widget = scrolledtext.ScrolledText(
        parent,
        height=8,
        width=50,
        wrap=tk.WORD,
        bg=theme.get_color('input'),
        fg=theme.get_color('fg'),
        insertbackground=theme.get_color('fg'),
        font=widget_font,
        relief='flat',
        borderwidth=0,
        highlightthickness=0
    )
    
    # Configure bold tag for non-mono widgets
    if not is_mono:
        bold_font = fonts.get_bold_font()
        widget.tag_configure("bold", font=bold_font, foreground=theme.get_color('accent'))
    
    return widget


def setup_matplotlib_style(theme):
    """Configure matplotlib to match theme
    
    Parameters:
    -----------
    theme : ThemeManager
        Theme manager instance
    """
    import matplotlib.pyplot as plt
    
    if theme.mode == 'dark':
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
    
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.facecolor'] = theme.get_color('input')
    plt.rcParams['figure.facecolor'] = theme.get_color('panel')
    plt.rcParams['text.color'] = theme.get_color('fg')
    plt.rcParams['axes.labelcolor'] = theme.get_color('fg')
    plt.rcParams['xtick.color'] = theme.get_color('fg')
    plt.rcParams['ytick.color'] = theme.get_color('fg')


def style_plot_axes(ax, theme):
    """Apply theme styling to matplotlib axes
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes to style
    theme : ThemeManager
        Theme manager instance
    """
    # Grid
    ax.grid(True, alpha=0.15, color=theme.get_chart_color('grid'), 
           linestyle='-', linewidth=0.5)
    
    # Tick colors
    ax.tick_params(colors=theme.get_color('fg'), labelsize=10)
    
    # Spine styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(theme.get_color('border'))
    ax.spines['bottom'].set_color(theme.get_color('border'))
    
    # Legend styling
    legend = ax.get_legend()
    if legend:
        legend.get_frame().set_facecolor(theme.get_color('panel'))
        legend.get_frame().set_edgecolor(theme.get_color('border'))
        legend.get_frame().set_alpha(0.9)
        for text in legend.get_texts():
            text.set_color(theme.get_color('fg'))