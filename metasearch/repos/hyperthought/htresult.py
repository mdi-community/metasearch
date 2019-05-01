import json
import requests

from ...result import QueryResult
# from .htquery import HTQuery

class HTQueryResult(QueryResult):

    def __init__(self, nativedata, page_size=20, query=None):
        """
        initialize this result with the native data object returned by the
        repository search service.
        """
        super(HTQueryResult, self).__init__(nativedata, page_size, query)
        self._get_next()

    def getNative(self):
        """
        return the query results in its native form
        """
        return self.native

    def _get_next(self):
        self.need_next = False
        self.next = None
        return

    def hasNextPage(self):
        """
        return True if it is (or may be) an additional page of results available
        """
        if self.need_next:
            self._get_next()
        if self.next is None:
            return False
        return True

    def nextPage(self):
        """
        return a QueryResult object that contains the next page of results
        that match the original query.

        :return: QueryResult or None if no further data is available
        """
        if self.need_next:
            self._get_next()
        self.need_next = True
        return self.next
