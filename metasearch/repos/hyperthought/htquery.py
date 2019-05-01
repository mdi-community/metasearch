import requests
import json

from query import Query

class HTQuery(Query):

    def __init__(self, baseurl, authentication=None):
        """
        initialize the query around a base url

        :param str baseurl:   the base URL to the repository's REST search 
                              endpoint.
        :param dict authentication:  an object to use for authentication 
                              (to be defined)
        """
        super(HTQuery, self).__init__(baseurl, authentication)
        self.text = []
        self.field = []

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
        self.text.append(term)
        return self

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
        self.field.append("{}:\"{}\"".format(fieldname, testvalue))
        return self

    def _build_search_term(self):
        terms = []
        if self.hasproperty('text') and len(self.text) >= 1:
            terms.append(" AND ".join(self.text))
        if self.hasproperty('field') and len(self.field) >= 1:
            terms.append(" AND ".join(self.field))
        term = " AND ".join(terms)
        return term

    def submit(self):
        """
        submit the query in its current state to the repository as a full query
        and return the results

        :return:  QueryResult, a container for the results of the query as
                  answered by the repository.
        """
        rest_api_endpoint = "www.icemaker.afrlmakerhub.com/api/accio/marklogic_search/"
        search_term = self._build_search_term()
        graph_uri = "http%3A%2F%2Fmarklogic.icemaker.afrlmakerhub.com%3A8016%2Fv1%2Fgraphs%2Fmbo"
        url = "https://{}?rs%3Aq={}&rs%3AgraphUri={}".format(rest_api_endpoint, search_term, graph_uri)
        response = requests.get(url)
        return response.json()
