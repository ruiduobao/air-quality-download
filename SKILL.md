---
description: 'Download air quality data (PM2.5, PM10, O3, NO2, SO2, CO) from Open-Meteo

  Air Quality API (free, no key). Supports current, historical, and forecast

  data with hourly/daily/monthly aggregation.

  '
name: air-quality-download
---

# air-quality-download

Download air quality data from Open-Meteo Air Quality API. No API key required. Supports current conditions, historical data, and forecasts.

## Features

- **Current Air Quality**: Real-time pollutant concentrations
- **Historical Data**: Up to several years of hourly data
- **Forecast**: Up to 16 days ahead
- **Multiple Pollutants**: PM2.5, PM10, O3, NO2, SO2, CO
- **Aggregation**: Hourly, daily, monthly averages
- **CSV/JSON Output**: Flexible output formats

## Usage

```bash
# Current air quality
python scripts\air-quality-download.py current --lat 39.9042 --lon 116.4074

# Historical data (daily aggregation)
python scripts\air-quality-download.py historical --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31 --aggregate daily

# 7-day forecast
python scripts\air-quality-download.py forecast --lat 39.9042 --lon 116.4074 --days 7

# Specific pollutants
python scripts\air-quality-download.py current --lat 39.9042 --lon 116.4074 --pollutants pm2_5,ozone,nitrogen_dioxide
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--lat` | Latitude (-90 to 90) | Required |
| `--lon` | Longitude (-180 to 180) | Required |
| `--start` | Start date (YYYY-MM-DD) | Required (historical) |
| `--end` | End date (YYYY-MM-DD) | Required (historical) |
| `--days` | Forecast days (1-16) | 7 |
| `--pollutants` | Comma-separated pollutant list | pm2_5,pm10 |
| `--aggregate` | Aggregation level (hourly/daily/monthly) | hourly |
| `--output` | Output file path | Auto-generated |

## Installation

```bash
pip install requests>=2.28.0 tqdm numpy scipy
# Or: pip install -r scripts/requirements.txt
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | Open-Meteo API calls |
| `numpy` | Data aggregation |
| `tqdm` | Progress bars |

## Data Source

- **Open-Meteo Air Quality** (https://open-meteo.com/) — CC BY 4.0
- No API key required
- Historical data from 2022 onward
- European CAMS model + local station data fusion

## Batch / Multi-Location Support

```bash
# Loop over multiple locations
for lat_lon in "39.9 116.4" "31.2 121.5" "23.1 113.3"; do
  set -- $lat_lon
  python scripts\air-quality-download.py historical --lat $1 --lon $2 --start 2023-01-01 --end 2023-12-31 --aggregate daily --output "aq_${1}_${2}.csv"
