"""
Abstract interfaces for capturing results from a query to a repository
"""
import cdcsquery
from result import QueryResult
import copy

class CDCSQueryResult(object):
    """
    a container for a result from a query to a repository.  This class gives
    access to summary information about the results and well access to the
    result in its native form.
    """
    __metaclass__ = ABCMeta

    def __init__(self, nativedata, page_size=20,query):
        """
        initialize this result with the native data object returned by the
        repository search service.
        """  
        super(CDCSQueryResult, self).__init__(nativedata, page_size, query)
        self.native = copy.deepcopy(nativedata)
        self.need_next = False
        self.current_page = 1

    def getNext(self):
        url = self.nativedata['next']
        self.nativedata = self.query.submit(url)
        return
        
    def getNative(self):
        """
        return the query results in its native form
        """

        return self.native['results']

    def hasNextPage(self):
        """
        return True if it is (or may be) an additional page of results available
        """
        if self.nativedata['next'] is not None:
            self.need_next = 'true'

        return self

    def nextPage(self):
        """
        return a QueryResult object that contains the next page of results
        that match the original query.

        :return: QueryResult or None if no further data is available
        """
        if self.need_next:
            self.get_next()
        return self.getNative
