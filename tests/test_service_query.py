import pandas as pd
from orgdensity.client import LindasClient, SwisstopoClient


class Test_queries:
    @classmethod
    def setup_class(cls):

        cls.lindas_client = LindasClient("https://ld.admin.ch/query")

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

        output = self.lindas_client.send_query(query, timeout=601)
        assert output.shape[0] > 0
