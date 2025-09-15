#!/usr/bin/env python3
"""
Deep HTML Analysis for Maritime Weather Pages
Analyzes the HTML structure to find wind direction and current direction data
"""

import requests
import re
from bs4 import BeautifulSoup

def deep_html_analysis():
    """Perform deep HTML analysis of maritime weather pages"""
    
    # Test with a few maritime areas
    test_areas = [
        {
            'name': 'Perairan Aceh Utara - Aceh Timur',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur'
        },
        {
            'name': 'Perairan Banda Aceh',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-banda-aceh'
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for area in test_areas:
        print(f"\n🔍 Deep Analysis: {area['name']}")
        print(f"🔗 URL: {area['url']}")
        print("=" * 60)
        
        try:
            response = requests.get(area['url'], headers=headers, timeout=30)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Parse with BeautifulSoup for better analysis
                soup = BeautifulSoup(html_content, 'html.parser')
                
                print(f"📊 HTML Structure Analysis:")
                
                # Look for tables
                tables = soup.find_all('table')
                print(f"   📋 Found {len(tables)} table(s)")
                
                for i, table in enumerate(tables):
                    print(f"\n   📋 Table {i+1}:")
                    
                    # Look for table headers
                    headers = table.find_all('th')
                    if headers:
                        print(f"      🏷️  Headers: {[h.get_text(strip=True) for h in headers]}")
                    
                    # Look for table rows
                    rows = table.find_all('tr')
                    print(f"      📝 Rows: {len(rows)}")
                    
                    # Analyze first few rows
                    for j, row in enumerate(rows[:3]):  # First 3 rows
                        cells = row.find_all(['td', 'th'])
                        if cells:
                            cell_texts = [cell.get_text(strip=True) for cell in cells]
                            print(f"         Row {j+1}: {cell_texts}")
                
                # Look for specific patterns in the HTML
                print(f"\n🔍 Pattern Analysis:")
                
                # Look for wind-related text
                wind_patterns = [
                    r'[Aa]ngin[:\s]*([^<>\n]+)',
                    r'[Ww]ind[:\s]*([^<>\n]+)',
                    r'[Aa]rah[:\s]*[Aa]ngin[:\s]*([^<>\n]+)',
                    r'[Dd]irection[:\s]*[Ww]ind[:\s]*([^<>\n]+)'
                ]
                
                for pattern in wind_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    if matches:
                        print(f"   💨 Wind pattern '{pattern}': {matches}")
                
                # Look for current-related text
                current_patterns = [
                    r'[Aa]rus[:\s]*([^<>\n]+)',
                    r'[Cc]urrent[:\s]*([^<>\n]+)',
                    r'[Aa]rah[:\s]*[Aa]rus[:\s]*([^<>\n]+)',
                    r'[Dd]irection[:\s]*[Cc]urrent[:\s]*([^<>\n]+)'
                ]
                
                for pattern in current_patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    if matches:
                        print(f"   🌊 Current pattern '{pattern}': {matches}")
                
                # Look for direction keywords in the entire HTML
                direction_keywords = ['barat', 'timur', 'utara', 'selatan', 'tenggara', 'barat daya', 'barat laut', 'timur laut']
                
                print(f"\n🧭 Direction Keywords Found:")
                for keyword in direction_keywords:
                    if keyword in html_content.lower():
                        # Find context around the keyword
                        keyword_matches = re.findall(f'([^<>\n]{{0,50}}{keyword}[^<>\n]{{0,50}})', html_content, re.IGNORECASE)
                        if keyword_matches:
                            print(f"   {keyword.upper()}: {keyword_matches[:2]}")  # Show first 2 matches
                
                # Look for specific CSS classes that might contain direction data
                print(f"\n🎨 CSS Class Analysis:")
                css_classes = re.findall(r'class="([^"]*)"', html_content)
                unique_classes = list(set(css_classes))
                
                # Filter for potentially relevant classes
                relevant_classes = [cls for cls in unique_classes if any(term in cls.lower() for term in ['wind', 'direction', 'current', 'arus', 'angin'])]
                if relevant_classes:
                    print(f"   🎯 Relevant classes: {relevant_classes}")
                
                # Look for data attributes
                data_attrs = re.findall(r'data-[^=]+="([^"]*)"', html_content)
                if data_attrs:
                    print(f"   📊 Data attributes: {data_attrs[:5]}")  # Show first 5
                
                # Look for JavaScript variables that might contain weather data
                script_tags = soup.find_all('script')
                print(f"\n📜 Script Analysis:")
                print(f"   Found {len(script_tags)} script tag(s)")
                
                for i, script in enumerate(script_tags):
                    script_content = script.get_text()
                    if script_content:
                        # Look for weather-related variables
                        weather_vars = re.findall(r'(\w+)\s*[:=]\s*["\']([^"\']+)["\']', script_content)
                        relevant_vars = [var for var in weather_vars if any(term in var[0].lower() for term in ['wind', 'current', 'direction', 'weather', 'cuaca'])]
                        if relevant_vars:
                            print(f"      Script {i+1} weather vars: {relevant_vars[:3]}")
                        
                        # Look for direction data in JavaScript arrays/objects
                        direction_patterns = [
                            r'["\']([^"\']*(?:barat|timur|utara|selatan|tenggara|barat daya|barat laut|timur laut)[^"\']*)["\']',
                            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d+\s*kt',  # Direction + speed pattern
                            r'wind_from["\']?\s*:\s*["\']?([^"\']+)["\']?',  # wind_from field
                            r'current_to["\']?\s*:\s*["\']?([^"\']+)["\']?'   # current_to field
                        ]
                        
                        for pattern in direction_patterns:
                            matches = re.findall(pattern, script_content, re.IGNORECASE)
                            if matches:
                                print(f"      Script {i+1} direction pattern '{pattern}': {matches[:5]}")
                        
                        # Look for JavaScript data structures containing weather info
                        js_data_patterns = [
                            r'(\w+)\s*:\s*\{[^}]*"time"[^}]*"weather"[^}]*"temp_avg"[^}]*"rh_avg"[^}]*"wind_from"[^}]*"wind_speed"[^}]*\}',
                            r'(\w+)\s*:\s*\[[^\]]*"Tenggara[^\]]*"Barat Laut"[^\]]*"Barat Daya"[^\]]*"Timur Laut"[^\]]*\]',
                            r'(\w+)\s*:\s*\{[^}]*"wind_from"[^}]*"current_to"[^}]*\}'
                        ]
                        
                        for pattern in js_data_patterns:
                            matches = re.findall(pattern, script_content, re.IGNORECASE | re.DOTALL)
                            if matches:
                                print(f"      Script {i+1} data structure '{pattern}': {matches[:3]}")
                        
                        # Look for specific wind direction values
                        wind_dirs = re.findall(r'["\']([^"\']*(?:Tenggara|Barat Laut|Barat Daya|Timur Laut|Barat|Timur|Utara|Selatan)[^"\']*)["\']', script_content, re.IGNORECASE)
                        if wind_dirs:
                            print(f"      Script {i+1} wind directions: {list(set(wind_dirs))[:5]}")
                        
                        # Look for current direction values
                        current_dirs = re.findall(r'["\']([^"\']*(?:Barat|Timur|Utara|Selatan)[^"\']*)["\']', script_content, re.IGNORECASE)
                        if current_dirs:
                            print(f"      Script {i+1} current directions: {list(set(current_dirs))[:5]}")
                
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    deep_html_analysis() 