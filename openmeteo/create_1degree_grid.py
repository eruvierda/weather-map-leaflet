import json

# Generate 1-degree grid for Indonesia
latitudes = []
longitudes = []

for lat in range(-11, 7):  # -11 to 6
    for lon in range(95, 142):  # 95 to 141
        latitudes.append(f"{lat:.4f}")
        longitudes.append(f"{lon:.4f}")

grid_data = {
    "latitude": ",".join(latitudes),
    "longitude": ",".join(longitudes),
    "grid_size": 1,
    "total_points": len(latitudes)
}

with open("gridData_1degree.json", "w") as f:
    json.dump(grid_data, f, indent=2)

print(f"Generated {len(latitudes)} grid points with 1-degree spacing") 