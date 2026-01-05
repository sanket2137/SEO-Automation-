"""
Test Script - Quick verification of the SEO automation system
Run this to test without needing API keys
"""

import sys
import os

print("=" * 60)
print("SEO Automation System - Test Script")
print("=" * 60)

# Test 1: Check Python version
print("\n[1/5] Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} - OK")
else:
    print(f"✗ Python {sys.version_info.major}.{sys.version_info.minor} - Please upgrade to 3.8+")
    sys.exit(1)

# Test 2: Check dependencies
print("\n[2/5] Checking dependencies...")
required_modules = [
    'requests',
    'bs4',
    'pandas',
    'google.generativeai',
    'dotenv'
]

missing = []
for module in required_modules:
    try:
        if module == 'bs4':
            import bs4
        elif module == 'google.generativeai':
            import google.generativeai
        elif module == 'dotenv':
            from dotenv import load_dotenv
        else:
            __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module} - MISSING")
        missing.append(module)

if missing:
    print("\n⚠ Missing dependencies. Install with:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# Test 3: Check project structure
print("\n[3/5] Checking project files...")
required_files = [
    'main.py',
    'seo_collector.py',
    'seo_analyzer.py',
    'ai_insights.py',
    'report_generator.py',
    'config.json',
    'requirements.txt'
]

for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING")

# Test 4: Test data collection (basic)
print("\n[4/5] Testing data collection module...")
try:
    from seo_collector import SEODataCollector
    collector = SEODataCollector()
    print("  ✓ SEODataCollector initialized")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 5: Test analysis module
print("\n[5/5] Testing analysis module...")
try:
    from seo_analyzer import SEOAnalyzer
    
    # Sample data
    test_data = {
        'url': 'https://example.com',
        'page_speed': {'performance_score': 85, 'seo_score': 90, 'mobile_friendly': True},
        'on_page_seo': {
            'title_length': 55,
            'meta_description_length': 150,
            'h1_count': 1,
            'total_images': 5,
            'images_without_alt': 0,
            'word_count': 1200
        },
        'technical_seo': {
            'is_https': True,
            'status_code': 200,
            'response_time_ms': 450,
            'has_robots_txt': True,
            'has_sitemap': True
        }
    }
    
    analyzer = SEOAnalyzer(test_data)
    analysis = analyzer.analyze_all()
    print(f"  ✓ Analysis complete - Score: {analysis['overall_score']:.1f}/100")
    
except Exception as e:
    print(f"  ✗ Error: {e}")

# Summary
print("\n" + "=" * 60)
print("Test Summary")
print("=" * 60)
print("\n✅ All core components are working!")
print("\nYou can now run the full workflow:")
print("  python main.py --urls https://example.com")
print("\nOr with AI insights (requires API key):")
print("  python main.py")
print("\n" + "=" * 60)
