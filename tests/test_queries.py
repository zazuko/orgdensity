import pandas as pd
from orgdensity.client import LindasClient, SwisstopoClient


class Test_queries:
    @classmethod
    def setup_class(cls):

        cls.lindas_client = LindasClient("https://ld.admin.ch/query", timeout=60)
        cls.swisstopo_client = SwisstopoClient("https://geo.ld.admin.ch/query", timeout=60)

    def test_lindas_endpoint(self):

        query = "SELECT * WHERE {?s ?p ?o} LIMIT 3"
        df = self.lindas_client.send_query(query, timeout=None)
        assert df.shape[0] == 3

    def test_swisstopo_endpoint(self):
        query = "SELECT * WHERE {?s ?p ?o} LIMIT 3"
        df = self.swisstopo_client.send_query(query, timeout=None)
        assert df.shape[0] == 3

    def test_get_commune_centroid(self):

        input = 4221
        output = self.lindas_client.get_commune_centroid(input)
        assert len(output) == 2

    def test_get_communes(self):
        output = self.lindas_client.get_communes()
        assert output.shape[0] > 0

    def test_get_commune_orgs(self):
        input = 4221
        output = self.lindas_client.get_orgs_in_commune(input)
        assert output.shape[0] > 0

    def test_get_commune_streets(self):
        input = 4221
        output = self.swisstopo_client.get_commune_streets(input)
        assert output.shape[0] > 0
