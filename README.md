# air-quality-download

**Air Quality Data Downloader** — PM2.5, PM10, O3, NO2, SO2, CO from Open-Meteo.

## Install

### ClawHub
```bash
clawhub install air-quality-download
```

### Manual
```bash
git clone https://github.com/ruiduobao/air-quality-download.git
cd air-quality-download
pip install -r requirements.txt  # requests
```

### Claude Code / skills.sh
```bash
/clawhub install air-quality-download
```

## Quick Start
```bash
python scripts/air-quality-download.py current --lat 39.9042 --lon 116.4074
python scripts/air-quality-download.py historical --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31 --aggregate daily
python scripts/air-quality-download.py forecast --lat 39.9042 --lon 116.4074 --days 7
```

## Data Source
- Open-Meteo Air Quality (https://open-meteo.com/) — CC BY 4.0

## License
MIT-0

---

# 空气质量数据下载工具

**空气质量数据下载器** — 从 Open-Meteo 获取 PM2.5、PM10、O3、NO2、SO2、CO 数据。

## 安装

### 手动安装
```bash
git clone https://github.com/ruiduobao/air-quality-download.git
cd air-quality-download
pip install requests
```

## 快速开始
```bash
python scripts/air-quality-download.py current --lat 39.9042 --lon 116.4074
python scripts/air-quality-download.py historical --lat 39.9042 --lon 116.4074 --start 2023-01-01 --end 2023-12-31 --aggregate daily
python scripts/air-quality-download.py forecast --lat 39.9042 --lon 116.4074 --days 7
```

## 数据来源
- Open-Meteo 空气质量 (https://open-meteo.com/) — CC BY 4.0

## 许可证
MIT-0
