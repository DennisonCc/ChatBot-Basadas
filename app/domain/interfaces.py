from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Employee, PauseRecord

class IBackendGateway(ABC):
    @abstractmethod
    async def get_employees(self) -> List[Employee]:
        pass

    @abstractmethod
    async def get_pause_history(self, ci: str = '%', fecha: Optional[str] = None) -> List[PauseRecord]:
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        pass

class IChatAgent(ABC):
    @abstractmethod
    async def get_response(self, message: str, current_screen: Optional[str] = None, session_id: str = "default") -> str:
        pass
