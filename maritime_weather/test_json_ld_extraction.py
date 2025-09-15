import requests
import re
import json

def test_json_ld_extraction():
    """Test JSON-LD structured data extraction from BMKG maritime pages"""
    
    # Test with the area that showed JSON-LD data
    test_url = "https://maritim.bmkg.go.id/cuaca/perairan/perairan-sabang-banda-aceh"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"🧪 Testing JSON-LD Structured Data Extraction")
        print(f"🔗 URL: {test_url}")
        
        response = requests.get(test_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            html_content = response.text
            
            print(f"\n🔍 JSON-LD Extraction Results:")
            
            # Look for JSON-LD scripts
            json_ld_matches = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html_content, re.DOTALL)
            
            if json_ld_matches:
                print(f"✅ Found {len(json_ld_matches)} JSON-LD script(s)")
                
                for i, json_ld in enumerate(json_ld_matches, 1):
                    print(f"\n📄 JSON-LD Script {i}:")
                    print(f"   Raw content: {json_ld.strip()[:200]}...")
                    
                    try:
                        json_data = json.loads(json_ld.strip())
                        print(f"   ✅ Valid JSON parsed")
                        
                        # Extract structured data
                        if json_data.get('@type') == 'WeatherForecast':
                            print(f"   🌤️  Weather Forecast Data:")
                            print(f"      Name: {json_data.get('name', 'N/A')}")
                            print(f"      Provider: {json_data.get('provider', {}).get('name', 'N/A')}")
                            print(f"      Valid From: {json_data.get('validFrom', 'N/A')}")
                            print(f"      Valid To: {json_data.get('validTo', 'N/A')}")
                            print(f"      Date Issued: {json_data.get('dateIssued', 'N/A')}")
                            print(f"      Location: {json_data.get('location', {}).get('name', 'N/A')}")
                        else:
                            print(f"   ❌ Not a WeatherForecast type: {json_data.get('@type', 'Unknown')}")
                            
                    except json.JSONDecodeError as e:
                        print(f"   ❌ Invalid JSON: {e}")
                        
            else:
                print(f"❌ No JSON-LD scripts found")
            
            # Also test the parser function
            print(f"\n🧪 Testing Parser Function:")
            from fetch_maritime_weather import parse_maritime_html
            
            weather_data = parse_maritime_html(html_content, "Perairan Sabang Banda Aceh")
            
            if weather_data and 'structured_data' in weather_data:
                print(f"✅ Structured data extracted by parser:")
                for key, value in weather_data['structured_data'].items():
                    print(f"   {key}: {value}")
            else:
                print(f"❌ No structured data extracted by parser")
                
        else:
            print(f"❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_json_ld_extraction() 