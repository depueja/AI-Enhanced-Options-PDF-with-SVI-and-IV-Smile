"""
AI Analysis Module for Options PDF Calculator
Handles both AI-powered and rule-based analysis
"""

import numpy as np
import os

# Check if Anthropic SDK is available
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def is_ai_available():
    """Check if AI analysis is available"""
    return ANTHROPIC_AVAILABLE


def generate_ai_analysis(results):
    """
    Generate AI-powered analysis using Claude API
    
    Parameters:
    -----------
    results : dict
        Dictionary containing analysis data with keys:
        - ticker, current_price, strikes, IVs, pdf_strikes, pdf_values, tau
    
    Returns:
    --------
    str : AI-generated analysis text
    """
    if not ANTHROPIC_AVAILABLE:
        return "❌ Anthropic SDK not installed. Run: pip install anthropic"
    
    # Check for API key with detailed debugging
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        # Try to load from .env again
        load_env_file()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        # Last resort: try to read .env file directly from exe directory
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            env_path = os.path.join(exe_dir, '.env')
            
            if os.path.exists(env_path):
                try:
                    with open(env_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for line in content.split('\n'):
                            if 'ANTHROPIC_API_KEY' in line and '=' in line:
                                api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                                break
                except Exception as e:
                    pass
    
    if not api_key:
        # Provide detailed error with file location
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            env_path = os.path.join(exe_dir, '.env')
            exists = os.path.exists(env_path)
            
            error_msg = f"❌ **API Key Not Found**\n\n"
            error_msg += f"**Looking for .env in:**\n{env_path}\n\n"
            error_msg += f"**File exists:** {exists}\n\n"
            
            if exists:
                try:
                    with open(env_path, 'r') as f:
                        content = f.read()
                        error_msg += f"**File contents ({len(content)} chars):**\n{content[:200]}\n\n"
                except:
                    error_msg += "**Could not read file**\n\n"
            
            error_msg += "**Solution:**\n"
            error_msg += "1. Create a file named `.env`\n"
            error_msg += "2. Put it in the same folder as the .exe\n"
            error_msg += "3. Add this line (no quotes):\n"
            error_msg += "   ANTHROPIC_API_KEY=your-key-here\n"
            
            return error_msg
        else:
            return "❌ ANTHROPIC_API_KEY not found in .env file or environment variables."
    
    ticker = results['ticker']
    current_price = results['current_price']
    tau = results['tau']
    days_to_expiry = int(tau * 365)
    
    # Extract IV metrics
    strikes = results['strikes']
    IVs = results['IVs']
    
    atm_idx = np.argmin(np.abs(strikes - current_price))
    atm_iv = IVs[atm_idx] * 100
    
    max_iv = np.max(IVs) * 100
    min_iv = np.min(IVs) * 100
    iv_range = max_iv - min_iv
    
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
    
    # Calculate percentiles
    cumulative = np.cumsum(pdf_values) * (pdf_strikes[1] - pdf_strikes[0])
    p5_idx = np.argmin(np.abs(cumulative - 0.05))
    p95_idx = np.argmin(np.abs(cumulative - 0.95))
    
    p5_price = pdf_strikes[p5_idx]
    p95_price = pdf_strikes[p95_idx]
    
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

Keep it practical and actionable. Max 200 words.

IMPORTANT: Use **bold** markdown syntax (e.g., **key point**) to emphasize important findings, numbers, and conclusions. Make the analysis visually scannable."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        analysis = message.content[0].text
        return f"🤖 AI ANALYSIS FOR {ticker} (Powered by Claude)\n{'='*50}\n\n{analysis}"
        
    except Exception as e:
        return f"❌ AI Analysis Error: {str(e)}\n\nFalling back to basic analysis..."


def generate_basic_analysis(results):
    """
    Generate rule-based analysis without AI
    
    Parameters:
    -----------
    results : dict
        Dictionary containing analysis data
    
    Returns:
    --------
    str : Rule-based analysis text
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
    
    # Calculate percentiles
    cumulative = np.cumsum(pdf_values) * (pdf_strikes[1] - pdf_strikes[0])
    p5_idx = np.argmin(np.abs(cumulative - 0.05))
    p95_idx = np.argmin(np.abs(cumulative - 0.95))
    
    p5_price = pdf_strikes[p5_idx]
    p95_price = pdf_strikes[p95_idx]
    
    # Build analysis
    analysis = f"""📊 MARKET ANALYSIS FOR {ticker}
{'='*50}

CURRENT STATE:
• Price: ${current_price:.2f}
• Expected (PDF Peak): ${expected_price:.2f}
• Days to Expiry: {days_to_expiry}

VOLATILITY ASSESSMENT:
• ATM IV: {atm_iv:.1f}%
• Max IV: {max_iv:.1f}%
• Min IV: {min_iv:.1f}%
"""
    
    # IV level assessment
    if atm_iv > 40:
        analysis += "• Level: HIGH - Options expensive\n"
        analysis += "• Strategy: Consider selling premium\n"
    elif atm_iv > 25:
        analysis += "• Level: MODERATE - Normal range\n"
        analysis += "• Strategy: Balanced approach\n"
    else:
        analysis += "• Level: LOW - Options cheap\n"
        analysis += "• Strategy: Consider buying options\n"
    
    analysis += f"\nSKEW ANALYSIS:\n• Put IV - Call IV: {skew:+.1f}%\n"
    
    if skew > 5:
        analysis += "• Pattern: Strong downside fear\n"
        analysis += "• Interpretation: Classic equity skew\n"
        analysis += "• Note: Puts expensive, calls cheap\n"
    elif skew < -5:
        analysis += "• Pattern: Reverse skew (unusual)\n"
        analysis += "• Interpretation: Upside concerns\n"
        analysis += "• Note: Calls expensive, puts cheap\n"
    else:
        analysis += "• Pattern: Balanced smile\n"
        analysis += "• Interpretation: Symmetric risk view\n"
    
    analysis += f"\nPROBABILITY DISTRIBUTION:\n"
    analysis += f"• 5th Percentile: ${p5_price:.2f}\n"
    analysis += f"• 95th Percentile: ${p95_price:.2f}\n"
    analysis += f"• 90% Range: ${p5_price:.2f} - ${p95_price:.2f}\n"
    
    # Market bias
    if expected_price > current_price * 1.01:
        analysis += "\nMARKET BIAS: Bullish\n"
        analysis += "• PDF peak above current price\n"
    elif expected_price < current_price * 0.99:
        analysis += "\nMARKET BIAS: Bearish\n"
        analysis += "• PDF peak below current price\n"
    else:
        analysis += "\nMARKET BIAS: Neutral\n"
        analysis += "• PDF centered at current price\n"
    
    # Time considerations
    if days_to_expiry <= 7:
        analysis += "\nTIME FACTOR:\n"
        analysis += "• Near expiration - theta decay high\n"
        analysis += "• Consider 0DTE strategies carefully\n"
    elif days_to_expiry <= 30:
        analysis += "\nTIME FACTOR:\n"
        analysis += "• Monthly expiration window\n"
        analysis += "• Moderate theta decay\n"
    
    analysis += "\n\n💡 Tip: Enable AI Analysis for deeper insights!"
    
    return analysis


def analyze(results, use_ai=False):
    """
    Main analysis function - routes to AI or basic analysis
    
    Parameters:
    -----------
    results : dict
        Analysis data
    use_ai : bool
        Whether to use AI analysis
    
    Returns:
    --------
    str : Analysis text
    """
    if use_ai and ANTHROPIC_AVAILABLE:
        ai_result = generate_ai_analysis(results)
        # If AI fails, fall back to basic
        if ai_result.startswith("❌"):
            return ai_result + "\n\n" + generate_basic_analysis(results)
        return ai_result
    else:
        return generate_basic_analysis(results)