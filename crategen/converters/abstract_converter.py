from abc import ABC, abstractmethod

class AbstractConverter(ABC):

    @abstractmethod
    def convert_to_wrroc(self, data):
        """Convert data to WRROC format"""
        pass

    @abstractmethod
    def convert_from_wrroc(self, data):
        """Convert data from WRROC format"""
        pass
