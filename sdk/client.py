import requests
from typing import Dict, Any, Optional
from datetime import datetime

class AcousticDesignClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/api/v1/health")
        response.raise_for_status()
        return response.json()

    def record_stress_event(self, gsr: float, hrv: float, temperature: float, 
                          anxiety_score: float, timestamp: Optional[str] = None) -> Dict[str, Any]:
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + "Z"
        
        payload = {
            "timestamp": timestamp,
            "gsr": gsr,
            "hrv": hrv,
            "temperature": temperature,
            "anxiety_score": anxiety_score
        }
        response = self.session.post(f"{self.base_url}/api/v1/stress", json=payload)
        response.raise_for_status()
        return response.json()

    def record_acoustic_metrics(self, rt60: float, sti: float, 
                              frequency_response: Dict[str, float],
                              spatial_metrics: Dict[str, float],
                              timestamp: Optional[str] = None) -> Dict[str, Any]:
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + "Z"
            
        payload = {
            "timestamp": timestamp,
            "rt60": rt60,
            "sti": sti,
            "frequency_response": frequency_response,
            "spatial_metrics": spatial_metrics
        }
        response = self.session.post(f"{self.base_url}/api/v1/acoustic", json=payload)
        response.raise_for_status()
        return response.json()

    def get_stress_events(self, limit: int = 100) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/api/v1/stress?limit={limit}")
        response.raise_for_status()
        return response.json()

    def get_acoustic_metrics(self, limit: int = 100) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/api/v1/acoustic?limit={limit}")
        response.raise_for_status()
        return response.json()
