import requests
import re
from datetime import datetime

def test_maritime_html_parsing():
    """Test HTML parsing with actual maritime weather page"""
    
    # Test URL
    test_url = "https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"🧪 Testing maritime HTML parsing...")
        print(f"🔗 URL: {test_url}")
        
        response = requests.get(test_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ HTTP 200 OK")
            html_content = response.text
            
            print(f"\n📊 HTML Analysis:")
            print(f"   📏 Content Length: {len(html_content)} characters")
            
            # Look for key patterns
            print(f"\n🔍 Pattern Analysis:")
            
            # Temperature
            temp_matches = re.findall(r'(\d+)°C', html_content)
            print(f"   🌡️  Temperature patterns found: {temp_matches}")
            
            # Humidity
            humidity_matches = re.findall(r'(\d+)%', html_content)
            print(f"   💧 Humidity patterns found: {humidity_matches}")
            
            # Wind speed
            wind_matches = re.findall(r'(\d+)\s*kt', html_content)
            print(f"   💨 Wind speed patterns found: {wind_matches}")
            
            # Gust wind
            gust_matches = re.findall(r'Gust:\s*(\d+)\s*kt', html_content)
            print(f"   🌪️  Gust wind patterns found: {gust_matches}")
            
            # Wind direction
            wind_dir_matches = re.findall(r'Angin Dari\s*([^<>\n]+)', html_content)
            print(f"   🧭 Wind direction patterns found: {wind_dir_matches}")
            
            # Wave height
            wave_matches = re.findall(r'(\d+\.?\d*)\s*m', html_content)
            print(f"   🌊 Wave height patterns found: {wave_matches}")
            
            # Current speed
            current_matches = re.findall(r'(\d+\.?\d*)\s*cm/s', html_content)
            print(f"   🌊 Current speed patterns found: {current_matches}")
            
            # Weather conditions
            weather_matches = re.findall(r'<td[^>]*>([^<>\n]+)</td>', html_content)
            print(f"   🌤️  Weather condition patterns found: {weather_matches[:10]}")  # First 10
            
            # Time patterns
            time_matches = re.findall(r'(\d{1,2}\s+Agu\s+\d{2},\s+\d{2}\.\d{2})', html_content)
            print(f"   ⏰ Time patterns found: {time_matches}")
            
            # Current time indicator
            if 'Saat ini' in html_content:
                print(f"   ✅ 'Saat ini' indicator found")
            else:
                print(f"   ❌ 'Saat ini' indicator not found")
            
            # Look for table structure
            print(f"\n📋 Table Structure Analysis:")
            table_matches = re.findall(r'<table[^>]*>(.*?)</table>', html_content, re.DOTALL)
            print(f"   📊 Tables found: {len(table_matches)}")
            
            # Look for specific data rows
            data_row_matches = re.findall(r'<tr[^>]*>(.*?)</tr>', html_content, re.DOTALL)
            print(f"   📝 Table rows found: {len(data_row_matches)}")
            
            # Enhanced pattern search
            print(f"\n🔍 Enhanced Pattern Search:")
            
            # Look for specific CSS classes
            css_classes = re.findall(r'class="([^"]*)"', html_content)
            unique_classes = list(set(css_classes))
            print(f"   🎨 CSS Classes found: {len(unique_classes)}")
            print(f"   🎨 Sample CSS Classes: {unique_classes[:20]}")
            
            # Look for weather text specifically
            weather_text_matches = re.findall(r'class="weather-text"[^>]*>([^<>\n]+)</', html_content)
            print(f"   🌤️  Weather text class matches: {weather_text_matches}")
            
            # Look for wind direction specifically
            wind_dir_class_matches = re.findall(r'class="[^"]*wind[^"]*"[^>]*>([^<>\n]+)</', html_content)
            print(f"   🧭 Wind direction class matches: {wind_dir_class_matches}")
            
            # Look for current direction specifically
            current_dir_class_matches = re.findall(r'class="[^"]*current[^"]*"[^>]*>([^<>\n]+)</', html_content)
            print(f"   🌊 Current direction class matches: {current_dir_class_matches}")
            
            # Look for wave classification specifically
            wave_class_matches = re.findall(r'class="[^"]*wave[^"]*"[^>]*>([^<>\n]+)</', html_content)
            print(f"   🌊 Wave classification class matches: {wave_class_matches}")
            
            # Look for button elements (might contain classifications)
            button_matches = re.findall(r'<button[^>]*>([^<>\n]+)</button>', html_content)
            print(f"   🔘 Button text matches: {button_matches}")
            
            # Look for span elements with specific text
            span_matches = re.findall(r'<span[^>]*>([^<>\n]+)</span>', html_content)
            # Filter for relevant weather terms
            weather_spans = [s for s in span_matches if any(term in s.lower() for term in ['hujan', 'berawan', 'cerah', 'barat', 'timur', 'utara', 'selatan', 'sedang', 'rendah', 'tinggi'])]
            print(f"   📝 Weather-related span matches: {weather_spans}")
            
            # Look for div elements with weather data
            div_matches = re.findall(r'<div[^>]*>([^<>\n]+)</div>', html_content)
            # Filter for relevant weather terms
            weather_divs = [d for d in div_matches if any(term in d.lower() for term in ['hujan', 'berawan', 'cerah', 'barat', 'timur', 'utara', 'selatan', 'sedang', 'rendah', 'tinggi', 'kt', 'm', 'cm/s'])]
            print(f"   📦 Weather-related div matches: {weather_divs[:10]}")
            
            # Sample HTML around weather data
            print(f"\n🔍 Sample HTML around weather data:")
            sample_start = html_content.find('Hujan Ringan')
            if sample_start > 0:
                sample_html = html_content[max(0, sample_start-300):sample_start+300]
                print(f"   📄 Sample HTML: {sample_html}")
            
            # Look for specific data around "Saat ini"
            saat_ini_start = html_content.find('Saat ini')
            if saat_ini_start > 0:
                saat_ini_html = html_content[max(0, saat_ini_start-500):saat_ini_start+500]
                print(f"\n🔍 HTML around 'Saat ini':")
                print(f"   📄 Saat ini HTML: {saat_ini_html}")
            
        else:
            print(f"❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_maritime_html_parsing() 