================================================================================

&nbsp;                   OPTIONS PDF CALCULATOR

&nbsp;         Options-Derived Probability Density Functions

&nbsp;                     Version 1.0

================================================================================



TABLE OF CONTENTS

-----------------

1\. Overview

2\. What This App Does

3\. System Requirements

4\. Installation \& Setup

5\. How to Use

6\. Understanding the Results

7\. Features

8\. Keyboard Shortcuts

9\. Troubleshooting

10\. Technical Details

11\. Credits \& License



================================================================================

1\. OVERVIEW

================================================================================



Options PDF Calculator extracts probability density functions (PDFs) from 

options market data using the SVI (Stochastic Volatility Inspired) model and 

the Breeden-Litzenberger formula.



This tool helps traders and analysts understand:

&nbsp; • What the options market expects for future price movements

&nbsp; • Implied volatility structure (smile/skew)

&nbsp; • Probability distributions of future stock prices

&nbsp; • Market sentiment and risk assessment



================================================================================

2\. WHAT THIS APP DOES

================================================================================



INPUT:

&nbsp; • Any stock ticker with listed options (e.g., SPY, AAPL, TSLA)



PROCESS:

&nbsp; 1. Fetches real-time options data from Yahoo Finance

&nbsp; 2. Calculates implied volatility for each strike price

&nbsp; 3. Fits an SVI model to the volatility smile using optimization

&nbsp; 4. Extracts the risk-neutral probability density function

&nbsp; 5. (Optional) Generates AI-powered analysis of the results



OUTPUT:

&nbsp; • Implied Volatility Smile chart (market data + fitted curve)

&nbsp; • Probability Density Function chart

&nbsp; • Optimization details (convergence, parameters, error metrics)

&nbsp; • Market analysis (sentiment, risks, trading implications)



================================================================================

3\. SYSTEM REQUIREMENTS

================================================================================



REQUIRED:

&nbsp; • Windows 7 or later (64-bit)

&nbsp; • Internet connection (for fetching options data)

&nbsp; • 200 MB free disk space

&nbsp; • 2 GB RAM minimum



OPTIONAL:

&nbsp; • Anthropic API key (for AI-powered analysis)

&nbsp; • 1920x1080 or higher resolution (for best experience)



NO PYTHON INSTALLATION NEEDED!

This is a standalone executable - works on any Windows PC.



================================================================================

4\. INSTALLATION \& SETUP

================================================================================



BASIC SETUP (Without AI):

--------------------------

1\. Copy the "OptionsPDFCalculator" folder to your desired location

&nbsp;  (Desktop, USB drive, hard drive, etc.)



2\. Double-click "OptionsPDFCalculator.exe"



3\. That's it! The app will run without AI analysis.





FULL SETUP (With AI Analysis):

-------------------------------

1\. Get an Anthropic API key:

&nbsp;  • Go to: https://console.anthropic.com/

&nbsp;  • Sign up for an account

&nbsp;  • Navigate to Settings → API Keys

&nbsp;  • Click "Create Key"

&nbsp;  • Copy the key (starts with "sk-ant-")



2\. Edit the "run.bat" file:

&nbsp;  • Right-click "run.bat" → Edit

&nbsp;  • Replace "your-key-here" with your actual API key

&nbsp;  • Save and close



3\. Double-click "run.bat" (NOT the .exe directly)



4\. AI Analysis will now be available!





IMPORTANT NOTES:

----------------

• If using AI: Always run via "run.bat", not the .exe directly

• Keep "run.bat" private - it contains your API key

• Don't share your API key with others

• AI analysis costs ~$0.01-0.05 per calculation



================================================================================

5\. HOW TO USE

================================================================================



BASIC USAGE:

------------

1\. Launch the app:

&nbsp;  • Without AI: Double-click "OptionsPDFCalculator.exe"

&nbsp;  • With AI: Double-click "run.bat"



2\. Enter a ticker symbol:

&nbsp;  • Type in the "Ticker Symbol" field (e.g., SPY, AAPL, TSLA)

&nbsp;  • Press Enter or click "Calculate PDF"



3\. Wait for calculation:

&nbsp;  • Fetching options data (2-5 seconds)

&nbsp;  • Calculating implied volatilities

