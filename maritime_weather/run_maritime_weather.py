#!/usr/bin/env python3
"""
Maritime Weather Data Collection - Main Runner Script

This script provides easy access to maritime weather operations
from the main project directory.
"""

import os
import sys
import subprocess

def main():
    """Main function to run maritime weather operations"""
    
    print("🌊 Maritime Weather Data Collection")
    print("=" * 50)
    
    # Check if maritime_weather folder exists
    if not os.path.exists('maritime_weather'):
        print("❌ Error: maritime_weather folder not found!")
        print("   Please ensure the folder exists in the current directory.")
        return
    
    # Change to maritime_weather directory
    os.chdir('maritime_weather')
    
    print("📁 Working directory: maritime_weather/")
    print("\n🚀 Available Operations:")
    print("1. Extract maritime areas and slugs")
    print("2. Fetch weather data from all areas")
    print("3. Test improved parser")
    print("4. Test JSON-LD extraction")
    print("5. Run all tests")
    print("6. Show folder contents")
    
    try:
        choice = input("\n🎯 Select operation (1-6): ").strip()
        
        if choice == '1':
            print("\n🔧 Extracting maritime areas and slugs...")
            subprocess.run([sys.executable, 'extract_maritime_slugs.py'])
            
        elif choice == '2':
            print("\n🌊 Fetching weather data from all maritime areas...")
            subprocess.run([sys.executable, 'fetch_maritime_weather.py'])
            
        elif choice == '3':
            print("\n🧪 Testing improved parser...")
            subprocess.run([sys.executable, 'test_improved_parser.py'])
            
        elif choice == '4':
            print("\n🔍 Testing JSON-LD extraction...")
            subprocess.run([sys.executable, 'test_json_ld_extraction.py'])
            
        elif choice == '5':
            print("\n🧪 Running all tests...")
            print("\n--- Testing API connectivity ---")
            subprocess.run([sys.executable, 'test_maritime_api.py'])
            print("\n--- Testing HTML parsing ---")
            subprocess.run([sys.executable, 'test_maritime_parsing.py'])
            print("\n--- Testing focused patterns ---")
            subprocess.run([sys.executable, 'focused_maritime_test.py'])
            print("\n--- Testing improved parser ---")
            subprocess.run([sys.executable, 'test_improved_parser.py'])
            print("\n--- Testing JSON-LD extraction ---")
            subprocess.run([sys.executable, 'test_json_ld_extraction.py'])
            
        elif choice == '6':
            print("\n📁 Maritime Weather Folder Contents:")
            subprocess.run(['dir'], shell=True)
            
        else:
            print("❌ Invalid choice. Please select 1-6.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    # Return to main directory
    os.chdir('..')
    print(f"\n📁 Returned to: {os.getcwd()}")

if __name__ == "__main__":
    main() 