from abc import ABC, abstractmethod
from typing import Any, Dict

class AbstractConverter(ABC):
    @abstractmethod
    def convert_to_wrroc(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert data to WRROC format"""
    
    @abstractmethod
    def convert_from_wrroc(self, wrroc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert WRROC data to the original format"""
