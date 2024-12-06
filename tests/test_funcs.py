from etl.funcs import latitudeLongitude2, tenement, make_geometry
from etl.utils import EX

from rdflib import Graph, URIRef
from shapely import Polygon


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


def test_make_geometry_wkt_text():
    g = Graph()
    feature_iri = URIRef("http://example.com/feature/x")
    wkt = "POINTZ(137 -27)"

    # test 2D point
    g2 = Graph().parse(
        data="""
                PREFIX geo: <http://www.opengis.net/ont/geosparql#>

                <http://example.com/feature/x>
                    geo:hasGeometry
                        [
                            a geo:Geometry ;
                            geo:asWKT "POINT(137 -27)"^^geo:wktLiteral ;
                        ] ;
                .        
        """,
        format="turtle",
    )

    make_geometry(g, feature_iri, wkt=wkt)

    print(g.serialize(format="longturtle"))
    print(g2.serialize(format="longturtle"))

    assert g2.isomorphic(g)


def test_make_geometry_latlong():
    # test 3D point
    g = Graph()
    feature_iri = URIRef("http://example.com/feature/x")
    long = 137
    lat = -27
    ele = 350

    g2 = Graph().parse(
        data="""
                PREFIX geo: <http://www.opengis.net/ont/geosparql#>
                
                <http://example.com/feature/x>
                    geo:hasGeometry
                        [
                            a geo:Geometry ;
                            geo:asWKT "POINTZ(137 -27 350)"^^geo:wktLiteral ;
                        ] ;
                .        
        """,
        format="turtle",
    )

    make_geometry(g, feature_iri, longitude=long, latitude=lat, elevation=ele)

    print(g.serialize(format="longturtle"))
    print(g2.serialize(format="longturtle"))

    assert g2.isomorphic(g)

    # test 2D point
    g3 = Graph().parse(
        data="""
                PREFIX geo: <http://www.opengis.net/ont/geosparql#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                <http://example.com/feature/x>
                    geo:hasGeometry
                        [
                            a geo:Geometry ;
                            geo:asWKT "POINT(137 -27)"^^geo:wktLiteral ;
                        ] ;
                .        
        """,
        format="turtle",
    )

    g = Graph()

    make_geometry(g, feature_iri, longitude=long, latitude=lat)

    print(g.serialize(format="longturtle"))
    print(g3.serialize(format="longturtle"))

    assert g3.isomorphic(g)


def test_make_geometry_shapely_polygon():
    g = Graph()
    feature_iri = URIRef("http://example.com/feature/x")
    poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]])

    # test 2D point
    g2 = Graph().parse(
        data="""
                PREFIX geo: <http://www.opengis.net/ont/geosparql#>

                <http://example.com/feature/x>
                    geo:hasGeometry
                        [
                            a geo:Geometry ;
                            geo:asWKT "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"^^geo:wktLiteral ;
                        ] ;
                .        
        """,
        format="turtle",
    )

    make_geometry(g, feature_iri, shapely_object=poly)

    print(g.serialize(format="longturtle"))
    print(g2.serialize(format="longturtle"))

    assert g2.isomorphic(g)


def test_make_geometry_description():
    g = Graph()
    feature_iri = URIRef("http://example.com/feature/x")
    desc = "Room 3, Shelf 18, Box 23A"

    # test 2D point
    g2 = Graph().parse(
        data="""
                PREFIX geo: <http://www.opengis.net/ont/geosparql#>
                PREFIX schema: <https://schema.org/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                <http://example.com/feature/x>
                    geo:hasGeometry
                        [
                            a geo:Geometry ;
                            schema:description "Room 3, Shelf 18, Box 23A"^^xsd:string ;
                        ] ;
                .        
        """,
        format="turtle",
    )

    make_geometry(g, feature_iri, description=desc)

    print(g.serialize(format="longturtle"))
    print(g2.serialize(format="longturtle"))

    assert g2.isomorphic(g)