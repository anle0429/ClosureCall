# Evidence references

Checked official documentation on 2026-10-10. These support source/API facts; prototype action mappings are our own.

- NWS API / application User-Agent and GeoJSON: https://www.weather.gov/documentation/services-web-api
- Open-Meteo modeled AQ (CAMS; returned grid may differ from requested point): https://open-meteo.com/en/docs/air-quality-api
- AirNow AQI category definitions (151–200 unhealthy, not an office closure mandate): https://www.airnow.gov/aqi/aqi-basics/
- Strands OpenAIModel `client_args` / custom endpoint: https://strandsagents.com/docs/user-guide/sdk/model-providers/openai/
- Workshop Chat Completions and tool calls (`hackathon-chat`, team key): https://github.com/akamai-developers/akamai-workshop-hackmidwest/blob/main/docs/inference.md
- Akamai build guide: https://github.com/akamai-developers/akamai-workshop-hackmidwest/blob/main/docs/build.md
- OPM closure procedures (reference only): https://www.opm.gov/policy-data-oversight/pay-leave/reference-materials/handbooks/dcdismissal.pdf
- Ubuntu Docker official installation (read at deployment time): https://docs.docker.com/engine/install/ubuntu/

Original challenge text referenced by the starter kit is not in this repo; organizer deadline/timezone and judging eligibility remain unconfirmed. UI/source packages attribute modeled AQ to Open-Meteo / Copernicus Atmosphere Monitoring Service (CAMS). Verify licensing before commercial use.
