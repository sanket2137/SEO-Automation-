"""
SEO Data Analyzer Module
Analyzes collected SEO data to identify trends, issues, and opportunities
"""

import json
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime


class SEOAnalyzer:
    """Analyzes SEO data and generates insights"""
    
    def __init__(self, seo_data: Dict[str, Any]):
        self.data = seo_data
        self.url = seo_data.get('url', 'Unknown')
        self.issues = []
        self.opportunities = []
        self.strengths = []
        self.scores = {}
    
    def analyze_all(self) -> Dict[str, Any]:
        """Run all analysis methods"""
        print(f"\n📈 Analyzing SEO data for: {self.url}")
        
        self.analyze_page_speed()
        self.analyze_on_page_seo()
        self.analyze_technical_seo()
        self.calculate_overall_score()
        
        analysis = {
            "url": self.url,
            "timestamp": datetime.now().isoformat(),
            "overall_score": self.scores.get('overall', 0),
            "category_scores": self.scores,
            "critical_issues": [i for i in self.issues if i['severity'] == 'critical'],
            "warnings": [i for i in self.issues if i['severity'] == 'warning'],
            "all_issues": self.issues,
            "opportunities": self.opportunities,
            "strengths": self.strengths,
            "summary": self.generate_summary()
        }
        
        return analysis
    
    def analyze_page_speed(self):
        """Analyze page speed metrics"""
        speed_data = self.data.get('page_speed', {})
        
        if 'error' in speed_data:
            self.issues.append({
                "category": "Performance",
                "severity": "warning",
                "issue": "Could not retrieve PageSpeed data",
                "details": speed_data['error']
            })
            return
        
        perf_score = speed_data.get('performance_score', 0)
        seo_score = speed_data.get('seo_score', 0)
        
        # Performance analysis
        if perf_score >= 90:
            self.strengths.append("Excellent page performance")
        elif perf_score >= 50:
            self.issues.append({
                "category": "Performance",
                "severity": "warning",
                "issue": f"Moderate performance score: {perf_score:.0f}/100",
                "recommendation": "Optimize images, minify CSS/JS, enable caching"
            })
        else:
            self.issues.append({
                "category": "Performance",
                "severity": "critical",
                "issue": f"Poor performance score: {perf_score:.0f}/100",
                "recommendation": "Critical: Improve server response time, optimize images, reduce JavaScript"
            })
        
        # SEO score analysis
        if seo_score >= 90:
            self.strengths.append(f"Strong technical SEO score: {seo_score:.0f}/100")
        elif seo_score < 80:
            self.issues.append({
                "category": "Technical SEO",
                "severity": "warning",
                "issue": f"SEO score needs improvement: {seo_score:.0f}/100",
                "recommendation": "Review meta tags, heading structure, and mobile-friendliness"
            })
        
        # Mobile-friendly check
        if not speed_data.get('mobile_friendly', False):
            self.issues.append({
                "category": "Mobile",
                "severity": "critical",
                "issue": "Page is not mobile-friendly",
                "recommendation": "Add viewport meta tag and ensure responsive design"
            })
        
        self.scores['performance'] = perf_score
        self.scores['technical_seo'] = seo_score
    
    def analyze_on_page_seo(self):
        """Analyze on-page SEO elements"""
        onpage = self.data.get('on_page_seo', {})
        
        if 'error' in onpage:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "warning",
                "issue": "Could not analyze on-page elements",
                "details": onpage['error']
            })
            return
        
        # Title tag analysis
        title_length = onpage.get('title_length', 0)
        if title_length == 0:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "critical",
                "issue": "Missing title tag",
                "recommendation": "Add a descriptive title tag (50-60 characters)"
            })
        elif title_length < 30:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "warning",
                "issue": f"Title tag too short: {title_length} characters",
                "recommendation": "Expand title to 50-60 characters for better SEO"
            })
        elif title_length > 60:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "warning",
                "issue": f"Title tag too long: {title_length} characters",
                "recommendation": "Shorten title to 50-60 characters to avoid truncation"
            })
        else:
            self.strengths.append(f"Good title length: {title_length} characters")
        
        # Meta description analysis
        meta_desc_length = onpage.get('meta_description_length', 0)
        if meta_desc_length == 0:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "critical",
                "issue": "Missing meta description",
                "recommendation": "Add a compelling meta description (150-160 characters)"
            })
        elif meta_desc_length < 120:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "warning",
                "issue": f"Meta description too short: {meta_desc_length} characters",
                "recommendation": "Expand to 150-160 characters for better CTR"
            })
        elif meta_desc_length > 160:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "warning",
                "issue": f"Meta description too long: {meta_desc_length} characters",
                "recommendation": "Shorten to 150-160 characters to avoid truncation"
            })
        else:
            self.strengths.append(f"Good meta description length: {meta_desc_length} characters")
        
        # Heading structure
        h1_count = onpage.get('h1_count', 0)
        if h1_count == 0:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "critical",
                "issue": "Missing H1 heading",
                "recommendation": "Add exactly one H1 tag with primary keyword"
            })
        elif h1_count > 1:
            self.issues.append({
                "category": "On-Page SEO",
                "severity": "warning",
                "issue": f"Multiple H1 tags found: {h1_count}",
                "recommendation": "Use only one H1 tag per page"
            })
        else:
            self.strengths.append("Proper H1 structure")
        
        # Images analysis
        total_images = onpage.get('total_images', 0)
        images_without_alt = onpage.get('images_without_alt', 0)
        
        if total_images > 0 and images_without_alt > 0:
            percentage = (images_without_alt / total_images) * 100
            if percentage > 20:
                self.issues.append({
                    "category": "Image Optimization",
                    "severity": "warning",
                    "issue": f"{images_without_alt}/{total_images} images missing alt text ({percentage:.0f}%)",
                    "recommendation": "Add descriptive alt text to all images for accessibility and SEO"
                })
            else:
                self.opportunities.append(f"Add alt text to {images_without_alt} remaining images")
        elif total_images > 0:
            self.strengths.append("All images have alt text")
        
        # Content analysis
        word_count = onpage.get('word_count', 0)
        if word_count < 300:
            self.issues.append({
                "category": "Content",
                "severity": "warning",
                "issue": f"Thin content: only {word_count} words",
                "recommendation": "Aim for at least 1000 words for better ranking potential"
            })
        elif word_count > 1500:
            self.strengths.append(f"Comprehensive content: {word_count} words")
        else:
            self.opportunities.append(f"Consider expanding content (current: {word_count} words)")
        
        # Links analysis
        internal_links = onpage.get('internal_links_count', 0)
        if internal_links < 3:
            self.opportunities.append("Add more internal links to improve site structure")
        
        # Calculate on-page score
        score = 100
        if title_length == 0: score -= 20
        elif title_length < 30 or title_length > 60: score -= 10
        if meta_desc_length == 0: score -= 20
        elif meta_desc_length < 120 or meta_desc_length > 160: score -= 10
        if h1_count != 1: score -= 15
        if images_without_alt > total_images * 0.2: score -= 10
        if word_count < 300: score -= 15
        
        self.scores['on_page_seo'] = max(0, score)
    
    def analyze_technical_seo(self):
        """Analyze technical SEO aspects"""
        technical = self.data.get('technical_seo', {})
        
        if 'error' in technical:
            self.issues.append({
                "category": "Technical SEO",
                "severity": "warning",
                "issue": "Could not analyze technical aspects",
                "details": technical['error']
            })
            return
        
        # HTTPS check
        if not technical.get('is_https', False):
            self.issues.append({
                "category": "Security",
                "severity": "critical",
                "issue": "Site not using HTTPS",
                "recommendation": "Implement SSL certificate for security and SEO"
            })
        else:
            self.strengths.append("Secure HTTPS connection")
        
        # Status code check
        status_code = technical.get('status_code', 0)
        if status_code != 200:
            self.issues.append({
                "category": "Technical SEO",
                "severity": "critical",
                "issue": f"Unexpected status code: {status_code}",
                "recommendation": "Ensure page returns 200 OK status"
            })
        
        # Response time
        response_time = technical.get('response_time_ms', 0)
        if response_time > 2000:
            self.issues.append({
                "category": "Performance",
                "severity": "warning",
                "issue": f"Slow response time: {response_time}ms",
                "recommendation": "Optimize server performance, use CDN, enable caching"
            })
        elif response_time < 500:
            self.strengths.append(f"Fast response time: {response_time}ms")
        
        # Robots.txt and sitemap
        if not technical.get('has_robots_txt', False):
            self.opportunities.append("Add robots.txt file to guide search engine crawlers")
        else:
            self.strengths.append("robots.txt file present")
        
        if not technical.get('has_sitemap', False):
            self.opportunities.append("Add XML sitemap for better indexing")
        else:
            self.strengths.append("XML sitemap present")
        
        # Compression
        if not technical.get('has_compression', False):
            self.opportunities.append("Enable GZIP/Brotli compression to reduce page size")
    
    def calculate_overall_score(self):
        """Calculate weighted overall SEO score"""
        weights = {
            'performance': 0.3,
            'technical_seo': 0.3,
            'on_page_seo': 0.4
        }
        
        total = sum(self.scores.get(key, 0) * weight 
                   for key, weight in weights.items())
        
        self.scores['overall'] = round(total, 1)
    
    def generate_summary(self) -> str:
        """Generate a text summary of the analysis"""
        critical_count = len([i for i in self.issues if i['severity'] == 'critical'])
        warning_count = len([i for i in self.issues if i['severity'] == 'warning'])
        
        summary = f"""
SEO Analysis Summary for {self.url}
{'='*60}

Overall SEO Score: {self.scores.get('overall', 0):.1f}/100

Category Scores:
- Performance: {self.scores.get('performance', 0):.1f}/100
- Technical SEO: {self.scores.get('technical_seo', 0):.1f}/100
- On-Page SEO: {self.scores.get('on_page_seo', 0):.1f}/100

Issues Found:
- Critical Issues: {critical_count}
- Warnings: {warning_count}

Top Strengths ({len(self.strengths)}):
{self._format_list(self.strengths[:5])}

Top Issues:
{self._format_issues(self.issues[:5])}

Opportunities for Improvement:
{self._format_list(self.opportunities[:5])}
"""
        return summary.strip()
    
    def _format_list(self, items: List[str]) -> str:
        """Format a list of items"""
        if not items:
            return "  None identified"
        return "\n".join(f"  ✓ {item}" for item in items)
    
    def _format_issues(self, issues: List[Dict]) -> str:
        """Format issues list"""
        if not issues:
            return "  None - Great job!"
        
        formatted = []
        for issue in issues:
            severity_icon = "🔴" if issue['severity'] == 'critical' else "🟡"
            formatted.append(f"  {severity_icon} [{issue['category']}] {issue['issue']}")
            if 'recommendation' in issue:
                formatted.append(f"     → {issue['recommendation']}")
        
        return "\n".join(formatted)


def analyze_seo_data(data_file: str) -> Dict[str, Any]:
    """Analyze SEO data from a JSON file"""
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both single URL and multiple URLs
    if isinstance(data, list):
        analyses = []
        for item in data:
            analyzer = SEOAnalyzer(item)
            analysis = analyzer.analyze_all()
            analyses.append(analysis)
        return analyses
    else:
        analyzer = SEOAnalyzer(data)
        return analyzer.analyze_all()


if __name__ == "__main__":
    # Test analysis
    import sys
    if len(sys.argv) > 1:
        result = analyze_seo_data(sys.argv[1])
        print(json.dumps(result, indent=2))
