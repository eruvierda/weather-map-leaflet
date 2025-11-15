#!/usr/bin/env python3
"""
Automated Unified Weather Data Update Script
Updates all weather data types without user interaction
Designed for scheduled execution and automation
"""

import json
import time
import logging
import os
import sys
from datetime import datetime, timezone
import subprocess

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import city weather update functionality
from update_city_weather import (
    load_city_coordinates, 
    setup_openmeteo_client, 
    fetch_city_weather_data, 
    save_city_weather_data, 
    check_data_freshness as check_city_freshness,
    get_latest_city_fetch_time
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../automated_weather_update.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def _parse_iso_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        if value.endswith('Z'):
            try:
                return datetime.fromisoformat(value[:-1] + '+00:00')
            except ValueError:
                return None
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return None


def _hours_since(dt):
    if dt is None:
        return None
    reference = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    return (reference - dt).total_seconds() / 3600


def _get_latest_grid_fetch_time(filename='grid_weather_data_1degree.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.info(f"Grid data file {filename} does not exist.")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse {filename}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error reading {filename}: {e}")
        return None

    latest_fetch = None
    if isinstance(data, list):
        for entry in data:
            if not isinstance(entry, dict):
                continue
            weather_data = entry.get('weather_data', {})
            fetched_at = weather_data.get('fetched_at')
            timestamp = _parse_iso_datetime(fetched_at)
            if timestamp and (latest_fetch is None or timestamp > latest_fetch):
                latest_fetch = timestamp

    return latest_fetch


def _parse_port_timestamp(value):
    if not value:
        return None
    if value.endswith(' UTC'):
        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M UTC")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return _parse_iso_datetime(value)


def _get_latest_port_time(filename='../pelabuhan/pelabuhan_weather_data.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.info(f"Port data file {filename} does not exist.")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse {filename}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error reading {filename}: {e}")
        return None

    latest_time = None
    if isinstance(data, list):
        for entry in data:
            if not isinstance(entry, dict):
                continue
            weather_data = entry.get('weather_data') or {}
            issued = weather_data.get('issued')
            timestamp = _parse_port_timestamp(issued)
            if timestamp is None:
                valid_to = weather_data.get('valid_to')
                timestamp = _parse_port_timestamp(valid_to)
            if timestamp is None:
                day1 = weather_data.get('forecast_day1') if isinstance(weather_data, dict) else None
                if isinstance(day1, list) and day1:
                    first_time = day1[0].get('time') if isinstance(day1[0], dict) else None
                    timestamp = _parse_port_timestamp(first_time)
            if timestamp and (latest_time is None or timestamp > latest_time):
                latest_time = timestamp

    return latest_time


def check_grid_data_freshness(filename='grid_weather_data_1degree.json'):
    """Check if the grid weather data is fresh (less than 12 hours old)"""
    try:
        if not os.path.exists(filename):
            logging.info(f"Grid data file {filename} does not exist. Update needed.")
            return False

        latest_fetch = _get_latest_grid_fetch_time(filename)
        if latest_fetch is not None:
            age_hours = _hours_since(latest_fetch)
            if age_hours is not None:
                if age_hours > 12:  # 12 hours threshold for grid data
                    logging.info(
                        f"Most recent grid data in {filename} is {age_hours:.1f} hours old (fetched_at={latest_fetch.isoformat()}). Update needed."
                    )
                    return False
                logging.info(
                    f"Most recent grid data in {filename} is {age_hours:.1f} hours old (fetched_at={latest_fetch.isoformat()}). Still fresh."
                )
                return True

        file_mtime = os.path.getmtime(filename)
        file_age_hours = (time.time() - file_mtime) / 3600
        logging.info(
            f"Could not determine fetched_at timestamps in {filename}. Falling back to file age of {file_age_hours:.1f} hours."
        )
        return file_age_hours <= 12

    except Exception as e:
        logging.error(f"Error checking grid data freshness: {e}")
        return False


def check_port_data_freshness(filename='../pelabuhan/pelabuhan_weather_data.json'):
    """Check if the port weather data is fresh (less than 6 hours old)"""
    try:
        if not os.path.exists(filename):
            logging.info(f"Port data file {filename} does not exist. Update needed.")
            return False

        latest_time = _get_latest_port_time(filename)
        if latest_time is not None:
            age_hours = _hours_since(latest_time)
            if age_hours is not None:
                if age_hours > 6:  # 6 hours threshold for port data
                    logging.info(
                        f"Most recent port data in {filename} is {age_hours:.1f} hours old (timestamp={latest_time.isoformat()}). Update needed."
                    )
                    return False
                logging.info(
                    f"Most recent port data in {filename} is {age_hours:.1f} hours old (timestamp={latest_time.isoformat()}). Still fresh."
                )
                return True

        file_mtime = os.path.getmtime(filename)
        file_age_hours = (time.time() - file_mtime) / 3600
        logging.info(
            f"Could not determine timestamps in {filename}. Falling back to file age of {file_age_hours:.1f} hours."
        )
        return file_age_hours <= 6

    except Exception as e:
        logging.error(f"Error checking port data freshness: {e}")
        return False

def update_city_weather():
    """Update city weather data"""
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Starting City Weather Update")
    logger.info("=" * 60)
    
    try:
        # Check if update is needed
        if check_city_freshness():
            logger.info("City weather data is still fresh. No update needed.")
            return True
        
        # Setup OpenMeteo client
        logger.info("Setting up OpenMeteo client...")
        openmeteo_client = setup_openmeteo_client()
        
        # Load city coordinates
        logger.info("Loading city coordinates...")
        cities = load_city_coordinates()
        
        if not cities:
            logger.error("No cities loaded. Cannot proceed with update.")
            return False
        
        # Fetch city weather data
        logger.info(f"Fetching weather data for {len(cities)} cities...")
        city_weather_data = fetch_city_weather_data(openmeteo_client, cities)
        
        if city_weather_data:
            # Save the updated data
            save_city_weather_data(city_weather_data)
            logger.info("✅ City weather data update completed successfully!")
            logger.info(f"Updated {len(city_weather_data)} cities")
            return True
        else:
            logger.error("❌ Failed to fetch city weather data")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during city weather data update: {e}")
        return False

def update_grid_weather():
    """Update grid weather data"""
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Starting Grid Weather Update")
    logger.info("=" * 60)
    
    try:
        # Check if update is needed
        if check_grid_data_freshness():
            logger.info("Grid weather data is still fresh. No update needed.")
            return True
        
        # Run the grid weather update script
        logger.info("Running grid weather update script...")
        result = subprocess.run([sys.executable, 'fetch_weather_data.py'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            logger.info("✅ Grid weather data update completed successfully!")
            logger.info("Grid data saved to grid_weather_data_1degree.json")
            return True
        else:
            logger.error(f"❌ Grid weather update failed with return code: {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during grid weather update: {e}")
        return False

def update_port_weather():
    """Update port weather data"""
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Starting Port Weather Update")
    logger.info("=" * 60)
    
    try:
        # Check if update is needed
        if check_port_data_freshness():
            logger.info("Port weather data is still fresh. No update needed.")
            return True
        
        # Run the port weather update script
        logger.info("Running port weather update script...")
        port_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                      'pelabuhan', 'pelabuhan_weather.py')
        
        if os.path.exists(port_script_path):
            result = subprocess.run([sys.executable, port_script_path], 
                                  capture_output=True, text=True, 
                                  cwd=os.path.dirname(port_script_path))
            
            if result.returncode == 0:
                logger.info("✅ Port weather data update completed successfully!")
                return True
            else:
                logger.error(f"❌ Port weather update failed with return code: {result.returncode}")
                logger.error(f"Error output: {result.stderr}")
                return False
        else:
            logger.error(f"❌ Port weather script not found at: {port_script_path}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during port weather update: {e}")
        return False

def show_status():
    """Show current status of all weather data files"""
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Weather Data Status Report")
    logger.info("=" * 60)
    
    # Check city weather data
    city_status = "✅ Fresh" if check_city_freshness() else "❌ Needs Update"
    city_file = 'city_weather_data.json'
    if os.path.exists(city_file):
        city_latest = get_latest_city_fetch_time(city_file)
        if city_latest is not None:
            city_age = _hours_since(city_latest)
            logger.info(
                f"City Weather: {city_status} (Age: {city_age:.1f} hours, fetched_at={city_latest.isoformat()})"
            )
        else:
            city_age = (time.time() - os.path.getmtime(city_file)) / 3600
            logger.info(
                f"City Weather: {city_status} (No fetched_at timestamps found, file age={city_age:.1f} hours)"
            )
    else:
        logger.info("City Weather: ❌ File Not Found")
    
    # Check grid weather data
    grid_status = "✅ Fresh" if check_grid_data_freshness() else "❌ Needs Update"
    grid_file = 'grid_weather_data_1degree.json'
    if os.path.exists(grid_file):
        grid_latest = _get_latest_grid_fetch_time(grid_file)
        if grid_latest is not None:
            grid_age = _hours_since(grid_latest)
            logger.info(
                f"Grid Weather: {grid_status} (Age: {grid_age:.1f} hours, fetched_at={grid_latest.isoformat()})"
            )
        else:
            grid_age = (time.time() - os.path.getmtime(grid_file)) / 3600
            logger.info(
                f"Grid Weather: {grid_status} (No fetched_at timestamps found, file age={grid_age:.1f} hours)"
            )
    else:
        logger.info("Grid Weather: ❌ File Not Found")
    
    # Check port weather data
    port_status = "✅ Fresh" if check_port_data_freshness() else "❌ Needs Update"
    port_file = '../pelabuhan/pelabuhan_weather_data.json'
    if os.path.exists(port_file):
        port_latest = _get_latest_port_time(port_file)
        if port_latest is not None:
            port_age = _hours_since(port_latest)
            logger.info(
                f"Port Weather: {port_status} (Age: {port_age:.1f} hours, latest timestamp={port_latest.isoformat()})"
            )
        else:
            port_age = (time.time() - os.path.getmtime(port_file)) / 3600
            logger.info(
                f"Port Weather: {port_status} (No timestamps found, file age={port_age:.1f} hours)"
            )
    else:
        logger.info("Port Weather: ❌ File Not Found")
    
    logger.info("=" * 60)

def main():
    """Main function to update all weather data automatically"""
    logger = logging.getLogger(__name__)
    
    start_time = time.time()
    logger.info("Automated Unified Weather Data Update System Started")
    logger.info("=" * 60)
    
    # Show initial status
    show_status()
    
    # Update all weather data
    logger.info("Starting automated update of all weather data...")
    logger.info("This may take several minutes...")
    
    # Update city weather
    logger.info("\n1/3: Updating City Weather...")
    city_success = update_city_weather()
    
    # Update grid weather
    logger.info("\n2/3: Updating Grid Weather...")
    grid_success = update_grid_weather()
    
    # Update port weather
    logger.info("\n3/3: Updating Port Weather...")
    port_success = update_port_weather()
    
    # Calculate total time
    total_time = time.time() - start_time
    
    # Final status report
    logger.info("\n" + "=" * 60)
    logger.info("AUTOMATED UPDATE SUMMARY")
    logger.info("=" * 60)
    logger.info(f"City Weather: {'✅ Success' if city_success else '❌ Failed'}")
    logger.info(f"Grid Weather: {'✅ Success' if grid_success else '❌ Failed'}")
    logger.info(f"Port Weather: {'✅ Success' if port_success else '❌ Failed'}")
    logger.info(f"Total Time: {total_time:.1f} seconds")
    
    if all([city_success, grid_success, port_success]):
        logger.info("\n🎉 All weather data updated successfully!")
        return 0
    else:
        logger.info("\n⚠️  Some updates failed. Check logs for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
