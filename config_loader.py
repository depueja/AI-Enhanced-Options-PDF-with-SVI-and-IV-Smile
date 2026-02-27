"""
Simple configuration loader that works in frozen executables
"""
import os
import sys


def get_api_key():
    """
    Get API key from multiple sources in order of priority:
    1. Environment variable
    2. .env file in exe/script directory
    3. config.txt file in exe/script directory
    """
    
    # Method 1: Check environment variable first
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        return api_key
    
    # Get the directory where the exe/script is located
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        app_dir = os.path.dirname(sys.executable)
    else:
        # Running as Python script
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Method 2: Try to read .env file
    env_file = os.path.join(app_dir, '.env')
    api_key = read_key_from_file(env_file)
    if api_key:
        return api_key
    
    # Method 3: Try to read config.txt file (alternative)
    config_file = os.path.join(app_dir, 'config.txt')
    api_key = read_key_from_file(config_file)
    if api_key:
        return api_key
    
    return None


def read_key_from_file(filepath):
    """Read API key from a file"""
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Look for ANTHROPIC_API_KEY
                if 'ANTHROPIC_API_KEY' in line:
                    if '=' in line:
                        # Format: ANTHROPIC_API_KEY=sk-ant-...
                        key = line.split('=', 1)[1].strip()
                    else:
                        # Format: just the key on its own line
                        key = line.replace('ANTHROPIC_API_KEY', '').strip()
                    
                    # Remove quotes if present
                    key = key.strip('"').strip("'")
                    
                    # Validate it looks like a real key
                    if key and key.startswith('sk-ant-'):
                        return key
                
                # If line starts with sk-ant-, assume it's the key
                if line.startswith('sk-ant-'):
                    return line
    
    except Exception:
        pass
    
    return None


def set_api_key(api_key):
    """Set the API key in environment"""
    if api_key:
        os.environ['ANTHROPIC_API_KEY'] = api_key


# Auto-load on import
_api_key = get_api_key()
if _api_key:
    set_api_key(_api_key)
