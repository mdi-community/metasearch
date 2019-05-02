"""
Abstract interfaces for expressing and submitting a query to a repository
"""
from abc import ABCMeta, abstractmethod, abstractproperty

class Query(object):
    """
    an encapsulation of a query to a particular repository expressed through
    a general interface.

    A query has two types of constraints:
      *  text terms or phrases that will be compared against any number of
         metadata fields in the repositories database.
      *  constraints on specific metadata fields having recognized names:
         the constraint would be applied against a specific field at the
         repository.
    """
    __metaclass__ = ABCMeta

    def __init__(self, baseurl, authentication=None):
        """
        initialize the query around a base url

        :param str baseurl:   the base URL to the repository's REST search
                              endpoint.
        :param dict authentication:  an object to use for authentication
                              (to be defined)
        """
        self.base = baseurl
        self.auth = authentication

        # this is a list of commonly defined field names that this repository
        # will recognize and try to interpret
        self.supported = []

    @abstractmethod
    def add_freetext_constraint(self, term):
        """
        add a constraint to this query.  The result will included records that
        match the given terms somewhere in the document.

        The implementing repository decides which fields it looks for these
        terms in.

        :param term:   a word, phrase, or a list of phrases to search for
                       matches against
        :type  term:   str or list of str
        """
        raise NotImplemented()

    @abstractmethod
    def add_field_constraint(self, fieldname, testvalue):
        """
        add a search constraint to this query against a specific term or concept
        in the repository.

        :param str fieldname:   a name for a field or concept recognized by
                                the repository.  If the name if not recognized
                                or supported, the repository may ignore it or
                                tread it value as free-text search term.
        :param any testvalue:   the value to test the field against
        """
        raise NotImplemented()

    @abstractmethod
    def page(self, num=1):
        """
        set the page number the search query is to return.

        :param num:  the page number .submit() is to return.
        """
        raise NotImplemented()

    @abstractmethod
    def submit(self):
        """
        submit the query in its current state to the repository as a full query
        and return the results

        :return:  QueryResult, a container for the results of the query as
                  answered by the repository.
        """
        raise NotImplemented()

    def supported_fields(self):
        """
        return a list of the field names that this implementation will
        recognize and support as searchable.
        """
        return list(self.supported)
