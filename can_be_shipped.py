from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract: anything that can be shipped must be able
    to say what shipping it costs. No attributes or shipping details live here."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Returns the cost of shipping this item."""
