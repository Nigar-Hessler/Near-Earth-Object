"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str, boolean_to_string


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical
    parameters about the object, such
    as its primary designation (required, unique),
    IAU name (optional), diameter
    in kilometers (optional - sometimes unknown),
    and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection
    of its close approaches -
    initialized to an empty collection, but eventually
    populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name=None, diameter=None, hazardous=None):
        """Create a new `NearEarthObject`.

        :param designation: primary designation of the asteroid or comet
        :param name: IAU name
        :param diameter: Diameter of asteroid or meteor.
        :param hazardous: if the asteroid or meteor is hazardous
        """
        self.designation = designation
        self.name = None if name == "" else str(name)
        self.diameter = float(diameter) if diameter else float("nan")
        if hazardous == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"A NearEarthObject has id = {self.designation!r}"
            f"and name = {self.name}"
        else:
            return f"A NearEarthObject has id = {self.designation!r}"

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous is True:
            return (
                f"{self.fullname} has a diameter {self.diameter:.3f} km "
                f"and {boolean_to_string(self.hazardous)}"
                "potentially hazardous")
        else:
            return (f"{self.fullname} has a diameter {self.diameter:.3f} km")

    def __repr__(self):
        """Return `repr(self)`, a string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, "
            f"name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Return a dictionary with key attributes of the near earth object."""
        return {'designation': self.designation,
                'name': self.name if self.name else "",
                'diameter_km': self.diameter,
                'potentially_hazardous': self.hazardous}


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information
    about the NEO's close approach to
    Earth, such as the date and time (in UTC) of
    closest approach, the nominal
    approach distance in astronomical units, and
    the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference
    to its `NearEarthObject` -
    initally, this information (the NEO's primary
    designation) is saved in a
    private attribute, but the referenced NEO is
    eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(
            self,
            designation,
            time,
            distance,
            velocity,
            neo: NearEarthObject = None):
        """Create a new `CloseApproach`.

        :param time: Time of close approach in
        NASA-formatted calendar date/time format.
        :param distance: Approach distance in
        astronomical units.
        :param velocity: relative approach velocity
        in kilometers per second
        :param neo: A Near earth object.
        """
        self._designation = designation
        self.time = cd_to_datetime(time) if time else None
        self.distance = float(distance) if distance else float("nan")
        self.velocity = float(velocity) if velocity else float("nan")
        self.neo = neo

    @property
    def designation(self):
        """Return a designation parameter as a property."""
        return self._designation

    @property
    def time_str(self):
        """Return a formatted representation of this approach time.

        The value in `self.time` should be a Python
        `datetime` object. While a
        `datetime` object has a string representation,
        the default representation
        includes seconds - significant figures that
        don't exist in our input
        data set.

        The `datetime_to_str` method converts a
        `datetime` object to a
        formatted string that can be used in
        human-readable representations and
        in serialization to CSV and JSON files.
        """
        return (f"{datetime_to_str(self.time)}")

    def __str__(self):
        """Return `str(self)`."""
        if self.neo.name:
            return (f"On {self.time_str!r} {self.designation!r} "
                    f"{self.neo.name!r} approaches Earth "
                    f"at a distance of {self.distance:.2f} "
                    f"and velocity of {self.velocity:.2f} km/s")
        else:
            return (
                f"On {self.time_str!r} {self.designation!r} approaches Earth "
                f"at a distance of {self.distance:.2f} au "
                f"and velocity of {self.velocity:.2f} km/s")

    def __repr__(self):
        """Return `repr(self)`, a string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, velocity={self.velocity:.2f})")

    def serialize(self):
        """Return a dictionary with key attributes of close approach."""
        return {'datetime_utc': datetime_to_str(self.time),
                'distance_au': self.distance, 'velocity_km_s': self.velocity}
