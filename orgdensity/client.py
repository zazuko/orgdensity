from graphly.api_client import SparqlClient


class LindasClient(SparqlClient):

    def get_streets(self, muni_id: int):
        query = """
        PREFIX schema: <http://schema.org/>
        PREFIX admin: <https://schema.ld.admin.ch/>
        PREFIX locn: <http://www.w3.org/ns/locn#>

        SELECT DISTINCT ?thoroughfare
        FROM <https://lindas.admin.ch/foj/zefix>
        WHERE {{
                ?sub a admin:ZefixOrganisation ;
                schema:address/locn:thoroughfare ?thoroughfare;
                admin:municipality <https://ld.admin.ch/municipality/{}>.

        }}
        """.format(
            muni_id
        )
        df = self.send_query(query)
        return df["thoroughfare"]

    def get_companies_on_street(self, muni_id: int, street: str):
        query = """PREFIX schema: <http://schema.org/>
        PREFIX admin: <https://schema.ld.admin.ch/>
        PREFIX locn: <http://www.w3.org/ns/locn#>

		SELECT (COUNT(?sub) AS ?companies)
        FROM <https://lindas.admin.ch/foj/zefix>
        WHERE {{
                ?sub a admin:ZefixOrganisation ;
                schema:address/locn:thoroughfare "{}";
                admin:municipality <https://ld.admin.ch/municipality/{}>.

        SERVICE <https://geo.ld.admin.ch/query> {{

            GRAPH <urn:bgdi:location:streets> {{
                ?street_id a <http://www.opengis.net/ont/geosparql#Feature>;
                schema:name "{}";
                schema:containedInPlace <https://geo.ld.admin.ch/boundaries/municipality/{}>;
                <http://www.opengis.net/ont/geosparql#hasGeometry>/<http://www.opengis.net/ont/geosparql#asWKT> ?geom.
            }}
        }}
        }}""".format(street, muni_id, street, muni_id)
        df = self.send_query(query)
        return df["companies"]

    def get_commune_centroid(self, muni_id: int):

        query = """
        SELECT ?geom
        WHERE {{
            <https://ld.admin.ch/municipality/{}> <http://www.opengis.net/ont/geosparql#hasGeometry> ?_geom.

            SERVICE <https://geo.ld.admin.ch/query> {{
                ?_geom <http://www.opengis.net/ont/geosparql#asWKT> ?geom.
            }}
        }}
        """.format(
            muni_id
        )
        df = self.send_query(query)
        df = df.set_crs(epsg=4326)
        centroid = df["geom"].iloc[0].centroid
        return [centroid.y, centroid.x]

    def get_communes(self):
        query = """
        SELECT ?municipality ?municipality_id WHERE {
            ?_municipality a <https://schema.ld.admin.ch/Municipality>;
                <http://schema.org/name> ?municipality;
                <http://schema.org/identifier> ?municipality_id.
        }
        ORDER BY ?municipality
        """
        df = self.send_query(query)
        return df

    def get_commune_streets(self, muni_id: int):
        query = """
        PREFIX schema: <http://schema.org/>
        PREFIX admin: <https://schema.ld.admin.ch/>
        PREFIX locn: <http://www.w3.org/ns/locn#>

        SELECT ?thoroughfare (COUNT(?sub) AS ?companies) ?geom
        FROM <https://lindas.admin.ch/foj/zefix>
        WHERE {{
                ?sub a admin:ZefixOrganisation ;
                schema:address/locn:thoroughfare ?thoroughfare;
                admin:municipality <https://ld.admin.ch/municipality/{}>.

        SERVICE <https://geo.ld.admin.ch/query> {{

            GRAPH <urn:bgdi:location:streets> {{
                ?street_id a <http://www.opengis.net/ont/geosparql#Feature>;
                schema:name ?thoroughfare;
                schema:containedInPlace <https://geo.ld.admin.ch/boundaries/municipality/{}>;
                <http://www.opengis.net/ont/geosparql#hasGeometry>/<http://www.opengis.net/ont/geosparql#asWKT> ?geom.
            }}
        }}
        }}
        GROUP BY ?thoroughfare ?geom
        ORDER BY DESC (?companies)
        """.format(
            muni_id, muni_id
        )

        df = self.send_query(query)
        df = df.set_crs(epsg=4326)

        return df
