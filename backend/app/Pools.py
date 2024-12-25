# Description: Defines the data models and utility functions for the swimming pool application.

from uuid import uuid4, UUID
from typing import Optional, List
from pydantic import BaseModel, Field


class PoolLog(BaseModel):
    """
    Represents a maintenance log entry for the pool.
    """

    id: UUID = Field(default_factory=uuid4)  # UUID field with default factory
    date: str
    pH_level: float
    chlorine_level: float
    notes: Optional[str] = ""

    class Config:
        # Allow both UUID and str inputs for id field
        json_encoders = {
            UUID: str  # Ensure UUID is serialized as a string
        }


class Pool(BaseModel):
    """
    Represents a swimming pool and its associated information and operations.
    """

    id: Optional[str] = None
    owner_name: str
    length: float
    width: float
    depth: float
    type: str
    notes: Optional[str] = None
    water_volume: float = Field(default_factory=lambda: 0.0)
    next_maintenance: Optional[str] = None
    logbook: List[PoolLog] = Field(default_factory=list)

    def validate_dimensions(cls, values):
        """
        Ensures that pool dimensions are positive numbers.
        """
        if (
            values.get("length", 0) <= 0
            or values.get("width", 0) <= 0
            or values.get("depth", 0) <= 0
        ):
            raise ValueError(
                "Pool dimensions (length, width, depth) must be positive numbers."
            )
        return values

    def calculate_volume(self) -> float:
        """
        Calculates the water volume of the pool in cubic meters.
        """
        return self.length * self.width * self.depth

    def log_maintenance(self, log: PoolLog):
        """
        Adds a maintenance log entry to the pool's logbook.
        """
        self.logbook.append(log)

    def schedule_maintenance(self, next_date: str):
        """
        Schedules the next maintenance for the pool.
        """
        self.next_maintenance = next_date

    def display_info(self) -> str:
        """
        Displays essential pool information in a formatted string.
        """
        return (
            f"Owner: {self.owner_name}\n"
            f"Dimensions: {self.length}m x {self.width}m x {self.depth}m\n"
            f"Water Volume: {self.water_volume:.2f} cubic meters\n"
            f"Type: {self.type}\n"
            f"Notes: {self.notes or 'None'}"
        )

    def display_logbook(self) -> str:
        """
        Displays the maintenance logbook in a formatted string.
        """
        if not self.logbook:
            return "No maintenance logs available."
        return "\n".join(
            [
                f"Date: {log.date}\n"
                f"pH Level: {log.pH_level}\n"
                f"Chlorine Level: {log.chlorine_level}\n"
                f"Notes: {log.notes or 'None'}"
                for log in self.logbook
            ]
        )


class PoolUtils:
    """
    Utility class for checking pool maintenance parameters.
    """

    @staticmethod
    def check_ph_level(ph_level: float) -> str:
        """
        Checks if the pH level is within the safe range.
        """
        if 7.2 <= ph_level <= 7.8:
            return "pH level is within the safe range."
        elif ph_level < 7.2:
            return "pH level is too low. Add pH increaser."
        else:
            return "pH level is too high. Add pH reducer."

    @staticmethod
    def check_chlorine_level(chlorine_level: float) -> str:
        """
        Checks if the chlorine level is within the safe range.
        """
        if 1.0 <= chlorine_level <= 3.0:
            return "Chlorine level is within the safe range."
        elif chlorine_level < 1.0:
            return "Chlorine level is too low. Add chlorine."
        else:
            return "Chlorine level is too high. Dilute with water or wait for natural reduction."
