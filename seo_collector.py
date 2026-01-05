"""
SEO Data Collector Module
Collects real SEO data from websites using multiple methods:
1. Google PageSpeed Insights API (no auth required)
2. Web scraping for on-page SEO elements
3. Basic technical SEO checks
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import time
from datetime import datetime
from typing import Dict, List, Any


class SEODataCollector:
    """Collects comprehensive SEO data from target URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def collect_all_data(self, url: str) -> Dict[str, Any]:
        """Collect all SEO data for a given URL"""
        print(f"\n📊 Collecting SEO data for: {url}")
        
        data = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "domain": urlparse(url).netloc,
            "page_speed": self.get_pagespeed_data(url),
            "on_page_seo": self.get_onpage_seo(url),
            "technical_seo": self.get_technical_seo(url)
        }
        
        return data
    
    def get_pagespeed_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from Google PageSpeed Insights API"""
        print("  ⚡ Fetching PageSpeed Insights...")
        
        api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            "url": url,
            "strategy": "mobile",  # mobile or desktop
            "category": ["performance", "seo", "accessibility"]
        }
        
        try:
            response = self.session.get(api_url, params=params, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            lighthouse = result.get("lighthouseResult", {})
            categories = lighthouse.get("categories", {})
            audits = lighthouse.get("audits", {})
            
            # Extract key metrics
            data = {
                "performance_score": categories.get("performance", {}).get("score", 0) * 100,
                "seo_score": categories.get("seo", {}).get("score", 0) * 100,
                "accessibility_score": categories.get("accessibility", {}).get("score", 0) * 100,
                "first_contentful_paint": audits.get("first-contentful-paint", {}).get("displayValue", "N/A"),
                "speed_index": audits.get("speed-index", {}).get("displayValue", "N/A"),
                "largest_contentful_paint": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
                "time_to_interactive": audits.get("interactive", {}).get("displayValue", "N/A"),
                "total_blocking_time": audits.get("total-blocking-time", {}).get("displayValue", "N/A"),
                "cumulative_layout_shift": audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
                "mobile_friendly": audits.get("viewport", {}).get("score", 0) == 1,
            }
            
            print(f"    ✓ Performance: {data['performance_score']:.0f}/100")
            print(f"    ✓ SEO Score: {data['seo_score']:.0f}/100")
            
            return data
            
        except Exception as e:
            print(f"    ⚠ PageSpeed API error: {str(e)}")
            return {"error": str(e)}
    
    def get_onpage_seo(self, url: str) -> Dict[str, Any]:
        """Scrape and analyze on-page SEO elements"""
        print("  🔍 Analyzing on-page SEO...")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract meta tags
            title = soup.find('title')
            title_text = title.string if title else None
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_desc_content = meta_desc.get('content') if meta_desc else None
            
            # Get heading structure
            headings = {
                'h1': [h.get_text(strip=True) for h in soup.find_all('h1')],
                'h2': [h.get_text(strip=True) for h in soup.find_all('h2')],
                'h3': [h.get_text(strip=True) for h in soup.find_all('h3')]
            }
            
            # Image analysis
            images = soup.find_all('img')
            images_without_alt = sum(1 for img in images if not img.get('alt'))
            
            # Links analysis
            internal_links = []
            external_links = []
            domain = urlparse(url).netloc
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                if domain in href or href.startswith('/'):
                    internal_links.append(href)
                elif href.startswith('http'):
                    external_links.append(href)
            
            # Content analysis
            text_content = soup.get_text(separator=' ', strip=True)
            word_count = len(text_content.split())
            
            data = {
                "title": title_text,
                "title_length": len(title_text) if title_text else 0,
                "meta_description": meta_desc_content,
                "meta_description_length": len(meta_desc_content) if meta_desc_content else 0,
                "h1_count": len(headings['h1']),
                "h1_tags": headings['h1'][:3],  # First 3
                "h2_count": len(headings['h2']),
                "h3_count": len(headings['h3']),
                "total_images": len(images),
                "images_without_alt": images_without_alt,
                "internal_links_count": len(internal_links),
                "external_links_count": len(external_links),
                "word_count": word_count,
                "has_meta_description": bool(meta_desc_content),
                "has_proper_title": bool(title_text and 30 <= len(title_text) <= 60)
            }
            
            print(f"    ✓ Title: {title_text[:50] if title_text else 'Missing'}...")
            print(f"    ✓ Word count: {word_count}")
            
            return data
            
        except Exception as e:
            print(f"    ⚠ On-page SEO error: {str(e)}")
            return {"error": str(e)}
    
    def get_technical_seo(self, url: str) -> Dict[str, Any]:
        """Check technical SEO aspects"""
        print("  🔧 Checking technical SEO...")
        
        try:
            response = self.session.get(url, timeout=30, allow_redirects=False)
            
            data = {
                "status_code": response.status_code,
                "is_https": url.startswith('https://'),
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                "content_type": response.headers.get('content-type', ''),
                "server": response.headers.get('server', 'Unknown'),
                "has_redirect": response.is_redirect,
                "redirect_location": response.headers.get('location') if response.is_redirect else None,
                "content_length": len(response.content),
                "has_cache_control": 'cache-control' in response.headers,
                "has_compression": 'content-encoding' in response.headers
            }
            
            # Check robots.txt
            robots_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
            try:
                robots_response = self.session.get(robots_url, timeout=10)
                data["has_robots_txt"] = robots_response.status_code == 200
            except:
                data["has_robots_txt"] = False
            
            # Check sitemap
            sitemap_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/sitemap.xml"
            try:
                sitemap_response = self.session.get(sitemap_url, timeout=10)
                data["has_sitemap"] = sitemap_response.status_code == 200
            except:
                data["has_sitemap"] = False
            
            print(f"    ✓ Status: {data['status_code']}")
            print(f"    ✓ HTTPS: {data['is_https']}")
            print(f"    ✓ Response time: {data['response_time_ms']}ms")
            
            return data
            
        except Exception as e:
            print(f"    ⚠ Technical SEO error: {str(e)}")
            return {"error": str(e)}
    
    def save_data(self, data: Dict[str, Any], output_path: str):
        """Save collected data to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Data saved to: {output_path}")


def collect_seo_data(urls: List[str], output_dir: str = "data") -> List[Dict[str, Any]]:
    """Main function to collect SEO data for multiple URLs"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    collector = SEODataCollector()
    all_data = []
    
    for url in urls:
        try:
            data = collector.collect_all_data(url)
            all_data.append(data)
            
            # Save individual file
            domain = urlparse(url).netloc.replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{output_dir}/seo_data_{domain}_{timestamp}.json"
            collector.save_data(data, filename)
            
            # Rate limiting to be respectful
            if len(urls) > 1:
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Error collecting data for {url}: {str(e)}")
            all_data.append({"url": url, "error": str(e)})
    
    # Save combined data
    combined_path = f"{output_dir}/seo_data_combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    return all_data


if __name__ == "__main__":
    # Test with sample URLs
    test_urls = [
        "https://www.wikipedia.org",
        "https://example.com"
    ]
    
    data = collect_seo_data(test_urls)
    print(f"\n✅ Collected data for {len(data)} URLs")
