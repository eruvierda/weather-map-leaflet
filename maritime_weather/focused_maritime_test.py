import requests
import re
from datetime import datetime

def focused_maritime_test():
    """Focused test for specific maritime weather patterns"""
    
    test_url = "https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"🎯 Focused Maritime Weather Pattern Test")
        print(f"🔗 URL: {test_url}")
        
        response = requests.get(test_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            html_content = response.text
            
            print(f"\n🔍 Pattern Extraction Results:")
            
            # 1. Weather Text (Cuaca)
            weather_patterns = [
                r'class="weather-text"[^>]*>([^<>\n]+)</',
                r'<span[^>]*>([^<>\n]+)</span>',
                r'<div[^>]*>([^<>\n]+)</div>'
            ]
            
            for i, pattern in enumerate(weather_patterns):
                matches = re.findall(pattern, html_content)
                weather_terms = [m for m in matches if any(term in m.lower() for term in ['hujan', 'berawan', 'cerah', 'mendung'])]
                if weather_terms:
                    print(f"   🌤️  Weather Pattern {i+1}: {weather_terms[:5]}")
            
            # 2. Wind Direction (Angin Dari)
            wind_patterns = [
                r'class="[^"]*wind[^"]*"[^>]*>([^<>\n]+)</',
                r'<span[^>]*>([^<>\n]+)</span>',
                r'<div[^>]*>([^<>\n]+)</div>'
            ]
            
            for i, pattern in enumerate(wind_patterns):
                matches = re.findall(pattern, html_content)
                wind_terms = [m for m in matches if any(term in m.lower() for term in ['barat', 'timur', 'utara', 'selatan', 'tenggara', 'barat daya', 'barat laut', 'timur laut'])]
                if wind_terms:
                    print(f"   🧭 Wind Pattern {i+1}: {wind_terms[:5]}")
            
            # 3. Wave Classification (Gelombang)
            wave_patterns = [
                r'class="[^"]*wave[^"]*"[^>]*>([^<>\n]+)</',
                r'<button[^>]*>([^<>\n]+)</button>',
                r'<span[^>]*>([^<>\n]+)</span>'
            ]
            
            for i, pattern in enumerate(wave_patterns):
                matches = re.findall(pattern, html_content)
                wave_terms = [m for m in matches if any(term in m.lower() for term in ['sedang', 'rendah', 'tinggi', 'sangat tinggi'])]
                if wave_terms:
                    print(f"   🌊 Wave Pattern {i+1}: {wave_terms[:5]}")
            
            # 4. Current Direction (Arus Ke)
            current_patterns = [
                r'class="[^"]*current[^"]*"[^>]*>([^<>\n]+)</',
                r'<span[^>]*>([^<>\n]+)</span>',
                r'<div[^>]*>([^<>\n]+)</div>'
            ]
            
            for i, pattern in enumerate(current_patterns):
                matches = re.findall(pattern, html_content)
                current_terms = [m for m in matches if any(term in m.lower() for term in ['barat', 'timur', 'utara', 'selatan', 'tenggara', 'barat daya', 'barat laut', 'timur laut'])]
                if current_terms:
                    print(f"   🌊 Current Pattern {i+1}: {current_terms[:5]}")
            
            # 5. Gust Wind Speed
            gust_patterns = [
                r'Gust:\s*(\d+)\s*kt',
                r'Gust[^>]*>([^<>\n]+)</',
                r'<span[^>]*>Gust[^<>\n]*</span>'
            ]
            
            for i, pattern in enumerate(gust_patterns):
                matches = re.findall(pattern, html_content)
                if matches:
                    print(f"   🌪️  Gust Pattern {i+1}: {matches[:3]}")
            
            # 6. CSS Classes Analysis
            print(f"\n🎨 CSS Classes Analysis:")
            css_classes = re.findall(r'class="([^"]*)"', html_content)
            unique_classes = list(set(css_classes))
            
            # Filter relevant classes
            weather_classes = [c for c in unique_classes if any(term in c.lower() for term in ['weather', 'wind', 'wave', 'current', 'temp', 'humidity'])]
            print(f"   🌤️  Weather-related classes: {weather_classes[:10]}")
            
            # 7. Table Structure Analysis
            print(f"\n📋 Table Structure:")
            
            # Find table cells with specific content
            table_cells = re.findall(r'<td[^>]*class="([^"]*)"[^>]*>', html_content)
            unique_cell_classes = list(set(table_cells))
            print(f"   📊 Table cell classes: {unique_cell_classes[:10]}")
            
            # 8. Sample HTML around key data
            print(f"\n🔍 Sample HTML Analysis:")
            
            # Look for "Saat ini" row
            saat_ini_start = html_content.find('Saat ini')
            if saat_ini_start > 0:
                context_html = html_content[max(0, saat_ini_start-800):saat_ini_start+800]
                
                # Extract data from this context
                print(f"   📍 Context around 'Saat ini':")
                
                # Temperature in context
                temp_in_context = re.findall(r'(\d+)°C', context_html)
                if temp_in_context:
                    print(f"      🌡️  Temperature in context: {temp_in_context}")
                
                # Humidity in context
                humidity_in_context = re.findall(r'(\d+)%', context_html)
                if humidity_in_context:
                    print(f"      💧 Humidity in context: {humidity_in_context[:3]}")
                
                # Wind speed in context
                wind_in_context = re.findall(r'(\d+)\s*kt', context_html)
                if wind_in_context:
                    print(f"      💨 Wind speed in context: {wind_in_context[:3]}")
                
                # Weather condition in context
                weather_in_context = re.findall(r'class="weather-text"[^>]*>([^<>\n]+)</', context_html)
                if weather_in_context:
                    print(f"      🌤️  Weather in context: {weather_in_context}")
                
                # Wind direction in context
                wind_dir_in_context = re.findall(r'<span[^>]*>([^<>\n]+)</span>', context_html)
                wind_dir_filtered = [w for w in wind_dir_in_context if any(term in w.lower() for term in ['barat', 'timur', 'utara', 'selatan'])]
                if wind_dir_filtered:
                    print(f"      🧭 Wind direction in context: {wind_dir_filtered[:3]}")
            
        else:
            print(f"❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    focused_maritime_test() 