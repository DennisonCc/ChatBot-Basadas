import httpx
from typing import List, Optional
from app.domain.interfaces import IBackendGateway
from app.domain.models import Employee, PauseRecord
from app.infrastructure.common.config import config

class FlaskBackendGateway(IBackendGateway):
    def __init__(self):
        self.base_url = config.FLASK_API_URL

    async def get_employees(self) -> List[Employee]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/empleados")
                response.raise_for_status()
                data = response.json()
                return [Employee(**item) for item in data]
            except Exception as e:
                # Log error or raise appropriate domain exception
                return []

    async def get_pause_history(self, ci: str = '%', fecha: Optional[str] = None) -> List[PauseRecord]:
        params = {"ci": ci}
        url = f"{self.base_url}/pausas"
        if fecha:
            url = f"{self.base_url}/pausas/fecha/{fecha}"
            params = {}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                # Ensure data is a list
                if isinstance(data, dict):
                    return []
                return [PauseRecord(**item) for item in data]
            except Exception as e:
                return []

    async def check_health(self) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                # Use employees endpoint as health check
                response = await client.get(f"{self.base_url}/empleados")
                return response.status_code == 200
            except Exception:
                return False
