import json
import requests
import time
from datetime import datetime

def fetch_maritime_weather_data():
    """Fetch weather data from BMKG maritime areas"""
    
    try:
        # Load maritime areas
        with open('maritime_areas.json', 'r', encoding='utf-8') as file:
            maritime_areas = json.load(file)
        
        print(f"🌊 Starting to fetch weather data for {len(maritime_areas)} maritime areas")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = []
        successful = 0
        failed = 0
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for i, area in enumerate(maritime_areas, 1):
            print(f"[{i:3d}/{len(maritime_areas)}] Fetching: {area['name']}")
            
            try:
                response = requests.get(area['url'], headers=headers, timeout=30)
                
                if response.status_code == 200:
                    # Check if it's HTML content (webpage)
                    if 'text/html' in response.headers.get('content-type', ''):
                        # This is a webpage, we need to extract data from HTML
                        weather_data = parse_maritime_html(response.text, area['name'])
                        
                        if weather_data:
                            results.append({
                                'area_name': area['name'],
                                'slug': area['slug'],
                                'url': area['url'],
                                'weather_data': weather_data,
                                'status': 'success',
                                'timestamp': datetime.now().isoformat()
                            })
                            successful += 1
                            print(f"    ✅ Success - HTML data extracted")
                        else:
                            results.append({
                                'area_name': area['name'],
                                'slug': area['slug'],
                                'url': area['url'],
                                'weather_data': None,
                                'status': 'failed',
                                'error': 'No weather data found in HTML',
                                'timestamp': datetime.now().isoformat()
                            })
                            failed += 1
                            print(f"    ❌ Failed - No data in HTML")
                    else:
                        # Try to parse as JSON
                        try:
                            weather_data = response.json()
                            results.append({
                                'area_name': area['name'],
                                'slug': area['slug'],
                                'url': area['url'],
                                'weather_data': weather_data,
                                'status': 'success',
                                'timestamp': datetime.now().isoformat()
                            })
                            successful += 1
                            print(f"    ✅ Success - JSON data")
                        except:
                            results.append({
                                'area_name': area['name'],
                                'slug': area['slug'],
                                'url': area['url'],
                                'weather_data': None,
                                'status': 'failed',
                                'error': 'Invalid JSON response',
                                'timestamp': datetime.now().isoformat()
                            })
                            failed += 1
                            print(f"    ❌ Failed - Invalid JSON")
                else:
                    results.append({
                        'area_name': area['name'],
                        'slug': area['slug'],
                        'url': area['url'],
                        'weather_data': None,
                        'status': 'failed',
                        'error': f"HTTP {response.status_code}",
                        'timestamp': datetime.now().isoformat()
                    })
                    failed += 1
                    print(f"    ❌ Failed - HTTP {response.status_code}")
                    
            except Exception as e:
                results.append({
                    'area_name': area['name'],
                    'slug': area['slug'],
                    'url': area['url'],
                    'weather_data': None,
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                failed += 1
                print(f"    ❌ Error: {e}")
            
            # Progress update every 20 areas
            if i % 20 == 0:
                print(f"\n📈 Progress: {i}/{len(maritime_areas)} ({i/len(maritime_areas)*100:.1f}%)")
                print(f"   ✅ Successful: {successful}, ❌ Failed: {failed}\n")
            
            # Add delay to avoid overwhelming the server
            time.sleep(1)
        
        # Save results
        filename = "maritime_weather_data.json"
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2, ensure_ascii=False)
        
        # Final summary
        print(f"\n" + "=" * 50)
        print(f"🎯 MARITIME WEATHER DATA COLLECTION COMPLETE")
        print(f"=" * 50)
        print(f"📊 Total areas processed: {len(maritime_areas)}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success rate: {successful/len(maritime_areas)*100:.1f}%")
        print(f"💾 Results saved to: {filename}")
        print(f"📁 File size: {len(json.dumps(results))/1024/1024:.1f} MB")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def parse_maritime_html(html_content, area_name):
    """Parse weather data from BMKG maritime HTML page"""
    
    try:
        # Look for weather data in the HTML
        # Enhanced parser based on actual HTML structure analysis
        
        weather_data = {
            'area_name': area_name,
            'source': 'BMKG Maritime HTML',
            'parsed_at': datetime.now().isoformat()
        }
        
        # Extract current weather info (comprehensive pattern matching)
        import re
        
        # Enhanced temperature extraction - look for multiple patterns
        temp_patterns = [
            r'(\d+)°C',  # Standard degree format
            r'(\d+)\s*C',  # C without degree symbol
            r'(\d+)\s*Celcius',  # Full word
            r'(\d+)\s*derajat'  # Indonesian word
        ]
        
        for pattern in temp_patterns:
            temp_match = re.search(pattern, html_content, re.IGNORECASE)
            if temp_match:
                weather_data['temperature'] = temp_match.group(1)
                break
        
        # Enhanced humidity extraction - look for multiple patterns
        humidity_patterns = [
            r'(\d+)%',  # Standard percentage
            r'Kelembaban[:\s]*(\d+)',  # Indonesian label
            r'Humidity[:\s]*(\d+)',  # English label
            r'RH[:\s]*(\d+)'  # Abbreviation
        ]
        
        for pattern in humidity_patterns:
            humidity_matches = re.findall(pattern, html_content, re.IGNORECASE)
            if humidity_matches:
                # Filter out unrealistic values (like 333333, 666667)
                valid_humidity = [h for h in humidity_matches if int(h) <= 100]
                if valid_humidity:
                    weather_data['humidity'] = valid_humidity[0]
                    break
        
        # Enhanced wind speed extraction
        wind_patterns = [
            r'(\d+)\s*kt',  # Knots
            r'(\d+)\s*knot',  # Full word
            r'(\d+)\s*km/h',  # Kilometers per hour
            r'(\d+)\s*m/s',  # Meters per second
            r'Kecepatan[:\s]*(\d+)',  # Indonesian label
            r'Wind[:\s]*(\d+)'  # English label
        ]
        
        for pattern in wind_patterns:
            wind_matches = re.findall(pattern, html_content, re.IGNORECASE)
            if wind_matches:
                # Filter out unrealistic values
                valid_wind = [w for w in wind_matches if int(w) <= 100]
                if valid_wind:
                    weather_data['wind_speed'] = valid_wind[0]
                    break
        
        # Enhanced gust wind speed extraction
        gust_patterns = [
            r'Gust[:\s]*(\d+)',  # English
            r'Angin[:\s]*Puncak[:\s]*(\d+)',  # Indonesian
            r'Puncak[:\s]*(\d+)',  # Short Indonesian
            r'(\d+)\s*kt.*gust',  # Pattern with gust
            r'gust.*(\d+)\s*kt'  # Gust with pattern
        ]
        
        for pattern in gust_patterns:
            gust_match = re.search(pattern, html_content, re.IGNORECASE)
            if gust_match:
                weather_data['wind_gust'] = gust_match.group(1)
                break
        
        # Enhanced wind direction extraction - more comprehensive
        direction_keywords = [
            'barat', 'timur', 'utara', 'selatan', 'tenggara', 'barat daya', 
            'barat laut', 'timur laut', 'utara timur', 'selatan barat',
            'west', 'east', 'north', 'south', 'southeast', 'southwest', 
            'northwest', 'northeast'
        ]
        
        # Look for wind direction in specific CSS classes first
        wind_dir_patterns = [
            r'class="[^"]*wind[^"]*"[^>]*>([^<>\n]+)</',  # Wind-specific class
            r'class="[^"]*direction[^"]*"[^>]*>([^<>\n]+)</',  # Direction class
            r'<span[^>]*class="[^"]*text-[^"]*"[^>]*>([^<>\n]+)</span>',  # Text classes
            r'<td[^>]*class="[^"]*text-center[^"]*"[^>]*>([^<>\n]+)</td>',  # Center-aligned cells
            # Look for wind direction in table headers and adjacent cells
            r'<th[^>]*>.*?[Aa]ngin.*?[Dd]ari.*?</th>.*?<td[^>]*>([^<>\n]+)</td>',  # Wind direction header + cell
            r'<th[^>]*>.*?[Ww]ind.*?[Dd]irection.*?</th>.*?<td[^>]*>([^<>\n]+)</td>',  # English wind direction
            r'[Aa]ngin[:\s]*[Dd]ari[:\s]*([^<>\n]+)',  # Indonesian wind direction label
            r'[Ww]ind[:\s]*[Dd]irection[:\s]*([^<>\n]+)',  # English wind direction label
        ]
        
        wind_direction_found = False
        for pattern in wind_dir_patterns:
            wind_dir_matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
            for match in wind_dir_matches:
                cell_text = match.strip()
                # Enhanced filtering to avoid area names and invalid data
                if (any(term in cell_text.lower() for term in direction_keywords) and 
                    not any(term in cell_text.lower() for term in ['perairan', 'aceh', 'medan', 'banda', 'provinsi', 'kota', 'kabupaten']) and
                    len(cell_text) < 30 and  # Avoid very long text
                    not cell_text.startswith('/') and  # Avoid URL fragments
                    not 'class=' in cell_text and  # Avoid HTML attributes
                    not 'href=' in cell_text):  # Avoid link fragments
                    weather_data['wind_direction'] = cell_text
                    wind_direction_found = True
                    break
            if wind_direction_found:
                break
        
        # Enhanced current direction extraction
        current_dir_patterns = [
            r'class="[^"]*current[^"]*"[^>]*>([^<>\n]+)</',  # Current-specific class
            r'Arus[:\s]*([^<>\n]+)',  # Indonesian label
            r'Current[:\s]*([^<>\n]+)',  # English label
            # Look for current direction in table headers and adjacent cells
            r'<th[^>]*>.*?[Aa]rus.*?[Dd]ari.*?</th>.*?<td[^>]*>([^<>\n]+)</td>',  # Current direction header + cell
            r'<th[^>]*>.*?[Cc]urrent.*?[Dd]irection.*?</th>.*?<td[^>]*>([^<>\n]+)</td>',  # English current direction
            r'[Aa]rus[:\s]*[Dd]ari[:\s]*([^<>\n]+)',  # Indonesian current direction label
            r'[Cc]urrent[:\s]*[Dd]irection[:\s]*([^<>\n]+)',  # English current direction label
        ]
        
        current_direction_found = False
        for pattern in current_dir_patterns:
            current_dir_matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
            for match in current_dir_matches:
                cell_text = match.strip()
                # Enhanced filtering to avoid area names and invalid data
                if (any(term in cell_text.lower() for term in direction_keywords) and 
                    not any(term in cell_text.lower() for term in ['perairan', 'aceh', 'medan', 'banda', 'provinsi', 'kota', 'kabupaten']) and
                    len(cell_text) < 30 and  # Avoid very long text
                    not cell_text.startswith('/') and  # Avoid URL fragments
                    not 'class=' in cell_text and  # Avoid HTML attributes
                    not 'href=' in cell_text):  # Avoid link fragments
                    weather_data['current_direction'] = cell_text
                    current_direction_found = True
                    break
            if current_direction_found:
                break
        
        # Enhanced wave height extraction
        wave_patterns = [
            r'(\d+\.?\d*)\s*m',  # Meters
            r'(\d+\.?\d*)\s*meter',  # Full word
            r'Tinggi[:\s]*Gelombang[:\s]*(\d+\.?\d*)',  # Indonesian label
            r'Wave[:\s]*Height[:\s]*(\d+\.?\d*)'  # English label
        ]
        
        for pattern in wave_patterns:
            wave_matches = re.findall(pattern, html_content, re.IGNORECASE)
            if wave_matches:
                # Filter out unrealistic values
                valid_waves = [w for w in wave_matches if float(w) <= 20]
                if valid_waves:
                    weather_data['wave_height'] = valid_waves[0]
                    break
        
        # Enhanced wave classification extraction
        wave_class_patterns = [
            r'class="[^"]*wave[^"]*"[^>]*>([^<>\n]+)</',  # Wave-specific class
            r'<span[^>]*class="[^"]*text-[^"]*"[^>]*>([^<>\n]+)</span>',  # Text classes
            r'<td[^>]*class="[^"]*text-center[^"]*"[^>]*>([^<>\n]+)</td>'  # Center-aligned cells
        ]
        
        wave_class_keywords = ['sedang', 'rendah', 'tinggi', 'sangat tinggi', 'moderate', 'low', 'high', 'very high']
        
        wave_class_found = False
        for pattern in wave_class_patterns:
            wave_class_matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in wave_class_matches:
                cell_text = match.strip()
                if any(term in cell_text.lower() for term in wave_class_keywords):
                    weather_data['wave_classification'] = cell_text
                    wave_class_found = True
                    break
            if wave_class_found:
                break
        
        # Enhanced current speed extraction
        current_speed_patterns = [
            r'(\d+\.?\d*)\s*cm/s',  # Centimeters per second
            r'(\d+\.?\d*)\s*m/s',  # Meters per second
            r'(\d+\.?\d*)\s*knot',  # Knots
            r'Kecepatan[:\s]*Arus[:\s]*(\d+\.?\d*)',  # Indonesian label
            r'Current[:\s]*Speed[:\s]*(\d+\.?\d*)'  # English label
        ]
        
        for pattern in current_speed_patterns:
            current_matches = re.findall(pattern, html_content, re.IGNORECASE)
            if current_matches:
                # Filter out unrealistic values
                valid_currents = [c for c in current_matches if float(c) <= 200]
                if valid_currents:
                    weather_data['current_speed'] = valid_currents[0]
                    break
        
        # Enhanced weather condition extraction
        weather_patterns = [
            r'class="weather-text"[^>]*>([^<>\n]+)</',  # Weather text class
            r'class="[^"]*weather[^"]*"[^>]*>([^<>\n]+)</',  # Weather class
            r'class="[^"]*condition[^"]*"[^>]*>([^<>\n]+)</',  # Condition class
            r'<span[^>]*class="[^"]*text-[^"]*"[^>]*>([^<>\n]+)</span>',  # Text classes
            r'Cuaca[:\s]*([^<>\n]+)',  # Indonesian label
            r'Weather[:\s]*([^<>\n]+)'  # English label
        ]
        
        weather_condition_found = False
        for pattern in weather_patterns:
            weather_matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in weather_matches:
                cell_text = match.strip()
                # Filter out HTML fragments and invalid data
                if (any(term in cell_text.lower() for term in ['hujan', 'berawan', 'cerah', 'mendung', 'rain', 'cloudy', 'clear', 'overcast']) and 
                    len(cell_text) < 50 and  # Avoid very long text
                    not cell_text.startswith('/') and  # Avoid URL fragments
                    not 'class=' in cell_text and  # Avoid HTML attributes
                    not 'href=' in cell_text):  # Avoid link fragments
                    weather_data['weather_condition'] = cell_text
                    weather_condition_found = True
                    break
            if weather_condition_found:
                break
        
        # Enhanced time information extraction with better validation
        time_patterns = [
            r'(\d{1,2}\s+Agu\s+\d{2},\s+\d{2}\.\d{2})',  # Specific format
            r'(\d{1,2}\s+[A-Za-z]+\s+\d{2},\s+\d{2}\.\d{2})',  # General format
            r'(\d{2}\.\d{2})',  # Time only (but validate it's reasonable)
            r'(\d{1,2}:\d{2})',  # HH:MM format
            r'Waktu[:\s]*([^<>\n]+)',  # Indonesian label
            r'Time[:\s]*([^<>\n]+)'  # English label
        ]
        
        for pattern in time_patterns:
            time_matches = re.findall(pattern, html_content, re.IGNORECASE)
            if time_matches:
                time_value = time_matches[0]
                # Validate time format - avoid extracting numbers that aren't times
                if pattern in [r'(\d{2}\.\d{2})', r'(\d{1,2}:\d{2})']:
                    # For time-only patterns, validate it's a reasonable time
                    if '.' in time_value:
                        parts = time_value.split('.')
                        if len(parts) == 2 and len(parts[0]) <= 2 and len(parts[1]) <= 2:
                            if 0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59:
                                weather_data['time'] = time_value
                                break
                    elif ':' in time_value:
                        parts = time_value.split(':')
                        if len(parts) == 2 and len(parts[0]) <= 2 and len(parts[1]) <= 2:
                            if 0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59:
                                weather_data['time'] = time_value
                                break
                else:
                    # For other patterns, use directly
                    weather_data['time'] = time_value
                    break
        
        # Enhanced current time detection
        current_time_patterns = [
            r'Saat ini',  # Indonesian
            r'Current',  # English
            r'Now',  # English
            r'(\d{1,2}\s+[A-Za-z]+\s+\d{2},\s+\d{2}\.\d{2})',  # Full date time
        ]
        
        for pattern in current_time_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                weather_data['is_current'] = True
                break
        
        # Enhanced weather icon extraction
        icon_patterns = [
            r'src="([^"]*\.svg)"',  # SVG files
            r'src="([^"]*\.png)"',  # PNG files
            r'src="([^"]*\.jpg)"',  # JPG files
            r'class="[^"]*icon[^"]*"[^>]*src="([^"]*)"',  # Icon class with src
        ]
        
        for pattern in icon_patterns:
            icon_matches = re.findall(pattern, html_content, re.IGNORECASE)
            if icon_matches:
                weather_data['weather_icon'] = icon_matches[0]
                break
        
        # Extract JSON-LD structured data if available
        json_ld_matches = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html_content, re.DOTALL)
        if json_ld_matches:
            try:
                for json_ld in json_ld_matches:
                    json_data = json.loads(json_ld.strip())
                    if json_data.get('@type') == 'WeatherForecast':
                        weather_data['structured_data'] = {
                            'forecast_name': json_data.get('name', ''),
                            'provider': json_data.get('provider', {}).get('name', ''),
                            'valid_from': json_data.get('validFrom', ''),
                            'valid_to': json_data.get('validTo', ''),
                            'date_issued': json_data.get('dateIssued', ''),
                            'location': json_data.get('location', {}).get('name', '')
                        }
                        break
            except json.JSONDecodeError:
                pass  # Skip invalid JSON
        
        # Extract wind direction and current direction from JavaScript data
        # These are often embedded in JavaScript variables rather than HTML
        if 'wind_direction' not in weather_data:
            js_wind_patterns = [
                r'["\']([^"\']*(?:Tenggara|Barat Laut|Barat Daya|Timur Laut|Barat|Timur|Utara|Selatan)[^"\']*)["\']\s*,\s*\d+\s*kt',  # Direction + speed
                r'wind_from["\']?\s*:\s*["\']?([^"\']*(?:Tenggara|Barat Laut|Barat Daya|Timur Laut|Barat|Timur|Utara|Selatan)[^"\']*)["\']?',  # wind_from field
                r'["\']([^"\']*(?:Tenggara|Barat Laut|Barat Daya|Timur Laut|Barat|Timur|Utara|Selatan)[^"\']*)["\']',  # Just direction
            ]
            
            for pattern in js_wind_patterns:
                js_wind_matches = re.findall(pattern, html_content, re.IGNORECASE)
                if js_wind_matches:
                    # Filter out area names and get the first valid direction
                    for match in js_wind_matches:
                        clean_match = re.sub(r'<[^>]+>', '', match).strip()  # Remove HTML tags
                        if (not any(term in clean_match.lower() for term in ['perairan', 'aceh', 'medan', 'banda', 'provinsi', 'kota', 'kabupaten']) and
                            len(clean_match) < 30 and  # Avoid very long text
                            not clean_match.startswith('data-') and  # Avoid data attributes
                            not 'class=' in clean_match):  # Avoid HTML attributes
                            weather_data['wind_direction'] = clean_match
                            break
                    if 'wind_direction' in weather_data:
                        break
        
        if 'current_direction' not in weather_data:
            js_current_patterns = [
                r'current_to["\']?\s*:\s*["\']?([^"\']*(?:Barat|Timur|Utara|Selatan)[^"\']*)["\']?',  # current_to field
                r'["\']([^"\']*(?:Barat|Timur|Utara|Selatan)[^"\']*)["\']',  # Just direction
            ]
            
            for pattern in js_current_patterns:
                js_current_matches = re.findall(pattern, html_content, re.IGNORECASE)
                if js_current_matches:
                    # Filter out area names and get the first valid direction
                    for match in js_current_matches:
                        clean_match = re.sub(r'<[^>]+>', '', match).strip()  # Remove HTML tags
                        if (not any(term in clean_match.lower() for term in ['perairan', 'aceh', 'medan', 'banda', 'provinsi', 'kota', 'kabupaten']) and
                            len(clean_match) < 30 and  # Avoid very long text
                            not clean_match.startswith('data-') and  # Avoid data attributes
                            not 'class=' in clean_match):  # Avoid HTML attributes
                            weather_data['current_direction'] = clean_match
                            break
                    if 'current_direction' in weather_data:
                        break
        
        # Enhanced fallback extraction for areas with different HTML structures
        # Look for data in table cells with specific CSS classes
        table_cell_patterns = [
            r'<td[^>]*class="[^"]*text-center[^"]*"[^>]*>([^<>\n]+)</td>',  # Center-aligned cells
            r'<td[^>]*class="[^"]*text-left[^"]*"[^>]*>([^<>\n]+)</td>',   # Left-aligned cells
            r'<td[^>]*class="[^"]*text-right[^"]*"[^>]*>([^<>\n]+)</td>',  # Right-aligned cells
            r'<td[^>]*>([^<>\n]+)</td>',  # Any table cell
        ]
        
        # Extract missing data from table cells
        for pattern in table_cell_patterns:
            table_cells = re.findall(pattern, html_content, re.IGNORECASE)
            
            # Extract wind direction if not found above
            if 'wind_direction' not in weather_data:
                for cell in table_cells:
                    cell_text = cell.strip()
                    if any(term in cell_text.lower() for term in direction_keywords) and not any(term in cell_text.lower() for term in ['perairan', 'aceh', 'medan', 'banda', 'provinsi']):
                        weather_data['wind_direction'] = cell_text
                        break
            
            # Extract current direction if not found above
            if 'current_direction' not in weather_data:
                for cell in table_cells:
                    cell_text = cell.strip()
                    if any(term in cell_text.lower() for term in direction_keywords) and not any(term in cell_text.lower() for term in ['perairan', 'aceh', 'medan', 'banda', 'provinsi']):
                        weather_data['current_direction'] = cell_text
                        break
            
            # Extract wave classification if not found above
            if 'wave_classification' not in weather_data:
                for cell in table_cells:
                    cell_text = cell.strip()
                    if any(term in cell_text.lower() for term in wave_class_keywords):
                        weather_data['wave_classification'] = cell_text
                        break
            
            # Extract weather condition if not found above
            if 'weather_condition' not in weather_data:
                for cell in table_cells:
                    cell_text = cell.strip()
                    if any(term in cell_text.lower() for term in ['hujan', 'berawan', 'cerah', 'mendung', 'rain', 'cloudy', 'clear', 'overcast']):
                        weather_data['weather_condition'] = cell_text
                        break
        
        # If we found any data, return it
        if len(weather_data) > 3:  # More than just area_name, source, and parsed_at
            return weather_data
        else:
            return None
            
    except Exception as e:
        print(f"⚠️  HTML parsing error for {area_name}: {e}")
        return None

def main():
    """Main function"""
    print("🌊 BMKG Maritime Weather Data Fetcher")
    print("=" * 50)
    
    results = fetch_maritime_weather_data()
    
    if results:
        # Show sample of successful data
        successful_data = [r for r in results if r['status'] == 'success']
        if successful_data:
            print(f"\n📋 Sample successful data:")
            sample = successful_data[0]
            print(f"  🌊 {sample['area_name']}")
            if sample['weather_data']:
                for key, value in sample['weather_data'].items():
                    if key not in ['area_name', 'source', 'parsed_at']:
                        print(f"     {key}: {value}")

if __name__ == "__main__":
    main() 