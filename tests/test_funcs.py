from etl.funcs import latitudeLongitude2, tenement
from etl.utils import EX

from rdflib import Graph


def test_latitudeLongitude():
    # declare static inputs
    iri = EX.Feature01
    subject = {"latitude": 137, "longitude": -23}
    g = Graph()

    # make a comparison object
    g2 = Graph().parse(
        data="""
            PREFIX ex: <http://example.com/>
            PREFIX geo: <http://www.opengis.net/ont/geosparql#>
            
            ex:Feature01
                geo:hasGeometry [
                    a geo:Geometry ;
                    geo:asWKT "POINT(137, -23)"^^geo:wktLiteral ;
                ] ;
            .
            """,
        format="turtle",
    )

    # make a comparison object
    latitudeLongitude2(iri, subject, g)

    # print test output
    print(g.serialize(format="longturtle"))
    print(g2.serialize(format="longturtle"))

    # compare comparison object to function being tested's output
    assert g2.isomorphic(g)


def test_tenement():
    # declare static inputs
    iri = EX.Thing01
    subject = {
        "tenement": "250",
    }
    g = Graph()

    # make a comparison object
    g2 = Graph().parse(
        data="""
            PREFIX ex: <http://example.com/>

            ex:Thing01 ex:hasTenement <http://example.com/tenement/250> .
            """,
        format="turtle",
    )

    # make a comparison object
    t = tenement(iri, subject, g)

    # printing to test the test
    print(t.serialize(format="longturtle"))
    print(g2.serialize(format="longturtle"))

    # compare comparison object to function being tested's output
    assert g2.isomorphic(t)
