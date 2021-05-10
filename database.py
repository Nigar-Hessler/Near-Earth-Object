"""A database encapsulating collections of NEO and CA.

A `NEODatabase` holds an interconnected data
set of NEOs and close approaches.
It provides methods to fetch an NEO by primary
designation or by name, as well
as a method to query the set of close approaches
that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates
one NEODatabase from the
data on NEOs and close approaches extracted
by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

from models import NearEarthObject, CloseApproach
from extract import load_neos, load_approaches


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs
    and a collection of close
    approaches. It additionally maintains a few
    auxiliary data structures to
    help fetch NEOs by primary designation or
    by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes
        that the collections of NEOs
        and close approaches haven't yet been
        linked - that is, the
        `.approaches` attribute of each `NearEarthObject`
        resolves to an empty
        collection, and the `.neo` attribute of each
        `CloseApproach` is None.

        However, each `CloseApproach` has an attribute
        (`._designation`) that
        matches the `.designation` attribute of the
        corresponding NEO. This
        constructor modifies the supplied NEOs and close
        approaches to link them
        together - after it's done, the `.approaches` attribute
        of each N a collection of that NEO's close approaches,
        and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        # created 3 dictionaries mapping designation to neo object,
        # name to neo object, designation to approach object
        # going through params neo and approaches and read
        # into dictionaries proper values to proper keys

        self._neos = neos
        self._approaches = approaches
        self.neo_designation = {}
        self.neo_name = {}
        self.approach_designation = {}

        for neo in neos:
            self.neo_designation[neo.designation] = neo

        for neo in neos:
            if neo.name:
                self.neo_name[neo.name] = neo
            else:
                self.neo_name[neo.name] = []

        for approach in approaches:
            if approach.designation in self.approach_designation.keys():
                self.approach_designation[approach.designation].append(
                    approach)
            else:
                self.approach_designation[approach.designation] = [approach]

        for neo in neos:
            neo.approaches = self.approach_designation.get(neo.designation, [])

        for approach in approaches:
            approach.neo = self.neo_designation.get(approach.designation, None)

    @property
    def get_neos(self):
        """Get neos from each class instances."""
        return self._neos

    @property
    def get_approaches(self):
        """Get approaches from each class instances."""
        return self._approaches

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary
        designation, as a string.

        The matching is exact - check for spelling
        and capitalization if no
        match is found.

        :param designation: The primary designation
        of the NEO to search for.
        :return: The `NearEarthObject` with the desired
        primary designation, or `None`.
        """
        return self.neo_designation.get(designation, None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name.
        No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and
        capitalization if no
        match is found.

        :param name: The name, as a string, of the
        NEO to search for.
        :return: The `NearEarthObject` with the desired
        name, or `None`.
        """
        return self.neo_name.get(name, None)

    def query(self, filters=()):
        """Query close approaches to generate filters.

        This generates a stream of `CloseApproach` objects
        that match all of the
        provided filters.

        If no arguments are provided, generate all
        known close approaches.

        The `CloseApproach` objects are generated in
        internal order, which isn't
        guaranteed to be sorted meaninfully, although
        is often sorted by time.

        :param filters: A collection of filters capturing
        user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # if approaches from self approaches comply
        # to all filters, yield this approach
        for approach in self._approaches:
            if all([filter(approach) for filter in filters]):
                yield approach
