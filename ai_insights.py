"""
AI Insights Generator using Google Gemini
Generates actionable SEO recommendations using AI
"""

import google.generativeai as genai
import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv


class GeminiInsightsGenerator:
    """Generate AI-powered SEO insights using Google Gemini"""
    
    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        print("✓ Gemini AI initialized")
    
    def generate_insights(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive AI insights from SEO analysis"""
        print("\n🤖 Generating AI insights with Gemini...")
        
        # Prepare the prompt with structured data
        prompt = self._create_analysis_prompt(analysis_data)
        
        try:
            # Generate insights
            response = self.model.generate_content(prompt)
            insights_text = response.text
            
            # Parse and structure the response
            insights = self._parse_ai_response(insights_text, analysis_data)
            
            print("✓ AI insights generated successfully")
            return insights
            
        except Exception as e:
            print(f"⚠ Error generating AI insights: {str(e)}")
            return {
                "error": str(e),
                "fallback_insights": self._generate_fallback_insights(analysis_data)
            }
    
    def _create_analysis_prompt(self, analysis: Dict[str, Any]) -> str:
        """Create a detailed prompt for Gemini"""
        
        url = analysis.get('url', 'Unknown')
        overall_score = analysis.get('overall_score', 0)
        scores = analysis.get('category_scores', {})
        issues = analysis.get('all_issues', [])
        strengths = analysis.get('strengths', [])
        opportunities = analysis.get('opportunities', [])
        
        # Format issues for the prompt
        critical_issues = [i for i in issues if i.get('severity') == 'critical']
        warnings = [i for i in issues if i.get('severity') == 'warning']
        
        prompt = f"""You are an expert SEO consultant analyzing a website. Provide actionable insights and recommendations.

Website: {url}
Overall SEO Score: {overall_score}/100

PERFORMANCE METRICS:
- Performance Score: {scores.get('performance', 'N/A')}/100
- Technical SEO Score: {scores.get('technical_seo', 'N/A')}/100
- On-Page SEO Score: {scores.get('on_page_seo', 'N/A')}/100

CRITICAL ISSUES ({len(critical_issues)}):
{self._format_issues_for_prompt(critical_issues)}

WARNINGS ({len(warnings)}):
{self._format_issues_for_prompt(warnings)}

STRENGTHS:
{self._format_list_for_prompt(strengths)}

OPPORTUNITIES:
{self._format_list_for_prompt(opportunities)}

Based on this comprehensive SEO analysis, provide:

1. **Executive Summary** (2-3 sentences)
   - Overall assessment of the website's SEO health
   - Most critical area needing attention

2. **Top 3 Priority Actions** (must be specific and actionable)
   - Focus on quick wins and high-impact improvements
   - Include specific metrics or targets where applicable
   - Order by priority (most important first)

3. **Strategic Recommendations** (3-4 items)
   - Long-term SEO improvements
   - Content strategy suggestions
   - Technical optimizations

4. **Competitive Advantage Opportunities**
   - Areas where the site can differentiate
   - Emerging SEO trends to capitalize on

5. **30-Day Action Plan**
   - Week-by-week breakdown of what to implement
   - Clear milestones and expected outcomes

Format your response clearly with these exact section headers. Be specific, actionable, and data-driven.
"""
        return prompt
    
    def _format_issues_for_prompt(self, issues: List[Dict]) -> str:
        """Format issues for inclusion in prompt"""
        if not issues:
            return "None"
        
        formatted = []
        for i, issue in enumerate(issues[:10], 1):
            category = issue.get('category', 'General')
            description = issue.get('issue', 'Unknown issue')
            recommendation = issue.get('recommendation', '')
            
            formatted.append(f"{i}. [{category}] {description}")
            if recommendation:
                formatted.append(f"   Recommendation: {recommendation}")
        
        return "\n".join(formatted)
    
    def _format_list_for_prompt(self, items: List[str]) -> str:
        """Format a simple list for the prompt"""
        if not items:
            return "None identified"
        return "\n".join(f"- {item}" for item in items[:10])
    
    def _parse_ai_response(self, ai_text: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure the AI response"""
        
        return {
            "url": analysis_data.get('url'),
            "ai_insights": ai_text,
            "generated_at": analysis_data.get('timestamp'),
            "overall_score": analysis_data.get('overall_score'),
            "insights_metadata": {
                "model": "gemini-pro",
                "analysis_version": "1.0",
                "issues_analyzed": len(analysis_data.get('all_issues', [])),
                "strengths_identified": len(analysis_data.get('strengths', []))
            }
        }
    
    def _generate_fallback_insights(self, analysis: Dict[str, Any]) -> str:
        """Generate basic insights if AI fails"""
        
        score = analysis.get('overall_score', 0)
        critical_issues = [i for i in analysis.get('all_issues', []) 
                          if i.get('severity') == 'critical']
        
        fallback = f"""
FALLBACK SEO INSIGHTS FOR {analysis.get('url')}

Overall Assessment:
Your site scored {score}/100. """
        
        if score >= 80:
            fallback += "This is a strong foundation, but there's always room for improvement."
        elif score >= 60:
            fallback += "There are several areas that need attention to improve rankings."
        else:
            fallback += "Significant improvements are needed to compete effectively."
        
        fallback += f"""

Priority Actions:
"""
        if critical_issues:
            fallback += "1. Address Critical Issues:\n"
            for issue in critical_issues[:3]:
                fallback += f"   - {issue.get('issue')}\n"
                if 'recommendation' in issue:
                    fallback += f"     → {issue.get('recommendation')}\n"
        
        if analysis.get('opportunities'):
            fallback += "\n2. Quick Wins:\n"
            for opp in analysis.get('opportunities')[:3]:
                fallback += f"   - {opp}\n"
        
        return fallback
    
    def generate_comparison_insights(self, analyses: List[Dict[str, Any]]) -> str:
        """Generate comparative insights for multiple URLs"""
        
        if len(analyses) < 2:
            return "Need at least 2 URLs for comparison"
        
        prompt = f"""You are an expert SEO consultant comparing multiple websites.

Compare these {len(analyses)} websites and provide insights:

"""
        for i, analysis in enumerate(analyses, 1):
            prompt += f"""
Website {i}: {analysis.get('url')}
- Overall Score: {analysis.get('overall_score')}/100
- Performance: {analysis.get('category_scores', {}).get('performance')}/100
- Critical Issues: {len([x for x in analysis.get('all_issues', []) if x.get('severity') == 'critical'])}
"""
        
        prompt += """

Provide:
1. Comparative Analysis - Which site is performing best and why?
2. Common Issues - What problems affect multiple sites?
3. Best Practices - Which site demonstrates the best practices to adopt?
4. Recommendations - Specific advice for each site

Be concise and actionable.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Comparison error: {str(e)}"


def generate_ai_insights(analysis_file: str, api_key: str = None) -> Dict[str, Any]:
    """Main function to generate insights from analysis file"""
    
    # Load analysis data
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # Initialize AI generator
    generator = GeminiInsightsGenerator(api_key)
    
    # Handle both single and multiple analyses
    if isinstance(analysis, list):
        insights = []
        for item in analysis:
            insight = generator.generate_insights(item)
            insights.append(insight)
        
        # Also generate comparison
        if len(analysis) > 1:
            comparison = generator.generate_comparison_insights(analysis)
            return {
                "individual_insights": insights,
                "comparative_analysis": comparison
            }
        return insights[0]
    else:
        return generator.generate_insights(analysis)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        insights = generate_ai_insights(sys.argv[1])
        print(json.dumps(insights, indent=2))
    else:
        print("Usage: python ai_insights.py <analysis_file.json>")