&nbsp;  • Running SVI optimization

&nbsp;  • Extracting probability density function

&nbsp;  • Total time: 5-15 seconds



4\. View results:

&nbsp;  • Top chart: Implied Volatility Smile

&nbsp;  • Bottom chart: Probability Density Function

&nbsp;  • Left panel: Optimization details and analysis





ENABLING AI ANALYSIS:

---------------------

1\. Make sure you ran via "run.bat" (with API key set)

2\. Check the box "AI Analysis (✓ Ready)"

3\. Calculate as normal

4\. AI-generated insights appear in "Market Analysis" section





EXPORTING RESULTS:

------------------

• File → Export Plot as PNG (high-quality image)

• File → Export Plot as PDF (publication-ready)

• File → Export Data as CSV (raw data for Excel)





SWITCHING THEMES:

-----------------

• View → Toggle Dark/Light Mode

• Or press Ctrl+T

• Changes apply immediately



================================================================================

6\. UNDERSTANDING THE RESULTS

================================================================================



TOP CHART: IMPLIED VOLATILITY SMILE

------------------------------------

• X-axis: Strike prices (the exercise price of options)

• Y-axis: Implied volatility (market's expected volatility %)

• Blue dots: Actual market implied volatilities

• Red line: SVI model fit (smoothed curve)

• Green dashed line: Current stock price



WHAT TO LOOK FOR:



Volatility Skew (most common in equities):

&nbsp; • Higher IV on left (OTM puts) = Downside fear

&nbsp; • Lower IV on right (OTM calls) = Less upside concern

&nbsp; • Indicates market pricing in crash risk



Volatility Smile (U-shaped):

&nbsp; • High IV on both sides

&nbsp; • Market uncertain about direction

&nbsp; • Common before earnings, major events



Flat Smile:

&nbsp; • Similar IV across all strikes

&nbsp; • Balanced risk perception

&nbsp; • Rare in real markets





BOTTOM CHART: PROBABILITY DENSITY FUNCTION

-------------------------------------------

• X-axis: Possible future stock prices

• Y-axis: Probability density (higher = more likely)

• Purple area: Risk-neutral probability distribution

• Green dashed line: Current stock price



WHAT TO LOOK FOR:



Peak Location:

&nbsp; • Peak at current price = Market expects no drift

&nbsp; • Peak above current = Bullish expectation

&nbsp; • Peak below current = Bearish expectation



Width:

&nbsp; • Narrow distribution = Low volatility, high certainty

&nbsp; • Wide distribution = High volatility, uncertain outcome



Tails:

&nbsp; • Fat left tail = Higher crash probability

&nbsp; • Fat right tail = Higher moonshot probability

&nbsp; • Symmetric = Balanced risk



Skewness:

&nbsp; • Left-skewed = More downside risk

&nbsp; • Right-skewed = More upside potential





OPTIMIZATION DETAILS:

---------------------

Shows the technical process:

&nbsp; • Initial parameter guesses

&nbsp; • Optimization algorithm (L-BFGS-B)

&nbsp; • Convergence status (should be "True")

&nbsp; • Number of iterations

&nbsp; • Final error (lower is better)

&nbsp; • Optimal SVI parameters



Good optimization:

&nbsp; • Converged: True ✓

&nbsp; • Error (SSE): < 0.001

&nbsp; • Iterations: 3-20





MARKET ANALYSIS:

----------------

Provides interpretation:

&nbsp; • Current state (price, expiration)

&nbsp; • Volatility assessment (high/moderate/low)

&nbsp; • Strategy suggestions (buy/sell premium)

&nbsp; • Skew analysis (market fear indicators)

&nbsp; • Probability ranges (5th-95th percentile)

&nbsp; • Market bias (bullish/bearish/neutral)

&nbsp; • Time considerations (theta decay warnings)



With AI enabled:

&nbsp; • Natural language insights

&nbsp; • Pattern recognition

&nbsp; • Anomaly detection

&nbsp; • Context-aware recommendations



================================================================================

7\. FEATURES

================================================================================



CORE FEATURES:

--------------

✓ Real-time options data from Yahoo Finance

✓ Automatic implied volatility calculation (Newton-Raphson)

✓ SVI model optimization (L-BFGS-B algorithm)

✓ Breeden-Litzenberger PDF extraction

✓ Professional-quality visualizations

✓ Detailed optimization logging



ADVANCED FEATURES:

------------------

✓ AI-powered market analysis (Claude Sonnet 4)

✓ Export to PNG (300 DPI, publication-ready)

✓ Export to PDF (vector graphics)

✓ Export data to CSV (for further analysis)

✓ Dark/Light theme toggle

✓ Adjustable font sizes (zoom in/out)

✓ Resizable panels (drag to adjust)

✓ Keyboard shortcuts



UI FEATURES:

------------

✓ Modern dark theme (GitHub-inspired)

✓ High-DPI support (crystal clear on 4K displays)

✓ Professional fonts (Segoe UI, Consolas)

✓ Color-coded status indicators

✓ Bold text in AI analysis for key findings

✓ Responsive interface



PORTABILITY:

------------

✓ Runs from USB drive

✓ No installation required

✓ No Python needed

✓ Works on any Windows PC

✓ Self-contained executable



================================================================================

8\. KEYBOARD SHORTCUTS

================================================================================



GENERAL:

--------

Enter           Calculate PDF (when in ticker field)

Ctrl+Q          Quit application



FILE OPERATIONS:

----------------

Ctrl+E          Export plot as PNG

Ctrl+Shift+E    Export plot as PDF

Ctrl+D          Export data as CSV



VIEW OPTIONS:

-------------

Ctrl+T          Toggle dark/light theme

Ctrl+Plus       Increase font size

Ctrl+=          Increase font size (no shift needed)

Ctrl+Minus      Decrease font size

Ctrl+0          Reset font size to default



================================================================================

9\. TROUBLESHOOTING

================================================================================



PROBLEM: "Ticker not found"

SOLUTION: 

&nbsp; • Check spelling (must be uppercase, e.g., "SPY" not "spy")

&nbsp; • Verify ticker has listed options (not all stocks do)

&nbsp; • Try a common ticker first (SPY, AAPL, MSFT)



PROBLEM: "No options data available"

SOLUTION:

&nbsp; • Stock may not have options

&nbsp; • Try more liquid stocks (SPY, QQQ, AAPL)

&nbsp; • Check if market is open (some data updates during trading hours)



PROBLEM: "Insufficient liquid options"

SOLUTION:

&nbsp; • Choose a different expiration (app uses nearest)

&nbsp; • Try more popular/liquid stocks

&nbsp; • Ensure market is open



PROBLEM: "Could not resolve host" or network errors

SOLUTION:

&nbsp; • Check internet connection

&nbsp; • Verify Yahoo Finance is accessible (open in browser)

&nbsp; • Check firewall settings (may be blocking the .exe)

&nbsp; • Add .exe to antivirus exceptions

&nbsp; • Try different network (e.g., phone hotspot)



PROBLEM: AI Analysis says "API Key Not Found"

SOLUTION:

&nbsp; • Make sure you ran "run.bat" (NOT the .exe directly)

&nbsp; • Open "run.bat" in Notepad and verify API key is correct

&nbsp; • Check for extra spaces or quotes around the key

&nbsp; • Key should start with "sk-ant-"

&nbsp; • Restart the app via "run.bat"



PROBLEM: AI Analysis fails with error

SOLUTION:

&nbsp; • Verify you have API credits at console.anthropic.com

&nbsp; • Check your API key is valid

&nbsp; • Try unchecking AI Analysis (basic analysis still works)



PROBLEM: App looks blurry/pixelated

SOLUTION:

&nbsp; • Right-click .exe → Properties → Compatibility

&nbsp; • Check "Override high DPI scaling behavior"

&nbsp; • Select "Application"

&nbsp; • Click OK and restart



PROBLEM: Antivirus flags the .exe as suspicious

SOLUTION:

&nbsp; • This is common with PyInstaller executables

&nbsp; • Add exception in your antivirus

&nbsp; • The app is safe - it's just packaged Python code



PROBLEM: Export features don't work

SOLUTION:

&nbsp; • Make sure you have write permissions in the export folder

&nbsp; • Try exporting to Desktop or Documents

&nbsp; • Check available disk space



================================================================================

10\. TECHNICAL DETAILS

================================================================================



METHODOLOGY:

------------

1\. OPTIONS DATA COLLECTION

&nbsp;  • Source: Yahoo Finance (yfinance library)

&nbsp;  • Uses nearest expiration date

&nbsp;  • Filters for liquid options (volume > 0)



2\. IMPLIED VOLATILITY CALCULATION

&nbsp;  • Method: Newton-Raphson iteration

&nbsp;  • Model: Black-Scholes formula

&nbsp;  • Tolerance: 1e-6

&nbsp;  • Max iterations: 100

&nbsp;  • Validates: 5% < IV < 200%



3\. SVI MODEL FITTING

&nbsp;  • Model: w(k) = a + b\[ρ(k-m) + √((k-m)² + σ²)]

&nbsp;  • Parameters: a, b, ρ, m, σ

&nbsp;  • Optimizer: L-BFGS-B (scipy.optimize.minimize)

&nbsp;  • Constraints: a≥0, b≥0, -1≤ρ≤1, σ>0

&nbsp;  • Prevents arbitrage violations



4\. PDF EXTRACTION

&nbsp;  • Method: Breeden-Litzenberger formula

&nbsp;  • Formula: p(K) = e^(rT) × ∂²C/∂K²

&nbsp;  • Implementation: Finite differences

&nbsp;  • Normalization: ∫p(K)dK = 1



5\. AI ANALYSIS (Optional)

&nbsp;  • Model: Claude Sonnet 4 (Anthropic)

&nbsp;  • Analyzes: Smile shape, PDF characteristics, market sentiment

&nbsp;  • Outputs: Natural language insights with bold emphasis





BUILT WITH:

-----------

• Python 3.14

• NumPy (numerical computations)

• SciPy (optimization algorithms)

• Matplotlib (visualizations)

• yfinance (options data)

• Tkinter (user interface)

• Anthropic SDK (AI analysis)

• PyInstaller (executable packaging)





ALGORITHMS:

-----------

• Black-Scholes option pricing

• Newton-Raphson root finding

• L-BFGS-B constrained optimization

• Cubic spline interpolation

• Numerical differentiation (finite differences)

• Trapezoidal integration





DATA SOURCES:

-------------

• Options data: Yahoo Finance API (free)

• Risk-free rate: Fixed at 5% (approximate)

• AI analysis: Anthropic Claude API (paid)





LIMITATIONS:

------------

• Uses nearest expiration only (future versions may support multiple)

• Assumes constant risk-free rate

• Requires active internet connection

• Yahoo Finance data can be delayed

• SVI model may not fit all smile shapes perfectly

• AI analysis requires API credits



================================================================================

11\. CREDITS \& LICENSE

================================================================================



CREATED BY:

-----------

Jade Parsons

December 2024



POWERED BY:

-----------

• Python (programming language)

• NumPy \& SciPy (scientific computing)

• Matplotlib (visualization)

• yfinance (financial data)

• Anthropic Claude (AI analysis)

• PyInstaller (executable packaging)



ACKNOWLEDGMENTS:

----------------

• Breeden \& Litzenberger (1978) - PDF extraction method

• Gatheral \& Jacquier (2014) - SVI model

• Anthropic - Claude AI API



LICENSE:

--------

This software is provided "as is" for personal and educational use.



DISCLAIMER:

-----------

This tool is for educational and informational purposes only.

NOT financial advice. NOT suitable for actual trading decisions.



Options trading involves substantial risk of loss.

Past performance does not guarantee future results.

Always consult with a qualified financial advisor.



The creators are not responsible for trading losses, data accuracy,

or any damages resulting from use of this software.



USE AT YOUR OWN RISK.



================================================================================



GETTING HELP:

-------------

If you encounter issues:

&nbsp; 1. Check the Troubleshooting section above

&nbsp; 2. Verify your internet connection

&nbsp; 3. Try with a different ticker (SPY always works)

&nbsp; 4. Check Help → Keyboard Shortcuts in the app menu



FEEDBACK:

---------

Found a bug? Have a suggestion?

Your feedback helps improve this tool!



================================================================================



HAPPY ANALYZING! 📊📈💰



Version 1.0 - December 2024



================================================================================

