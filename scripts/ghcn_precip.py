import os
import requests
import pandas as pd

stations_file = r"C:\Users\Shaira\Desktop\ghcnd-stations.txt"
data_url_base = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/"
output_csv = r"C:\Users\Shaira\Desktop\china_precipitation_2018_2024.csv"

china_stations = []
with open(stations_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("CH"):
            station_id = line[:11].strip()
            name = line[41:71].strip()
            china_stations.append((station_id, name))

print(f"找到 {len(china_stations)} 个中国站点")

all_data = []

def parse_dly(content, station_name):
    for line in content.decode("utf-8").splitlines():
        station_id = line[:11]
        year = int(line[11:15])
        month = int(line[15:17])
        element = line[17:21]

        if element != "PRCP" or not (2018 <= year <= 2024):
            continue

        for day in range(1, 32):
            value_str = line[21 + (day - 1) * 8: 26 + (day - 1) * 8]
            try:
                value = int(value_str)
            except:
                continue

            if value == -9999:
                continue

            try:
                date = f"{year}-{month:02d}-{day:02d}"
                pd.to_datetime(date)  # 过滤非法日期
            except:
                continue

            all_data.append({
                "date": date,
                "city": station_name,
                "precipitation": value / 10.0  # 转成 mm
            })

for station_id, name in china_stations:
    try:
        url = f"{data_url_base}{station_id}.dly"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            parse_dly(r.content, name)
            print(f"已处理: {name}")
        else:
            print(f"❌ 获取失败: {name}")
    except Exception as e:
        print(f"⚠️ 错误 - {name}: {e}")

df = pd.DataFrame(all_data)
df.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"\n✅ 全部完成，已保存为 {output_csv}")
