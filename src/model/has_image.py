from abc import ABC, abstractmethod


class HasImage(ABC):
    @abstractmethod
    def generate_image(self):
        raise NotImplemented
