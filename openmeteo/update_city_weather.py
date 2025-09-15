#!/usr/bin/env python3
"""
City Weather Update Script
Updates city weather data using OpenMeteo API
Run this script periodically to keep city weather data current
"""

import json
import time
import logging
from datetime import datetime
import os
import sys

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import openmeteo_requests
import requests_cache
from retry_requests import retry

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../city_weather_update.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_city_coordinates():
    """Load city coordinates from namaKota.json"""
    try:
        with open('namaKota.json', 'r', encoding='utf-8') as file:
            city_data = json.load(file)
        
        cities = []
        for city_name, data in city_data.items():
            cities.append({
                'name': city_name,
                'lat': data['latitude'],
                'lon': data['longitude']
            })
        
        logging.info(f"Loaded {len(cities)} cities from namaKota.json")
        return cities
    except Exception as e:
        logging.error(f"Error loading city coordinates: {e}")
        return []

def setup_openmeteo_client():
    """Setup OpenMeteo client with caching and retry mechanism"""
    # Setup cache session (1 hour cache)
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    return openmeteo

def fetch_city_weather_data(openmeteo_client, cities):
    """Fetch weather data for cities using OpenMeteo client"""
    if not cities:
        return []
    
    # Prepare coordinates for API call
    lats = [city['lat'] for city in cities]
    lons = [city['lon'] for city in cities]
    
    # API parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lats,
        "longitude": lons,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m", "wind_direction_10m"],
        "timezone": "Asia/Jakarta"
    }
    
    try:
        logging.info(f"Fetching weather data for {len(cities)} cities...")
        responses = openmeteo_client.weather_api(url, params=params)
        
        processed_data = []
        
        for i, response in enumerate(responses):
            if i < len(cities):
                city = cities[i]
                
                # Get current weather data
                current = response.Current()
                
                # Extract current weather variables using positional access
                current_vars = {}
                
                if current.VariablesLength() > 0:
                    # temperature_2m (first variable)
                    if current.VariablesLength() > 0:
                        temp_var = current.Variables(0)
                        current_vars['temperature_2m'] = temp_var.Value()
                    
                    # relative_humidity_2m (second variable)
                    if current.VariablesLength() > 1:
                        humidity_var = current.Variables(1)
                        current_vars['relative_humidity_2m'] = humidity_var.Value()
                    
                    # weather_code (third variable)
                    if current.VariablesLength() > 2:
                        weather_var = current.Variables(2)
                        current_vars['weather_code'] = weather_var.Value()
                    
                    # wind_speed_10m (fourth variable)
                    if current.VariablesLength() > 3:
                        wind_speed_var = current.Variables(3)
                        current_vars['wind_speed_10m'] = wind_speed_var.Value()
                    
                    # wind_direction_10m (fifth variable)
                    if current.VariablesLength() > 4:
                        wind_dir_var = current.Variables(4)
                        current_vars['wind_direction_10m'] = wind_dir_var.Value()
                
                processed_city = {
                    'name': city['name'],
                    'lat': city['lat'],
                    'lon': city['lon'],
                    'coordinates': {
                        'latitude': float(response.Latitude()),
                        'longitude': float(response.Longitude()),
                        'elevation': float(response.Elevation())
                    },
                    'weather_data': {
                        'temperature_2m': float(current_vars.get('temperature_2m')) if current_vars.get('temperature_2m') is not None else None,
                        'relative_humidity_2m': float(current_vars.get('relative_humidity_2m')) if current_vars.get('relative_humidity_2m') is not None else None,
                        'weather_code': int(current_vars.get('weather_code')) if current_vars.get('weather_code') is not None else None,
                        'wind_speed_10m': float(current_vars.get('wind_speed_10m')) if current_vars.get('wind_speed_10m') is not None else None,
                        'wind_direction_10m': float(current_vars.get('wind_direction_10m')) if current_vars.get('wind_direction_10m') is not None else None,
                        'timestamp': int(current.Time()) if current.Time() is not None else None,
                        'timezone': str(response.Timezone()).replace("b'", "").replace("'", "") if response.Timezone() is not None else None,
                        'utc_offset_seconds': int(response.UtcOffsetSeconds()) if response.UtcOffsetSeconds() is not None else None,
                        'fetched_at': datetime.now().isoformat()
                    }
                }
                
                processed_data.append(processed_city)
        
        logging.info(f"Successfully processed {len(processed_data)} cities")
        return processed_data
        
    except Exception as e:
        logging.error(f"Error fetching city weather data: {e}")
        return []

def save_city_weather_data(data, filename='city_weather_data.json'):
    """Save city weather data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        
        file_size = len(json.dumps(data)) / 1024 / 1024
        logging.info(f"Saved {len(data)} cities to {filename} ({file_size:.1f} MB)")
        
        # Also save a timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"city_weather_data_backup_{timestamp}.json"
        with open(backup_filename, 'w', encoding='utf-8') as backup_file:
            json.dump(data, backup_file, indent=2, ensure_ascii=False)
        logging.info(f"Backup saved as {backup_filename}")
        
        # Update file modification time to force cache refresh
        current_time = time.time()
        os.utime(filename, (current_time, current_time))
        logging.info(f"File modification time updated to force cache refresh")
        
    except Exception as e:
        logging.error(f"Error saving data to {filename}: {e}")

def check_data_freshness(filename='city_weather_data.json'):
    """Check if the city weather data is fresh (less than 6 hours old)"""
    try:
        if not os.path.exists(filename):
            logging.info(f"Data file {filename} does not exist. Update needed.")
            return False
        
        file_mtime = os.path.getmtime(filename)
        file_age_hours = (time.time() - file_mtime) / 3600
        
        if file_age_hours > 6:  # 6 hours threshold
            logging.info(f"Data file {filename} is {file_age_hours:.1f} hours old. Update needed.")
            return False
        else:
            logging.info(f"Data file {filename} is {file_age_hours:.1f} hours old. Still fresh.")
            return True
            
    except Exception as e:
        logging.error(f"Error checking data freshness: {e}")
        return False

def main():
    """Main function to update city weather data"""
    logger = logging.getLogger(__name__)
    
    logger.info("Starting city weather data update")
    logger.info("=" * 60)
    
    # Check if update is needed
    if check_data_freshness():
        logger.info("City weather data is still fresh. No update needed.")
        return 0
    
    try:
        # Setup OpenMeteo client
        logger.info("Setting up OpenMeteo client with caching...")
        openmeteo_client = setup_openmeteo_client()
        
        # Load city coordinates
        logger.info("Loading city coordinates...")
        cities = load_city_coordinates()
        
        if not cities:
            logger.error("No cities loaded. Cannot proceed with update.")
            return 1
        
        # Fetch city weather data
        logger.info(f"Fetching weather data for {len(cities)} cities...")
        city_weather_data = fetch_city_weather_data(openmeteo_client, cities)
        
        if city_weather_data:
            # Save the updated data
            save_city_weather_data(city_weather_data)
            logger.info("City weather data update completed successfully!")
            
            # Log summary
            logger.info(f"Updated {len(city_weather_data)} cities")
            logger.info("Data saved to city_weather_data.json")
            
            return 0
        else:
            logger.error("Failed to fetch city weather data")
            return 1
            
    except Exception as e:
        logger.error(f"Error during city weather data update: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
