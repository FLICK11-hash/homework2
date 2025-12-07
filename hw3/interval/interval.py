# write your solution here
# Looked up on generative AI how to call repr(s) (s!r)

from functools import total_ordering

class InvalidTimeError(ValueError):     # inherits from ValueError
    pass
    
@total_ordering
class Interval:
    def __init__(self, seconds: int = 0, *, minutes: int = 0, hours: int = 0):      # Everything after * must be passed by keyword, not by position
        total = int(seconds) + int(minutes) * 60 + int(hours) * 3600        # Retrieves all the total seconds
        if total < 0:       # If the number is negative, it is desirable, therefore raise Error
            raise InvalidTimeError(f"Interval cannot be negative: {total} seconds")
        self._seconds = total

    @classmethod
    def from_string(cls, s):        # Parameters is s:String with the documentation and cls:Interval
        if not isinstance(s, str):      # If s isn't a string, we have issues
            raise InvalidTimeError(f"from_string expects a string, got {type(s).__name__}")
        
        parts = s.split(":")        # Split hours, minutes and seconds to understand it better
        if len(parts) != 3:     # We are only expecting three variables
            raise InvalidTimeError(f"Invalid time format: {s!r}. Expected HHH:MM:SS")       # includes quotes for strings and other debug-friendly info
        
        hours_str, minutes_str, seconds_str = parts     # Initialize these parts
        if not (hours_str.isdigit() and minutes_str.isdigit() and seconds_str.isdigit()):
            raise InvalidTimeError(f"Invalid time components in {s!r}")     # We raise error if something isn't in a valid format
        
        if len(minutes_str) != 2 or len(seconds_str) != 2:      # Seconds and mintues must have a length of two
            raise InvalidTimeError(f"Minutes and seconds must be two digits in {s!r}")

        hours = int(hours_str)      # Initialize the numbers in a simpler form that is easier to call
        minutes = int(minutes_str)
        seconds = int(seconds_str)

        if not (0 <= minutes < 60 and 0 <= seconds < 60):       # If seconds and/or minutes are out of the range from 0-60, something went wrong and we have to raise error
            raise InvalidTimeError(f"Minutes and seconds must be between 0 and 59 in {s!r}")
        
        total = hours * 3600 + minutes * 60 + seconds       # Calculates total seconds
        return cls(total)       # cls(total) calls the constructor, so this returns a new Interval instance
    
    @property
    def in_seconds(self) -> int:        # Returns only in a seconds format
        return self._seconds

    @property
    def in_minutes(self) -> float:      # Returns only in a minutes format
        return self._seconds / 60.0

    @property
    def in_hours(self) -> float:        # Returns only in a hours format
        return self._seconds / 3600.0

    def __repr__(self) -> str:      # Calculates the time format correctly
        total = self._seconds
        hours = total // 3600
        remaining = total % 3600
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def __eq__(self, other):
        if isinstance(other, Interval):     # Checks if equal
            return self._seconds == other._seconds
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Interval):     # Checks greater than or equal to
            return self._seconds < other._seconds
        return NotImplemented
    
    def __add__(self, other):
        if not isinstance(other, Interval):
            raise ValueError("Can only add Interval to Interval")
        total = self._seconds + other._seconds      # Adding the times of two different intervals and then returning it
        return Interval(total)
    
    def __sub__(self, other):
        if not isinstance(other, Interval):
            raise ValueError("Can only subtract Interval from Interval")
        total = self._seconds - other._seconds      # Substracts the total time from one interval to another
        if total < 0:       # If invalid time we raise error, otherwise return valid time
            raise InvalidTimeError("Resulting Interval cannot be negative")
        return Interval(total)
    
    def __mul__(self, factor):
        if not isinstance(factor, int):     # Can only multiply whole int
            raise ValueError("Can only multiply Interval by an integer")
        if factor < 0:      # Raise error if invalid number, otherwise return newly made interval
            raise InvalidTimeError("Cannot multiply Interval by a negative integer")
        total = self._seconds * factor
        return Interval(total)

    def __rmul__(self, factor):     # __rmul__ is needed so that something like 5 * Interval(10) works,
        return self.__mul__(factor)
