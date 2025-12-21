"""
AI Analyzer Module for Options PDF Calculator
Uses Claude API to provide intelligent analysis of options data
"""

import numpy as np


def analyze_results(results):
    """
    Analyze options PDF results using Claude AI
    
    Parameters:
    -----------
    results : dict
        Dictionary containing:
        - ticker: str
        - current_price: float
        - strikes: array
        - IVs: array
        - fitted_IVs: array
        - pdf_strikes: array
        - pdf_values: array
        - tau: float (time to expiration in years)
        - expiry: str
        - optimal_params: array (SVI parameters)
    
    Returns:
    --------
    str : AI-generated analysis
    """
    
    try:
        # Extract key metrics for analysis
        ticker = results['ticker']
        current_price = results['current_price']
        tau = results['tau']
        days_to_expiry = int(tau * 365)
        
        # IV smile analysis
        strikes = results['strikes']
        IVs = results['IVs']
        
        # Find ATM IV
        atm_idx = np.argmin(np.abs(strikes - current_price))
        atm_iv = IVs[atm_idx] * 100
        
        # Find max and min IV
        max_iv = np.max(IVs) * 100
        min_iv = np.min(IVs) * 100
        iv_range = max_iv - min_iv
        
        # Analyze skew
        otm_put_ivs = IVs[strikes < current_price * 0.95]
        otm_call_ivs = IVs[strikes > current_price * 1.05]
        
        if len(otm_put_ivs) > 0 and len(otm_call_ivs) > 0:
            put_avg_iv = np.mean(otm_put_ivs) * 100
            call_avg_iv = np.mean(otm_call_ivs) * 100
            skew = put_avg_iv - call_avg_iv
        else:
            skew = 0
        
        # PDF analysis
        pdf_strikes = results['pdf_strikes']
        pdf_values = results['pdf_values']
        
        # Find peak
        peak_idx = np.argmax(pdf_values)
        expected_price = pdf_strikes[peak_idx]
        
        # Calculate percentiles
        cumulative = np.cumsum(pdf_values) * (pdf_strikes[1] - pdf_strikes[0])
        p5_idx = np.argmin(np.abs(cumulative - 0.05))
        p95_idx = np.argmin(np.abs(cumulative - 0.95))
        
        p5_price = pdf_strikes[p5_idx]
        p95_price = pdf_strikes[p95_idx]
        
        # Expected move
        expected_move_pct = abs(expected_price - current_price) / current_price * 100
        range_90_pct = (p95_price - p5_price) / current_price * 100
        
        # Build prompt for Claude
        prompt = f"""Analyze these options market data for {ticker}:

CURRENT STATE:
- Current Price: ${current_price:.2f}
- Days to Expiration: {days_to_expiry}

IMPLIED VOLATILITY SMILE:
- ATM IV: {atm_iv:.1f}%
- Max IV: {max_iv:.1f}%
- Min IV: {min_iv:.1f}%
- IV Range: {iv_range:.1f}%
- Skew (Put IV - Call IV): {skew:.1f}%

PROBABILITY DISTRIBUTION:
- Expected Price (PDF peak): ${expected_price:.2f}
- 5th Percentile: ${p5_price:.2f}
- 95th Percentile: ${p95_price:.2f}
- Expected Move: {expected_move_pct:.2f}%
- 90% Confidence Range: ±{range_90_pct/2:.2f}%

Provide a concise analysis covering:
1. What the volatility smile shape tells us about market sentiment
2. Key risks or opportunities revealed by the PDF
3. Trading implications (bullish/bearish/neutral)
4. Any notable patterns or anomalies

Keep it practical and actionable. Max 200 words."""

        # Call Claude API
        import anthropic
        
        client = anthropic.Anthropic()
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract response
        analysis = message.content[0].text
        
        return f"🤖 AI ANALYSIS FOR {ticker}\n" + "="*50 + "\n\n" + analysis
        
    except ImportError:
        return """AI Analysis requires the Anthropic SDK.

To install:
    pip install anthropic

Then set your API key as an environment variable:
    
    Windows (Command Prompt):
    set ANTHROPIC_API_KEY=your_key_here
    
    Windows (PowerShell):
    $env:ANTHROPIC_API_KEY="your_key_here"
    
    Mac/Linux:
    export ANTHROPIC_API_KEY=your_key_here

Get your API key at: https://console.anthropic.com/"""
        
    except Exception as e:
        return f"""AI Analysis Error: {str(e)}

Please check:
1. Anthropic SDK is installed (pip install anthropic)
2. API key is set correctly
3. You have API credits available

Error details: {type(e).__name__}"""


def analyze_results_fallback(results):
    """
    Fallback analysis without AI - basic rule-based analysis
    """
    
    ticker = results['ticker']
    current_price = results['current_price']
    tau = results['tau']
    days_to_expiry = int(tau * 365)
    
    # Extract metrics
    strikes = results['strikes']
    IVs = results['IVs']
    
    atm_idx = np.argmin(np.abs(strikes - current_price))
    atm_iv = IVs[atm_idx] * 100
    
    max_iv = np.max(IVs) * 100
    min_iv = np.min(IVs) * 100
    
    # Skew analysis
    otm_put_ivs = IVs[strikes < current_price * 0.95]
    otm_call_ivs = IVs[strikes > current_price * 1.05]
    
    if len(otm_put_ivs) > 0 and len(otm_call_ivs) > 0:
        put_avg_iv = np.mean(otm_put_ivs) * 100
        call_avg_iv = np.mean(otm_call_ivs) * 100
        skew = put_avg_iv - call_avg_iv
    else:
        skew = 0
    
    # PDF metrics
    pdf_strikes = results['pdf_strikes']
    pdf_values = results['pdf_values']
    
    peak_idx = np.argmax(pdf_values)
    expected_price = pdf_strikes[peak_idx]
    
    # Build basic analysis
    analysis = f"""📊 BASIC ANALYSIS FOR {ticker}
{"="*50}

Market Setup:
• Current: ${current_price:.2f}
• Expected: ${expected_price:.2f}
• Time: {days_to_expiry} days

Volatility Assessment:
• ATM IV: {atm_iv:.1f}%
"""
    
    if atm_iv > 40:
        analysis += "• Level: HIGH - Options expensive\n"
    elif atm_iv > 25:
        analysis += "• Level: MODERATE - Normal range\n"
    else:
        analysis += "• Level: LOW - Options cheap\n"
    
    analysis += f"\nSkew Analysis (Put IV - Call IV): {skew:.1f}%\n"
    
    if skew > 5:
        analysis += "• Strong downside fear (classic equity skew)\n"
        analysis += "• Put protection expensive\n"
    elif skew < -5:
        analysis += "• Unusual upside fear (reverse skew)\n"
        analysis += "• Call premium elevated\n"
    else:
        analysis += "• Balanced volatility smile\n"
    
    analysis += "\nImplications:\n"
    
    if expected_price > current_price * 1.01:
        analysis += "• Slight bullish bias in PDF\n"
    elif expected_price < current_price * 0.99:
        analysis += "• Slight bearish bias in PDF\n"
    else:
        analysis += "• Neutral expected move\n"
    
    if days_to_expiry <= 7:
        analysis += "• Near expiration - theta decay accelerating\n"
    
    analysis += "\n💡 Note: Install Anthropic SDK for AI-powered analysis"
    
    return analysis
