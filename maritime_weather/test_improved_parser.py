import json
import requests
from fetch_maritime_weather import parse_maritime_html

def test_improved_parser():
    """Test the improved maritime weather parser with a few areas"""
    
    # Test with a few maritime areas
    test_areas = [
        {
            'name': 'Perairan Aceh Utara - Aceh Timur',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur'
        },
        {
            'name': 'Perairan Banda Aceh',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-banda-aceh'
        },
        {
            'name': 'Perairan Medan',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-medan'
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"🧪 Testing Improved Maritime Weather Parser")
    print(f"=" * 50)
    
    for i, area in enumerate(test_areas, 1):
        print(f"\n[{i}/{len(test_areas)}] Testing: {area['name']}")
        print(f"🔗 URL: {area['url']}")
        
        try:
            response = requests.get(area['url'], headers=headers, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ HTTP 200 OK")
                
                # Parse the HTML
                weather_data = parse_maritime_html(response.text, area['name'])
                
                if weather_data:
                    print(f"✅ Data extracted successfully!")
                    print(f"📊 Extracted data:")
                    
                    # Show extracted fields
                    for key, value in weather_data.items():
                        if key not in ['area_name', 'source', 'parsed_at']:
                            print(f"   {key}: {value}")
                    
                    # Calculate extraction rate
                    expected_fields = ['temperature', 'humidity', 'wind_speed', 'wind_direction', 
                                     'wave_height', 'wave_classification', 'current_direction', 
                                     'current_speed', 'weather_condition', 'weather_icon']
                    
                    extracted_fields = [f for f in expected_fields if f in weather_data]
                    extraction_rate = len(extracted_fields) / len(expected_fields) * 100
                    
                    print(f"\n📈 Extraction Rate: {extraction_rate:.1f}%")
                    print(f"✅ Extracted: {extracted_fields}")
                    print(f"❌ Missing: {[f for f in expected_fields if f not in weather_data]}")
                    
                else:
                    print(f"❌ No data extracted")
                    
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print(f"-" * 50)

if __name__ == "__main__":
    test_improved_parser() 