# Quick Setup Guide

Follow these steps to get started with the SEO Automation Workflow in under 5 minutes.

## Step 1: Install Dependencies (1 minute)

Open PowerShell/Command Prompt in the Task folder and run:

```powershell
pip install -r requirements.txt
```

Expected output:
```
Successfully installed requests beautifulsoup4 pandas google-generativeai python-dotenv matplotlib lxml
```

## Step 2: Get Your Gemini API Key (2 minutes)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

## Step 3: Configure API Key (1 minute)

### Option A: Using .env file (Recommended)

Create a file named `.env` in the Task folder:

```
GEMINI_API_KEY=paste_your_key_here
```

### Option B: Using environment variable

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="paste_your_key_here"
```

**Windows CMD:**
```cmd
set GEMINI_API_KEY=paste_your_key_here
```

## Step 4: Configure URLs (30 seconds)

Edit `config.json` and replace with your target URLs:

```json
{
  "target_urls": [
    "https://your-website.com",
    "https://example.com"
  ]
}
```

## Step 5: Run the Analysis (1 minute)

```powershell
python main.py
```

That's it! The system will:
1. ✓ Collect SEO data from your URLs
2. ✓ Analyze performance, technical, and on-page SEO
3. ✓ Generate AI insights with Gemini
4. ✓ Create reports in the `reports/` folder

## Viewing Your Reports

### Markdown Report
Open `reports/seo_report_*.md` in VS Code or any text editor

### HTML Report
Double-click `reports/seo_report_*.html` to open in your browser

### JSON Report
Use for integrations: `reports/seo_report_*.json`

## Quick Test (Without API Key)

To test without configuring Gemini:

```powershell
python main.py --skip-ai
```

This will generate reports without AI insights (still useful!).

## Common Issues

### Issue: "pip not recognized"
**Solution:** Ensure Python is in PATH. Try: `python -m pip install -r requirements.txt`

### Issue: "GEMINI_API_KEY not found"
**Solution:** Create `.env` file or use `--skip-ai` flag

### Issue: "PageSpeed API timeout"
**Solution:** Wait a moment and try again. The API has rate limits.

## Next Steps

1. ✓ Review generated reports in `reports/` folder
2. ✓ Implement recommended fixes from AI insights
3. ✓ Schedule regular scans (see README for automation)
4. ✓ Track improvements over time

## Need Help?

Refer to the comprehensive [README.md](README.md) for:
- Detailed documentation
- Advanced usage
- Automation setup
- Troubleshooting guide

---

**Time to first report: ~5 minutes** ⚡
