# air-quality-download - Development Doc

## Purpose
Download air quality data from Open-Meteo (free, no key) and WAQI APIs.

## Data Sources
1. Open-Meteo Air Quality API: `https://air-quality-api.open-meteo.com/v1/air-quality`
   - Free, no key, historical data supported
   - Pollutants: pm2_5, pm10, ozone, nitrogen_dioxide, sulphur_dioxide, carbon_monoxide
2. WAQI: `https://api.waqi.info/` (requires free token)

## CLI Design
```
air-quality-download current --lat --lon --output
air-quality-download historical --lat --lon --start --end --output
air-quality-download forecast --lat --lon --days --output
```

## Dependencies
- requests>=2.28.0

## Implementation Notes
- Open-Meteo supports hourly data, aggregate to daily/monthly if requested
- Support --pollutants flag to select specific pollutants
- Output CSV or JSON based on file extension
- Include data source attribution in output
