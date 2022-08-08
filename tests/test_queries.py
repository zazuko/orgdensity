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

    def test_service_query(self):

        query = """
        PREFIX schema: <http://schema.org/>
        PREFIX admin: <https://schema.ld.admin.ch/>
        PREFIX locn: <http://www.w3.org/ns/locn#>

        SELECT ?thoroughfare (COUNT(?sub) AS ?companies) ?geom
        FROM <https://lindas.admin.ch/foj/zefix>
        WHERE {
                ?sub a admin:ZefixOrganisation ;
                schema:address/locn:thoroughfare ?thoroughfare;
                admin:municipality <https://ld.admin.ch/municipality/4001>.

        SERVICE <https://geo.ld.admin.ch/query> {

            GRAPH <urn:bgdi:location:streets> {
                ?street_id a <http://www.opengis.net/ont/geosparql#Feature>;
                schema:name ?thoroughfare;
                schema:containedInPlace <https://geo.ld.admin.ch/boundaries/municipality/4001>;
                <http://www.opengis.net/ont/geosparql#hasGeometry>/<http://www.opengis.net/ont/geosparql#asWKT> ?geom.
            }
        }
        }
        GROUP BY ?thoroughfare ?geom
        """

        output = self.lindas_client.send_query(query, timeout=600)
        assert type(output) == pd.DataFrame
        assert output.shape[0] > 0
