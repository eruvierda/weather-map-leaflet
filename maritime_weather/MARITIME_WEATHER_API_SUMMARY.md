# BMKG Maritime Weather API Analysis

## 🎯 **API Discovery Summary**

Based on the analysis of the BMKG maritime weather system, I've successfully identified the correct slug format and API structure.

## 📍 **URL Format**

**Base URL:** `https://maritim.bmkg.go.id/cuaca/perairan/[slug]`

**Example:** `https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur`

## 🔍 **Slug Generation Pattern**

### **Format:** `perairan-[area-name-slugified]`

**Process:**
1. Take the maritime area name (e.g., "Perairan Aceh Utara - Aceh Timur")
2. Remove "Perairan" prefix
3. Convert to lowercase
4. Replace spaces and special characters with hyphens
5. Add "perairan-" prefix

**Examples:**
- "Perairan Aceh Utara - Aceh Timur" → `perairan-aceh-utara-aceh-timur`
- "Perairan Sabang Banda Aceh" → `perairan-sabang-banda-aceh`
- "Perairan Utara Serang" → `perairan-utara-serang`

## 📊 **API Response Analysis**

### **Response Type:** HTML Webpage
- **Content-Type:** `text/html;charset=utf-8`
- **Average Size:** ~300KB per response
- **Data Format:** Embedded in HTML tables

### **Extractable Weather Data:**
- 🌡️ **Temperature:** Found in format "XX°C"
- 💨 **Wind Speed:** Found in format "XX kt" (knots)
- 🧭 **Wind Direction:** Found in format "Angin dari [direction]"
- 🌊 **Wave Height:** Found in format "X.X m"

## 📁 **Files Created**

1. **`maritime_areas.json`** - Complete list of 139 maritime areas with slugs
2. **`extract_maritime_slugs.py`** - Script to extract slugs from perairan.json
3. **`fetch_maritime_weather.py`** - Script to fetch weather data from all areas
4. **`test_maritime_api.py`** - Test script for API validation
5. **`maritime_api_test_results.json`** - Test results

## 🚀 **Usage Instructions**

### **1. Extract All Maritime Areas**
```bash
python extract_maritime_slugs.py
```

### **2. Test API with Sample Areas**
```bash
python test_maritime_api.py
```

### **3. Fetch Weather Data from All Areas**
```bash
python fetch_maritime_weather.py
```

## 📈 **Test Results**

**Success Rate:** 100% (3/3 test areas)
- ✅ Perairan Aceh Utara - Aceh Timur
- ✅ Perairan Sabang Banda Aceh  
- ✅ Perairan Utara Serang

**Data Found:**
- Temperature: 28-29°C
- Wind Speed: 10-16 kt
- Wave Height: 0.75 m

## 🔧 **Implementation Notes**

### **HTML Parsing Required**
Since the API returns HTML pages, you'll need to parse the HTML to extract weather data. The current implementation includes basic regex patterns for:
- Temperature extraction
- Wind speed and direction
- Wave height
- Weather conditions

### **Rate Limiting**
- Add 1-second delay between requests
- Use proper User-Agent headers
- Handle timeouts gracefully

### **Data Structure**
```json
{
  "area_name": "Perairan Aceh Utara - Aceh Timur",
  "slug": "perairan-aceh-utara-aceh-timur",
  "url": "https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur",
  "weather_data": {
    "temperature": "28",
    "wind_speed": "16",
    "wind_direction": "Timur Laut",
    "wave_height": "0.75",
    "weather_condition": "Berawan Tebal"
  },
  "status": "success",
  "timestamp": "2025-08-14T15:46:16.732468"
}
```

## 🎯 **Next Steps**

1. **Run Full Data Collection:** Execute `fetch_maritime_weather.py` to collect data from all 139 areas
2. **Enhance HTML Parsing:** Improve regex patterns based on actual HTML structure
3. **Integrate with Map:** Add maritime weather layer to your weather map
4. **Set Up Automation:** Create daily update system similar to port weather

## 📚 **References**

- **Source:** [BMKG Maritime Weather](https://maritim.bmkg.go.id/cuaca/perairan/perairan-aceh-utara-aceh-timur)
- **Data Source:** `perairan.json` from BMKG API
- **Total Areas:** 139 maritime areas across Indonesia 