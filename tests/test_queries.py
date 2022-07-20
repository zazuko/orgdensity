from graphly.api_client import SparqlClient
from orgdensity.client import LindasClient


class Test_queries:
    @classmethod
    def setup_class(cls):

        cls.endpoint = "https://ld.admin.ch/query"
        cls.client = LindasClient(cls.endpoint, timeout=60)

    def test_lindas_endpoint(self):

        query = "SELECT * WHERE {?s ?p ?o} LIMIT 3"
        df = self.client.send_query(query, timeout=None)
        assert df.shape[0] == 3

    def test_swisstopo_endpoint(self):
        query = "SELECT * WHERE {?s ?p ?o} LIMIT 3"
        geoclient = SparqlClient("https://geo.ld.admin.ch/query")
        df = geoclient.send_query(query, timeout=None)
        assert df.shape[0] == 3

    def test_get_commune_centroid(self):

        input = 4221
        output = self.client.get_commune_centroid(input)
        assert len(output) == 2

    def test_get_communes(self):
        output = self.client.get_communes()
        assert output.shape[0] > 0

    def test_get_commune_streets(self):
        input = 4221
        output = self.client.get_commune_streets(input)
        assert output.shape[0] > 0
