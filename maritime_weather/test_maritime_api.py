import json
import requests
from datetime import datetime

def test_maritime_api():
    """Test the maritime weather API with sample areas"""
    
    # Test areas
    test_areas = [
        {
            'name': 'Perairan Aceh Utara - Aceh Timur',
            'slug': 'perairan-aceh-utara-aceh-timur',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur'
        },
        {
            'name': 'Perairan Sabang Banda Aceh',
            'slug': 'perairan-sabang-banda-aceh',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-sabang-banda-aceh'
        },
        {
            'name': 'Perairan Utara Serang',
            'slug': 'perairan-utara-serang',
            'url': 'https://maritim.bmkg.go.id/cuaca/perairan/perairan-utara-serang'
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    results = []
    
    for area in test_areas:
        print(f"🧪 Testing: {area['name']}")
        print(f"🔗 URL: {area['url']}")
        
        try:
            response = requests.get(area['url'], headers=headers, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ HTTP 200 OK")
                print(f"📄 Content-Type: {response.headers.get('content-type', 'Unknown')}")
                print(f"📏 Content Length: {len(response.text)} characters")
                
                # Check if it's HTML
                if 'text/html' in response.headers.get('content-type', ''):
                    print(f"🌐 HTML webpage detected")
                    
                    # Look for key weather data in HTML
                    html_content = response.text
                    
                    # Check for temperature
                    import re
                    temp_match = re.search(r'(\d+)°C', html_content)
                    if temp_match:
                        print(f"🌡️  Temperature found: {temp_match.group(1)}°C")
                    
                    # Check for wind speed
                    wind_match = re.search(r'(\d+)\s*kt', html_content)
                    if wind_match:
                        print(f"💨 Wind speed found: {wind_match.group(1)} kt")
                    
                    # Check for wind direction
                    wind_dir_match = re.search(r'Angin dari\s*([^<>\n]+)', html_content)
                    if wind_dir_match:
                        print(f"🧭 Wind direction found: {wind_dir_match.group(1).strip()}")
                    
                    # Check for wave height
                    wave_match = re.search(r'(\d+\.?\d*)\s*m', html_content)
                    if wave_match:
                        print(f"🌊 Wave height found: {wave_match.group(1)} m")
                    
                    results.append({
                        'area_name': area['name'],
                        'slug': area['slug'],
                        'url': area['url'],
                        'status': 'success',
                        'content_type': 'html',
                        'content_length': len(response.text),
                        'timestamp': datetime.now().isoformat()
                    })
                    
                else:
                    print(f"📊 Non-HTML content detected")
                    try:
                        data = response.json()
                        print(f"✅ JSON data parsed successfully")
                        print(f"📋 JSON keys: {list(data.keys())}")
                        
                        results.append({
                            'area_name': area['name'],
                            'slug': area['slug'],
                            'url': area['url'],
                            'status': 'success',
                            'content_type': 'json',
                            'data_keys': list(data.keys()),
                            'timestamp': datetime.now().isoformat()
                        })
                    except:
                        print(f"⚠️  Could not parse as JSON")
                        results.append({
                            'area_name': area['name'],
                            'slug': area['slug'],
                            'url': area['url'],
                            'status': 'failed',
                            'error': 'Could not parse content',
                            'timestamp': datetime.now().isoformat()
                        })
            else:
                print(f"❌ HTTP {response.status_code}")
                results.append({
                    'area_name': area['name'],
                    'slug': area['slug'],
                    'url': area['url'],
                    'status': 'failed',
                    'error': f"HTTP {response.status_code}",
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'area_name': area['name'],
                'slug': area['slug'],
                'url': area['url'],
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        print("-" * 50)
    
    # Save test results
    with open('maritime_api_test_results.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=2, ensure_ascii=False)
    
    print(f"📁 Test results saved to: maritime_api_test_results.json")
    
    # Summary
    successful = sum(1 for r in results if r['status'] == 'success')
    print(f"\n📊 Test Summary:")
    print(f"   ✅ Successful: {successful}/{len(test_areas)}")
    print(f"   ❌ Failed: {len(test_areas) - successful}/{len(test_areas)}")

if __name__ == "__main__":
    test_maritime_api() 