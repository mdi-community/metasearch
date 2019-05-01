import json
import requests
from urllib.parse import urlencode, quote_plus

from query import Query

class HTQuery(Query):

    def __init__(self, baseurl=None, authentication=None):
        """
        initialize the query around a base url

        :param str baseurl:   the base URL to the repository's REST search
                              endpoint.
        :param dict authentication:  an object to use for authentication
                              (to be defined)
        """
        if baseurl is None:
            baseurl = "www.icemaker.afrlmakerhub.com/api/accio/marklogic_search/"
        super(HTQuery, self).__init__(baseurl, authentication)
        self.host = baseurl.split("/")[0]
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
        self.field.append("{}:{}".format(fieldname, testvalue))
        return self

    def submit(self):
        """
        submit the query in its current state to the repository as a full query
        and return the results

        :return:  QueryResult, a container for the results of the query as
                  answered by the repository.
        """
        params = {
            'rs:graphUri': "http://{}:8016/v1/graphs/mbo".format(self.host)
        }
        if len(self.text) >= 1:
            params['rs:q'] = " ".join(self.text)
        if len(self.field) >= 1:
            params['rs:facets'] = " ".join(self.field)
        url_get_params = urlencode(params, quote_via=quote_plus)
        url = "https://{}?{}".format(self.baseurl, url_get_params)
        response = requests.get(url)
        return response.json()
