# Building .exe for Options PDF Calculator

This guide shows you how to create a standalone .exe file that you can run from a thumb drive!

---

## 🎯 What You'll Get

A single `.exe` file that:
- ✅ Runs on any Windows computer (no Python needed!)
- ✅ Works from a thumb drive
- ✅ Includes all dependencies
- ✅ Is self-contained and portable

---

## 📦 Method 1: PyInstaller (Recommended)

### **Step 1: Install PyInstaller**

```bash
python -m pip install pyinstaller
```

### **Step 2: Create Build Spec (Optional but Recommended)**

Create a file called `build_config.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['options_pdf_calculator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['anthropic', 'yfinance', 'scipy', 'numpy', 'matplotlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OptionsPDFCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Add icon='icon.ico' if you have one
)
```

### **Step 3: Build the .exe**

**Option A: Using spec file (recommended):**
```bash
pyinstaller build_config.spec
```

**Option B: Quick build (one command):**
```bash
pyinstaller --onefile --windowed --name OptionsPDFCalculator options_pdf_calculator.py
```

**Option C: With all options:**
```bash
pyinstaller ^
  --onefile ^
  --windowed ^
  --name OptionsPDFCalculator ^
  --hidden-import anthropic ^
  --hidden-import yfinance ^
  --hidden-import scipy ^
  --hidden-import numpy ^
  --hidden-import matplotlib ^
  options_pdf_calculator.py
```

### **Step 4: Find Your .exe**

The .exe will be in: `dist/OptionsPDFCalculator.exe`

### **Step 5: Test It**

```bash
cd dist
OptionsPDFCalculator.exe
```

---

## 📦 Method 2: Auto-py-to-exe (GUI Tool - Easiest!)

### **Step 1: Install**

```bash
python -m pip install auto-py-to-exe
```

### **Step 2: Run the GUI**

```bash
auto-py-to-exe
```

### **Step 3: Configure in GUI**

1. **Script Location**: Browse to `options_pdf_calculator.py`
2. **One File**: Select "One File"
3. **Console Window**: Select "Window Based (hide console)"
4. **Icon**: (Optional) Add an icon
5. **Additional Files**: 
   - Add `ui_components.py`
   - Add `features.py`
   - Add `ai_analysis.py`
6. **Hidden Imports**: Add these in "Advanced" section:
   - anthropic
   - yfinance
   - scipy
   - numpy
   - matplotlib
   - tkinter

7. Click **"CONVERT .PY TO .EXE"**

---

## 🎨 Adding an Icon (Optional)

### **Get an Icon:**
1. Create or download a `.ico` file (256x256 works best)
2. Save it as `icon.ico` in your project folder

### **Use it in PyInstaller:**
```bash
pyinstaller --onefile --windowed --icon=icon.ico --name OptionsPDFCalculator options_pdf_calculator.py
```

---

## 📋 Complete Build Script (Recommended)

Create `build.bat` (Windows):

```batch
@echo off
echo ========================================
echo Building Options PDF Calculator .exe
echo ========================================
echo.

echo Step 1: Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo Step 2: Building .exe...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name OptionsPDFCalculator ^
  --hidden-import anthropic ^
  --hidden-import yfinance ^
  --hidden-import scipy.optimize ^
  --hidden-import scipy.stats ^
  --hidden-import numpy ^
  --hidden-import matplotlib ^
  --hidden-import matplotlib.backends.backend_tkagg ^
  --add-data "ui_components.py;." ^
  --add-data "features.py;." ^
  --add-data "ai_analysis.py;." ^
  options_pdf_calculator.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your .exe is in: dist\OptionsPDFCalculator.exe
echo.
pause
```

Run it:
```bash
build.bat
```

---

## 💾 For Thumb Drive Use

### **Create Portable Package:**

1. Create a folder called `OptionsPDFCalculator-Portable`
2. Copy these files into it:
   ```
   OptionsPDFCalculator-Portable/
   ├── OptionsPDFCalculator.exe
   ├── .env (with your API key)
   └── README.txt (instructions for users)
   ```

3. Zip it up and copy to thumb drive!

### **Important for .env File:**

The .exe needs the `.env` file in the **same folder** to find your API key!

**Alternative**: Set environment variable before running:
```batch
set ANTHROPIC_API_KEY=your-key-here
OptionsPDFCalculator.exe
```

---

## 🐛 Troubleshooting

### **Problem: "Failed to execute script"**
**Solution:** Add missing hidden imports:
```bash
pyinstaller --onefile --windowed --hidden-import missing_module options_pdf_calculator.py
```

### **Problem: .exe is huge (>500MB)**
**Solution:** This is normal! It includes Python + all libraries. To reduce:
```bash
# Use --onedir instead of --onefile
pyinstaller --onedir --windowed options_pdf_calculator.py
```

### **Problem: API key not found**
**Solution:** Make sure `.env` is in the same folder as the .exe!

### **Problem: Module not found errors**
**Solution:** Add to hidden imports:
```bash
--hidden-import module_name
```

### **Problem: Antivirus flags it**
**Solution:** This is common with PyInstaller. You can:
- Add exception in antivirus
- Code-sign the .exe (requires certificate)
- Use `--debug=all` to see what's happening

---

## 📊 Build Size Estimates

| Build Type | Size | Pros | Cons |
|------------|------|------|------|
| **One File** | ~150-250 MB | Single .exe | Slower startup |
| **One Dir** | ~200-300 MB | Faster startup | Multiple files |

---

## ✅ Final Checklist

Before distributing:

- [ ] Test .exe on clean computer (without Python)
- [ ] Include `.env` file (or instructions to create it)
- [ ] Test all features (AI, export, theme toggle)
- [ ] Create README with instructions
- [ ] Test from thumb drive
- [ ] Verify keyboard shortcuts work

---

## 🚀 Quick Start Commands

**Simplest build (for testing):**
```bash
python -m pip install pyinstaller
pyinstaller --onefile --windowed options_pdf_calculator.py
```

**Production build (recommended):**
```bash
pyinstaller --onefile --windowed --name OptionsPDFCalculator --hidden-import anthropic --hidden-import yfinance options_pdf_calculator.py
```

**Find your .exe:**
```bash
cd dist
dir OptionsPDFCalculator.exe
```

---

## 📝 User Instructions (Include in Package)

Create `README.txt`:

```
Options PDF Calculator - Portable Edition

REQUIREMENTS:
- Windows 7 or later
- Internet connection (for fetching options data)

SETUP:
1. Copy this folder to your computer or thumb drive
2. Create a file called ".env" in the same folder
3. Add this line to .env:
   ANTHROPIC_API_KEY=your-api-key-here
4. Double-click OptionsPDFCalculator.exe

USAGE:
1. Enter a ticker symbol (e.g., SPY, AAPL)
2. Check "AI Analysis" if you want AI insights
3. Click "Calculate PDF"
4. Use File menu to export results

KEYBOARD SHORTCUTS:
- Ctrl+E: Export PNG
- Ctrl+T: Toggle theme
- Ctrl+Plus: Increase font
- Ctrl+Q: Quit

For support, visit: [your contact info]
```

---

## 🎉 You're Done!

Your portable Options PDF Calculator is ready to share!

**Distribution package:**
```
OptionsPDFCalculator-Portable.zip
├── OptionsPDFCalculator.exe
├── .env.example (template)
└── README.txt
```