from dataclasses import dataclass

@dataclass
class Prefs:
    cold_bias: int = 0
    wind_tolerance: int = 0
    rain_tolerance: int = 0
    language: str = "en"