done
```

## Output Format Selection

- **CSV**: Use for tabular analysis, spreadsheet import
- **JSON**: Use for programmatic processing, API integration
- Default output is CSV. Use `--format json` for JSON output.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `ConnectionError` | Network issue | Check internet, retry |
| `HTTP 429` | Rate limit | Wait 60s, retry |
| `HTTP 400` | Invalid parameters | Check lat/lon range and date format |
| Empty output | No data for location/dates | Try different parameters |
| `ModuleNotFoundError` | Missing dep | Run pip install |

## Timezone Documentation

- **Open-Meteo**: Returns UTC time by default. Use `--timezone auto` for local time.
- **CNEMC** (if supported): Returns local China time (UTC+8).

## Spatial Resolution Info

| Source | Resolution |
|--------|------------|
| Open-Meteo | ~11 km (CAMS model grid) |
| CNEMC station data | Station-level (point) |

## AQI Calculation Option

Calculate AQI from pollutant concentrations:

```bash
python scripts\air-quality-download.py aqi --input pm25.csv --output aqi.csv
```

Supports China HJ 633-2012 AQI standard and US EPA AQI standard (`--standard china` or `--standard us`).

## "All" Pollutants Option

Use `--pollutants all` to download all available pollutants at once:

```bash
python scripts\air-quality-download.py historical --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31 --pollutants all
```

## Data Quality Flags

Open-Meteo provides quality flags when available. Check the `quality_flag` column in CSV output:
- `0`: Good quality
- `1`: Moderate quality
- `2`: Low quality (use with caution)

## Data Availability Check

```bash
# Check data availability for a location and date range
python scripts\air-quality-download.py check --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31
```

## Out-of-Range Date Handling

Open-Meteo air quality data is available from **2022-06-01** onward. Requests for earlier dates will return an error. For historical data before 2022, consider ERA5 reanalysis or local station records.

## Citation

```bibtex
@misc{openmeteo2024air,
  title={Open-Meteo Air Quality API},
  author={{Open-Meteo}},
  year={2024},
  url={https://open-meteo.com/en/docs/air-quality-api},
  note={CC BY 4.0}
}
```

## Visualization Guidance

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("air_quality.csv")
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
for ax, pollutant in zip(axes, ["pm2_5", "pm10", "ozone"]):
    ax.plot(df["time"], df[pollutant], linewidth=0.8)
    ax.set_ylabel(f"{pollutant} (µg/m³)")
    ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("air_quality_timeseries.png", dpi=150)
```

## Pollutants

| Key | Name | Unit |
|-----|------|------|
| pm2_5 | PM2.5 | µg/m³ |
| pm10 | PM10 | µg/m³ |
| ozone | Ozone (O3) | µg/m³ |
| nitrogen_dioxide | NO2 | µg/m³ |
| sulphur_dioxide | SO2 | µg/m³ |
| carbon_monoxide | CO | µg/m³ |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `ConnectionError` | Network issue | Check internet, retry |
| `HTTP 429` | Rate limit | Wait 60s, retry |
| `ValueError` | Invalid input | Check parameter format |
| Empty output | No data | Try different parameters |
| `ModuleNotFoundError` | Missing dep | Run pip install |

---

## Advanced Usage

### Batch Multi-City Download
```bash
for city in "北京" "上海" "广州"; do
  python scripts\air-quality-download.py download     --city "$city" --pollutant PM2.5     --start 2023-01-01 --end 2023-12-31     --output aqi_${city}_2023.csv
  sleep 1
done
```

### CI/CD Integration (GitHub Actions)
```yaml
# .github/workflows/update-aqi.yml
name: Air Quality Monitor
on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 08:00 Beijing time
jobs:
  download:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install requests
      - run: |
          python scripts\air-quality-download.py download \
            --city 北京 --pollutant PM2.5 \
            --start $(date -d '7 days ago' +%Y-%m-%d) \
            --end $(date +%Y-%m-%d) \
            --output data/beijing_pm25.csv
```

### PostgreSQL Import
```bash
python scripts\air-quality-download.py download   --city 北京 --pollutant PM2.5   --start 2023-01-01 --end 2023-12-31   --output aqi.csv

psql -d gis_db -c "\COPY air_quality(city, date, pm25, pm10, o3, no2, so2, co) FROM 'aqi.csv' CSV HEADER"
```

### Performance Tips
- Use `--aggregate daily` to reduce file size (default is hourly)
- Add `sleep 1` between city queries to respect rate limits
- `--pollutant ALL` downloads all 6 pollutants in one request

---

## 中文说明

从 Open-Meteo 空气质量 API 下载 PM2.5、PM10、O3、NO2、SO2、CO 数据。无需 API key，支持实时、历史、预报三种模式。

## 安装

```bash
pip install requests>=2.28.0 tqdm numpy scipy
# 或: pip install -r scripts/requirements.txt
```

## 依赖

| 包 | 用途 |
|-----|------|
| `requests` | Open-Meteo API 调用 |
| `numpy` | 数据聚合 |
| `tqdm` | 进度条 |

## 批量/多位置支持

```bash
# Shell 循环处理多个位置
for lat_lon in "39.9 116.4" "31.2 121.5" "23.1 113.3"; do
  set -- $lat_lon
  python scripts\air-quality-download.py historical --lat $1 --lon $2 --start 2023-01-01 --end 2023-12-31 --aggregate daily --output "aq_${1}_${2}.csv"
done
```

## 输出格式选择

- **CSV**：用于表格分析、电子表格导入
- **JSON**：用于程序化处理、API 集成
- 默认输出为 CSV。使用 `--format json` 获取 JSON 格式。

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ConnectionError` | 网络问题 | 检查网络，重试 |
| `HTTP 429` | 速率限制 | 等待 60 秒后重试 |
| `HTTP 400` | 无效参数 | 检查经纬度范围和日期格式 |
| 空输出 | 无数据 | 尝试不同参数 |
| `ModuleNotFoundError` | 缺少依赖 | 运行 pip install |

## 时区说明

- **Open-Meteo**：默认返回 UTC 时间。使用 `--timezone auto` 获取本地时间。
- **CNEMC**（如支持）：返回中国本地时间（UTC+8）。

## 空间分辨率

| 数据源 | 分辨率 |
|--------|--------|
| Open-Meteo | ~11 km（CAMS 模型网格） |
| CNEMC 站点数据 | 站点级（点数据） |

## AQI 计算选项

从污染物浓度计算 AQI：

```bash
python scripts\air-quality-download.py aqi --input pm25.csv --output aqi.csv
```

支持中国 HJ 633-2012 AQI 标准和美国 EPA AQI 标准（`--standard china` 或 `--standard us`）。

## "全部"污染物选项

使用 `--pollutants all` 一次下载所有可用污染物：

```bash
python scripts\air-quality-download.py historical --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31 --pollutants all
```

## 数据质量标记

Open-Meteo 在可用时提供质量标记。检查 CSV 输出中的 `quality_flag` 列：
- `0`：质量好
- `1`：质量中等
- `2`：质量低（谨慎使用）

## 数据可用性检查

```bash
# 检查某位置和日期范围的数据可用性
python scripts\air-quality-download.py check --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31
```

## 超出范围日期处理

Open-Meteo 空气质量数据从 **2022-06-01** 起可用。请求更早日期将返回错误。2022 年之前的历史数据请考虑 ERA5 再分析或本地站点记录。

## 引用格式

```bibtex
@misc{openmeteo2024air,
  title={Open-Meteo Air Quality API},
  author={{Open-Meteo}},
  year={2024},
  url={https://open-meteo.com/en/docs/air-quality-api},
  note={CC BY 4.0}
}
```

## 可视化指南

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("air_quality.csv")
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
for ax, pollutant in zip(axes, ["pm2_5", "pm10", "ozone"]):
    ax.plot(df["time"], df[pollutant], linewidth=0.8)
    ax.set_ylabel(f"{pollutant} (µg/m³)")
    ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("air_quality_timeseries.png", dpi=150)
```

## 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ConnectionError` | 网络问题 | 检查网络，重试 |
| `HTTP 429` | 速率限制 | 等待 60 秒后重试 |
| `ValueError` | 无效输入 | 检查参数格式 |
| 空输出 | 无数据 | 尝试不同参数 |
| `ModuleNotFoundError` | 缺少依赖 | 运行 pip install |

从 Open-Meteo 空气质量 API 下载 PM2.5、PM10、O3、NO2、SO2、CO 数据。无需 API key，支持实时、历史、预报三种模式。

## 功能特性

- **实时空气质量**：当前污染物浓度
- **历史数据**：多年小时级数据回溯
- **预报数据**：最长 16 天预报
- **多种污染物**：PM2.5、PM10、O3、NO2、SO2、CO
- **数据聚合**：小时/日/月平均
- **CSV/JSON 输出**：灵活输出格式

## 使用方法

```bash
# 实时空气质量
python scripts\air-quality-download.py current --lat 39.9042 --lon 116.4074

# 历史数据（日聚合）
python scripts\air-quality-download.py historical --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31 --aggregate daily

# 7 天预报
python scripts\air-quality-download.py forecast --lat 39.9042 --lon 116.4074 --days 7

# 指定污染物
python scripts\air-quality-download.py current --lat 39.9042 --lon 116.4074 --pollutants pm2_5,ozone,nitrogen_dioxide
```

## 数据来源

- **Open-Meteo 空气质量** (https://open-meteo.com/) — CC BY 4.0
- 无需 API key
- 历史数据从 2022 年起
- 欧洲 CAMS 模型 + 地面站融合数据

## 污染物列表

| 参数 | 名称 | 单位 |
|------|------|------|
| pm2_5 | PM2.5 | µg/m³ |
| pm10 | PM10 | µg/m³ |
| ozone | 臭氧 (O3) | µg/m³ |
| nitrogen_dioxide | 二氧化氮 (NO2) | µg/m³ |
| sulphur_dioxide | 二氧化硫 (SO2) | µg/m³ |
| carbon_monoxide | 一氧化碳 (CO) | µg/m³ |
