import os
import sys
import json
import datetime
import time

# Add pelabuhan folder to path for imports
sys.path.append('pelabuhan')
from pelabuhan_weather import main as collect_weather_data

def check_data_freshness():
    """Check if pelabuhan_weather_data.json is current (less than 24 hours old)"""
    
    filename = "pelabuhan/pelabuhan_weather_data.json"
    
    if not os.path.exists(filename):
        print("📁 pelabuhan/pelabuhan_weather_data.json not found. Starting fresh data collection...")
        return False
    
    # Check file modification time
    file_mtime = os.path.getmtime(filename)
    current_time = datetime.datetime.now().timestamp()
    age_hours = (current_time - file_mtime) / 3600
    
    print(f"📁 Data file age: {age_hours:.1f} hours")
    
    if age_hours > 24:
        print("⚠️  Data is older than 24 hours. Updating...")
        return False
    else:
        print("✅ Data is current (less than 24 hours old)")
        return True

def backup_old_data():
    """Create a backup of the old data file"""
    filename = "pelabuhan/pelabuhan_weather_data.json"
    if os.path.exists(filename):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"pelabuhan/pelabuhan_weather_data_backup_{timestamp}.json"
        
        try:
            with open(filename, 'r', encoding='utf-8') as source:
                with open(backup_name, 'w', encoding='utf-8') as backup:
                    backup.write(source.read())
            print(f"💾 Backup created: {backup_name}")
        except Exception as e:
            print(f"⚠️  Warning: Could not create backup: {e}")

def main():
    """Main function to check and update weather data"""
    print("🌤️  Weather Data Update Checker")
    print("=" * 50)
    
    # Check if data is current
    is_current = check_data_freshness()
    
    if not is_current:
        print("\n🔄 Starting data update process...")
        
        # Create backup of old data
        backup_old_data()
        
        # Collect fresh data
        try:
            collect_weather_data()
            print("\n✅ Weather data updated successfully!")
        except Exception as e:
            print(f"\n❌ Error updating weather data: {e}")
            return False
    else:
        print("\n✅ No update needed. Data is current.")
    
    # Verify the updated data
    try:
        with open("pelabuhan/pelabuhan_weather_data.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        successful = sum(1 for item in data if item.get('status') == 'success')
        failed = sum(1 for item in data if item.get('status') == 'failed')
        total = len(data)
        
        print(f"\n📊 Data Summary:")
        print(f"   📈 Total ports: {total}")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📊 Success rate: {successful/total*100:.1f}%")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not verify data: {e}")
    
    return True

if __name__ == "__main__":
    main() 