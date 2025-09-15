import json
import re
import requests
import os

def load_pelabuhan_data(file_path="pelabuhan.json"):
    """Load port data from pelabuhan.json"""
    try:
        # Try to find the file in multiple possible locations
        possible_paths = [
            "pelabuhan.json",  # If running from pelabuhan folder
            "pelabuhan/pelabuhan.json",  # If running from root directory
            os.path.join(os.path.dirname(__file__), "pelabuhan.json")  # Absolute path
        ]
        
        data = None
        used_path = None
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    used_path = path
                    break
        
        if data is None:
            print(f"Error: Could not find pelabuhan.json in any of these locations:")
            for path in possible_paths:
                print(f"  - {path}")
            return []
        
        print(f"Loaded data from: {used_path}")
        
        ports = []
        
        # The structure has sequential elements: ID, Port Name, Lat, Lon, {object}
        # We need to find "Pelabuhan" strings and get the next two elements as coordinates
        for i, item in enumerate(data):
            if isinstance(item, str) and 'Pelabuhan' in item:
                # Check if we have enough elements after this for coordinates
                if i + 2 < len(data):
                    lat = data[i + 1]
                    lon = data[i + 2]
                    
                    # Verify these are numbers
                    if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                        ports.append({
                            'id': f"PORT_{len(ports)+1:03d}",
                            'name': item,
                            'lat': lat,
                            'lon': lon
                        })
        
        print(f"Found {len(ports)} ports")
        return ports
    except Exception as e:
        print(f"Error: {e}")
        return []

def create_slug(port_name):
    """Convert port name to slug for BMKG API"""
    # Convert to lowercase and replace non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-zA-Z0-9\s]', ' ', port_name)
    slug = re.sub(r'\s+', '-', slug.strip()).lower()
    return slug

def fetch_port_weather(port_name, port_lat, port_lon):
    """Fetch weather data for a port"""
    try:
        slug = create_slug(port_name)
        api_url = f"https://maritim.bmkg.go.id/api/pelabuhan?slug={slug}"
        
        print(f"Fetching: {port_name} -> {slug}")
        
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            weather_data = response.json()
            return {
                'port_name': port_name,
                'slug': slug,
                'coordinates': {'lat': port_lat, 'lon': port_lon},
                'weather_data': weather_data,
                'status': 'success'
            }
        else:
            return {
                'port_name': port_name,
                'slug': slug,
                'coordinates': {'lat': port_lat, 'lon': port_lon},
                'weather_data': None,
                'status': 'failed',
                'error': f"HTTP {response.status_code}"
            }
            
    except Exception as e:
        return {
            'port_name': port_name,
            'slug': create_slug(port_name),
            'coordinates': {'lat': port_lat, 'lon': port_lon},
            'weather_data': None,
            'status': 'error',
            'error': str(e)
        }

def main():
    print("Port Weather Data Fetcher")
    print("=" * 50)
    
    ports = load_pelabuhan_data()
    if not ports:
        print("No ports found. Exiting.")
        return
    
    print(f"Found {len(ports)} ports to process")
    print("Estimated time: ~5-6 minutes (with 500ms delays)")
    print("Starting data collection...\n")
    
    results = []
    successful = 0
    failed = 0
    
    # Process all ports
    for i, port in enumerate(ports, 1):
        print(f"[{i:3d}/{len(ports)}] Processing: {port['name']}")
        
        result = fetch_port_weather(port['name'], port['lat'], port['lon'])
        results.append(result)
        
        if result['status'] == 'success':
            successful += 1
            print(f"    Success")
        else:
            failed += 1
            print(f"    Failed: {result.get('error', 'Unknown error')}")
        
        # Progress update every 50 ports
        if i % 50 == 0:
            print(f"\nProgress: {i}/{len(ports)} ({i/len(ports)*100:.1f}%)")
            print(f"   Successful: {successful}, Failed: {failed}\n")
        
        # Add delay to avoid overwhelming BMKG API
        import time
        time.sleep(0.5)  # 500ms delay between requests
    
    # Final summary
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    print(f"Total ports processed: {len(ports)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {successful/len(ports)*100:.1f}%")
    
    # Save results
    filename = "pelabuhan_weather_data.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {filename}")
    print(f"File size: {len(json.dumps(results))/1024/1024:.1f} MB")
    
    if successful > 0:
        print(f"\nReady to integrate {successful} ports into your weather map!")
    else:
        print(f"\nNo successful data collected. Check your internet connection and API status.")

if __name__ == "__main__":
    main() 