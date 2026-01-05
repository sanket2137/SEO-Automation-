"""
Main SEO Automation Workflow
Orchestrates the entire SEO automation process:
1. Data Collection
2. Analysis
3. AI Insights Generation
4. Report Creation
"""

import json
import os
import sys
from datetime import datetime
from typing import List
import argparse

from seo_collector import collect_seo_data, SEODataCollector
from seo_analyzer import SEOAnalyzer
from ai_insights import GeminiInsightsGenerator
from report_generator import ReportGenerator


class SEOAutomation:
    """Main automation orchestrator"""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize with configuration"""
        self.load_config(config_file)
        self.results = {}
        
        # Create necessary directories
        os.makedirs(self.config.get('data_directory', 'data'), exist_ok=True)
        os.makedirs(self.config.get('output_directory', 'reports'), exist_ok=True)
    
    def load_config(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
            print(f"✓ Configuration loaded from {config_file}")
        except FileNotFoundError:
            print(f"⚠ Config file not found. Using defaults.")
            self.config = {
                "target_urls": [],
                "output_directory": "reports",
                "data_directory": "data"
            }
    
    def run(self, urls: List[str] = None, skip_ai: bool = False):
        """Run the complete SEO automation workflow"""
        
        print("\n" + "="*60)
        print("🚀 AI-POWERED SEO AUTOMATION WORKFLOW")
        print("="*60)
        
        # Use URLs from parameter or config
        target_urls = urls or self.config.get('target_urls', [])
        
        if not target_urls:
            print("❌ Error: No URLs provided")
            print("   Either specify URLs via command line or add them to config.json")
            return
        
        print(f"\n📋 Analyzing {len(target_urls)} URL(s):")
        for url in target_urls:
            print(f"   • {url}")
        
        # Step 1: Collect SEO Data
        print("\n" + "-"*60)
        print("STEP 1: Data Collection")
        print("-"*60)
        
        data_dir = self.config.get('data_directory', 'data')
        collected_data = collect_seo_data(target_urls, data_dir)
        
        if not collected_data:
            print("❌ Failed to collect data")
            return
        
        print(f"✅ Data collection complete for {len(collected_data)} URL(s)")
        
        # Step 2: Analyze SEO Data
        print("\n" + "-"*60)
        print("STEP 2: SEO Analysis")
        print("-"*60)
        
        analyses = []
        for data in collected_data:
            if 'error' not in data:
                analyzer = SEOAnalyzer(data)
                analysis = analyzer.analyze_all()
                analyses.append(analysis)
                print(f"\n{analysis.get('summary', '')}")
        
        print(f"\n✅ Analysis complete for {len(analyses)} URL(s)")
        
        # Save analysis results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        analysis_file = os.path.join(data_dir, f'analysis_{timestamp}.json')
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analyses, f, indent=2, ensure_ascii=False)
        print(f"💾 Analysis saved to: {analysis_file}")
        
        # Step 3: Generate AI Insights
        ai_insights_list = []
        
        if not skip_ai:
            print("\n" + "-"*60)
            print("STEP 3: AI Insights Generation")
            print("-"*60)
            
            try:
                # Check for API key
                api_key = os.getenv('GEMINI_API_KEY') or self.config.get('gemini_api_key')
                
                if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
                    print("⚠ Gemini API key not configured")
                    print("  Skipping AI insights generation")
                    print("  To enable: Set GEMINI_API_KEY environment variable")
                    skip_ai = True
                else:
                    generator = GeminiInsightsGenerator(api_key)
                    
                    for analysis in analyses:
                        insights = generator.generate_insights(analysis)
                        ai_insights_list.append(insights)
                    
                    # If multiple URLs, generate comparison
                    if len(analyses) > 1:
                        comparison = generator.generate_comparison_insights(analyses)
                        print("\n📊 Comparative Analysis:")
                        print(comparison)
                    
                    print(f"\n✅ AI insights generated for {len(ai_insights_list)} URL(s)")
                    
            except Exception as e:
                print(f"⚠ AI insights generation failed: {str(e)}")
                print("  Continuing with basic insights...")
                skip_ai = True
        
        # Step 4: Generate Reports
        print("\n" + "-"*60)
        print("STEP 4: Report Generation")
        print("-"*60)
        
        report_dir = self.config.get('output_directory', 'reports')
        generator = ReportGenerator(report_dir)
        
        generated_reports = []
        
        for i, analysis in enumerate(analyses):
            # Get corresponding AI insights if available
            ai_insights = ai_insights_list[i] if i < len(ai_insights_list) else {
                'ai_insights': 'AI insights not available. Run with Gemini API key configured.'
            }
            
            # Generate domain-safe filename
            from urllib.parse import urlparse
            domain = urlparse(analysis.get('url')).netloc.replace('.', '_')
            base_filename = f"seo_report_{domain}_{timestamp}"
            
            # Generate Markdown report
            md_content = generator.generate_full_report(analysis, ai_insights, format="markdown")
            md_file = generator.save_report(md_content, base_filename, format="markdown")
            generated_reports.append(md_file)
            
            # Generate HTML report
            html_content = generator.generate_full_report(analysis, ai_insights, format="html")
            html_file = generator.save_report(html_content, base_filename, format="html")
            generated_reports.append(html_file)
            
            # Generate JSON report
            json_content = generator.generate_full_report(analysis, ai_insights, format="json")
            json_file = generator.save_report(json_content, base_filename, format="json")
            generated_reports.append(json_file)
        
        print(f"\n✅ Generated {len(generated_reports)} report files")
        
        # Final Summary
        print("\n" + "="*60)
        print("✅ WORKFLOW COMPLETE!")
        print("="*60)
        
        print("\n📊 Summary:")
        print(f"   URLs Analyzed: {len(analyses)}")
        print(f"   Reports Generated: {len(generated_reports)}")
        print(f"   Output Directory: {report_dir}")
        
        if analyses:
            avg_score = sum(a.get('overall_score', 0) for a in analyses) / len(analyses)
            print(f"   Average SEO Score: {avg_score:.1f}/100")
        
        print("\n📁 Generated Files:")
        for report_file in generated_reports:
            print(f"   • {report_file}")
        
        print("\n💡 Next Steps:")
        print("   1. Review the generated reports")
        print("   2. Prioritize critical issues")
        print("   3. Implement recommended improvements")
        print("   4. Re-run analysis to track progress")
        
        self.results = {
            'analyses': analyses,
            'reports': generated_reports,
            'timestamp': timestamp
        }
        
        return self.results


def main():
    """Main entry point for command-line usage"""
    
    parser = argparse.ArgumentParser(
        description='AI-Powered SEO Automation Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze URLs from config.json
  python main.py

  # Analyze specific URLs
  python main.py --urls https://example.com https://wikipedia.org

  # Skip AI insights (if API key not available)
  python main.py --skip-ai

  # Use custom config file
  python main.py --config my_config.json
        """
    )
    
    parser.add_argument(
        '--urls',
        nargs='+',
        help='URLs to analyze (overrides config.json)'
    )
    
    parser.add_argument(
        '--config',
        default='config.json',
        help='Configuration file (default: config.json)'
    )
    
    parser.add_argument(
        '--skip-ai',
        action='store_true',
        help='Skip AI insights generation'
    )
    
    args = parser.parse_args()
    
    # Initialize and run automation
    try:
        automation = SEOAutomation(args.config)
        automation.run(urls=args.urls, skip_ai=args.skip_ai)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
