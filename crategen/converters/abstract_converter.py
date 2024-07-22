from abc import ABC, abstractmethod

class AbstractConverter(ABC):
    @abstractmethod
    def convert_to_wrroc(self, data):
        """Convert data to WRROC format"""
    
    @abstractmethod
    def convert_from_wrroc(self, wrroc_data):
        """Convert WRROC data to the original format"""
