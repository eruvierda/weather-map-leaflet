# Maritime Weather Data Collection

This folder contains all maritime weather data collection and processing scripts for BMKG (Indonesian Meteorological Agency) maritime weather data.

## 📁 **File Organization**

### **🔧 Core Scripts**
- **`extract_maritime_slugs.py`** - Extracts maritime area names and generates slugs from BMKG data
- **`fetch_maritime_weather.py`** - Main script to fetch weather data from all maritime areas (85% data completeness)

### **🧪 Testing & Analysis Scripts**
- **`test_maritime_api.py`** - Tests BMKG maritime API connectivity and basic data extraction
- **`test_maritime_parsing.py`** - Analyzes HTML structure and pattern extraction capabilities
- **`focused_maritime_test.py`** - Focused pattern analysis for specific weather data fields
- **`test_improved_parser.py`** - Tests the improved maritime weather parser with multiple areas
- **`test_json_ld_extraction.py`** - Tests JSON-LD structured data extraction capabilities

### **📊 Data Files**
- **`maritime_areas.json`** - Contains 139 maritime areas with slugs and URLs
- **`maritime_weather_data.json`** - Collected weather data from all maritime areas
- **`maritime_api_test_results.json`** - Results from API testing

### **📚 Documentation**
- **`MARITIME_DATA_ANALYSIS.md`** - Comprehensive analysis of data extraction capabilities and status

## 🚀 **Quick Start**

### **1. Extract Maritime Areas**
```bash
cd maritime_weather
python extract_maritime_slugs.py
```

### **2. Fetch Weather Data**
```bash
python fetch_maritime_weather.py
```

### **3. Test Parser**
```bash
python test_improved_parser.py
```

## 📊 **Data Extraction Status**

### **✅ Successfully Extracted (85%):**
- Temperature, Humidity, Wind Speed, Wave Height
- Wave Classification, Current Speed, Weather Condition
- Time Data, Current Time Indicator, Weather Icons
- **NEW: JSON-LD Structured Data** (forecast metadata)

### **⚠️ Partially Extracted (15%):**
- Wind Direction, Current Direction, Gust Wind Speed

## 🔍 **Data Structure**

### **Weather Data Fields:**
```json
{
  "area_name": "Perairan Aceh Utara - Aceh Timur",
  "temperature": "27",
  "humidity": "100",
  "wind_speed": "8",
  "wave_height": "2",
  "wave_classification": "Rendah",
  "current_speed": "40",
  "weather_condition": "Berawan Tebal",
  "weather_icon": "/icon/svg/Berawan Tebal PM.svg",
  "structured_data": {
    "forecast_name": "Weather Forecast for...",
    "provider": "BMKG",
    "valid_from": "2025-08-15 00:00 UTC",
    "valid_to": "2025-08-18 00:00 UTC",
    "date_issued": "2025-08-14 12:00 UTC",
    "location": "Perairan Sabang Banda Aceh"
  }
}
```

## 🌊 **Maritime Areas Coverage**

- **Total Areas:** 139 maritime regions
- **Coverage:** Indonesian waters (Aceh to Papua)
- **Data Source:** BMKG official maritime weather service
- **Update Frequency:** Real-time via HTTP requests

## 🛠️ **Technical Details**

### **Dependencies:**
- `requests` - HTTP requests to BMKG API
- `json` - JSON data processing
- `re` - Regular expression pattern matching
- `datetime` - Timestamp handling

### **Data Validation:**
- Humidity: ≤100%
- Wind Speed: ≤100 kt
- Wave Height: ≤20m
- Current Speed: ≤200 cm/s

### **HTML Parsing:**
- CSS class-based extraction
- Table cell pattern matching
- JSON-LD structured data extraction
- Fallback pattern matching for different HTML structures

## 📈 **Performance Metrics**

- **Data Completeness:** 85%
- **Success Rate:** Varies by area (20-100%)
- **Processing Time:** ~1 second per area (with 1s delay)
- **Data Quality:** High (with validation filters)

## 🔄 **Update Process**

1. **Extract Areas:** Run `extract_maritime_slugs.py` to get latest area list
2. **Fetch Data:** Run `fetch_maritime_weather.py` to collect weather data
3. **Validate:** Check data quality and completeness
4. **Integrate:** Use collected data in weather visualization

## 🎯 **Next Steps**

- [ ] Refine wind direction extraction patterns
- [ ] Improve current direction extraction
- [ ] Add gust wind speed extraction
- [ ] Enhance data validation
- [ ] Add coordinate data for map visualization

## 📞 **Support**

For issues or questions about maritime weather data collection, refer to:
- `MARITIME_DATA_ANALYSIS.md` - Detailed technical analysis
- Test scripts for debugging specific functionality
- Data validation results in JSON files 