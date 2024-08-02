from enum import Enum
from pathlib import Path

# Enumerations for release types and formats
class ReleaseType(Enum):
    International = 1
    USExtension = 2
    Unknown = 3

class ReleaseFormat(Enum):
    RF1 = 1
    RF2 = 2

# Class representing the release information
class SCTReleaseInfo:
    def __init__(self, release_directory, release_name):
        # Convert release_directory to a Path object for better path manipulation
        self.release_directory = Path(release_directory)
        self.release_name = release_name
        self.release_type = self._determine_release_type()
        self.release_format = self._determine_release_format()
        self.release_month, self.release_year = self._extract_month_and_year()

    def _determine_release_type(self):
        # Determine release type based on the prefix of the release name
        if self.release_name.startswith("INT"):
            return ReleaseType.International
        elif self.release_name.startswith("US"):
            return ReleaseType.USExtension
        else:
            return ReleaseType.Unknown

    def _determine_release_format(self):
        # Determine release format based on the suffix of the release name
        return ReleaseFormat.RF2 if self.release_name.endswith("(RF2)") else ReleaseFormat.RF1

    def _extract_month_and_year(self):
        # Extract month and year from the release name if available
        if " " in self.release_name:
            release_number_str = self.release_name.split(" ")[1].strip()
            release_num = int(release_number_str)
            release_year = release_num // 10000
            release_month = (release_num % 10000) // 100
            return release_month, release_year
        else:
            return 0, 0

    # Getter methods for retrieving release information
    def get_release_directory(self):
        return self.release_directory

    def get_release_type(self):
        return self.release_type

    def get_release_format(self):
        return self.release_format

    def get_release_month(self):
        return self.release_month

    def get_release_year(self):
        return self.release_year

    def get_release_name(self):
        return self.release_name
