"""
Abstract interfaces for capturing results from a query to a repository
"""
import copy

from abc import ABCMeta, abstractmethod, abstractproperty

class QueryResult(object):
    """
    a container for a result from a query to a repository.  This class gives
    access to summary information about the results and well access to the
    result in its native form.
    """
    __metaclass__ = ABCMeta

    def __init__(self, nativedata, page_size=20, page=1, query=None):
        """
        initialize this result with the native data object returned by the
        repository search service.
        """
        self.page_size = page_size
        self.current_page = page
        self.query = query
        self.native = copy.deepcopy(nativedata)

    def getNative(self):
        """
        return the query results in its native form
        """
        return self.native

    @abstractmethod
    def count(self):
        """
        return the number of records in this result that matches the
        generating query.

        :return: int, the number of matched records
        """
        raise NotImplemented()

    # We no longer have a .hasNextPage() method due to not all of the demo
    # search engines correctly implementing paging.  That is, not all search
    # engines return the total number of matches with each paged results
    # response.  :-(

    @abstractmethod
    def nextPage(self):
        """
        return a QueryResult object that contains the next page of results
        that match the original query.

        :return: QueryResult or None if no further data is available
        """
        raise NotImplemented()
