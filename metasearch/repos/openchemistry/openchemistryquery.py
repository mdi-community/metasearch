import requests
import json

from ...query import Query

DEFAULT_BASE_URL = "https://beta.openchemistry.org/"

class OpenChemistryQuery(Query):

    def __init__(self, baseurl=DEFAULT_BASE_URL, authentication=None):
        """
        initialize the query around a base url

        :param str baseurl:   the base URL to the repository's REST search 
                              endpoint.
        :param dict authentication:  an object to use for authentication 
                              (to be defined)
        """
        super(OpenChemistryQuery, self).__init__(baseurl, authentication)
        self.text = []
        self.field = []
        self.fieldvalue = []
        self.supported = ["name", "inchi", "inchikey", "smiles"]

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
        self.field.append(fieldname)
        self.fieldvalue.append(testvalue)
        return self

    def submit(self):
        """
        submit the query in its current state to the repository as a full query
        and return the results

        :return:  QueryResult, a container for the results of the query as
                  answered by the repository.
        """
        resturl = self.base + "/api/v1/"
        
        if len(self.field) >= 1:
            resturl = resturl + "molecules?" + self.field[0] + "=" + self.fieldvalue[0]
        
        print ("resturl:", resturl)
        
        response = requests.get(resturl)
        return response.json()
