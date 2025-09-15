import json
import re
import requests

def extract_maritime_slugs():
    """Extract maritime weather slugs from perairan.json"""
    
    try:
        # Load the perairan data
        with open('perairan.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        maritime_areas = []
        
        # Parse the complex structure to find maritime areas
        for i, item in enumerate(data):
            if isinstance(item, str) and 'Perairan' in item:
                # Extract the maritime area name
                area_name = item
                
                # Create slug from the area name
                slug = create_maritime_slug(area_name)
                
                maritime_areas.append({
                    'name': area_name,
                    'slug': slug,
                    'url': f"https://maritim.bmkg.go.id/cuaca/perairan/{slug}"
                })
        
        print(f"🌊 Found {len(maritime_areas)} maritime areas")
        
        # Save to file
        with open('maritime_areas.json', 'w', encoding='utf-8') as file:
            json.dump(maritime_areas, file, indent=2, ensure_ascii=False)
        
        print(f"📁 Maritime areas saved to: maritime_areas.json")
        
        # Show sample areas
        print(f"\n📋 Sample maritime areas:")
        for area in maritime_areas[:10]:
            print(f"  🌊 {area['name']}")
            print(f"     Slug: {area['slug']}")
            print(f"     URL: {area['url']}")
            print()
        
        if len(maritime_areas) > 10:
            print(f"  ... and {len(maritime_areas) - 10} more areas")
            
        return maritime_areas
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def create_maritime_slug(area_name):
    """Convert maritime area name to slug format"""
    # Remove "Perairan" prefix and clean the name
    clean_name = area_name.replace('Perairan', '').strip()
    
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^a-zA-Z0-9\s]', ' ', clean_name)
    slug = re.sub(r'\s+', '-', slug.strip()).lower()
    
    # Add "perairan-" prefix to match BMKG format
    return f"perairan-{slug}"

def test_maritime_api():
    """Test the maritime weather API with a sample slug"""
    
    # Test with the known working slug
    test_slug = "perairan-aceh-utara-aceh-timur"
    test_url = f"https://maritim.bmkg.go.id/cuaca/perairan/{test_slug}"
    
    print(f"🧪 Testing maritime API...")
    print(f"URL: {test_url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(test_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ API test successful!")
            print(f"📄 Content length: {len(response.text)} characters")
            
            # Check if it's HTML (webpage) or JSON (API)
            if response.headers.get('content-type', '').startswith('application/json'):
                print(f"📊 Response type: JSON API")
                try:
                    data = response.json()
                    print(f"📋 JSON keys: {list(data.keys())}")
                except:
                    print(f"⚠️  Could not parse JSON")
            else:
                print(f"🌐 Response type: HTML webpage")
                
        else:
            print(f"❌ API test failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test error: {e}")

def main():
    """Main function"""
    print("🌊 Maritime Weather Slug Extractor")
    print("=" * 50)
    
    # Extract maritime slugs
    maritime_areas = extract_maritime_slugs()
    
    if maritime_areas:
        print(f"\n🧪 Testing API with sample slug...")
        test_maritime_api()
        
        print(f"\n📊 Summary:")
        print(f"   🌊 Total maritime areas: {len(maritime_areas)}")
        print(f"   📁 Data saved to: maritime_areas.json")
        print(f"   🔗 URL format: https://maritim.bmkg.go.id/cuaca/perairan/[slug]")

if __name__ == "__main__":
    main() 