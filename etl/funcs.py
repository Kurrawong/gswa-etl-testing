from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import GEO, RDF, RDFS, SDO, XSD
from shapely import Point, Polygon, LineString
from typing import Optional, Union

from etl.utils import EX

EX_tenement = "http://example.com/tenement/"


def clean_id(i):
    return str(i)


def latitudeLongitude(iri, subject, g):
    if subject.get("latitude") is not None and subject.get("longitude") is not None:
        Geometry = (
            "POINT("
            + str(subject.get("latitude"))
            + " "
            + str(subject.get("longitude"))
            + ")"
        )
        GeometryBNode = BNode()
        g.add((iri, GEO.hasGeometry, GeometryBNode))
        g.add((GeometryBNode, RDF.type, GEO.Geometry))
        g.add((GeometryBNode, RDFS.label, Literal(Geometry, datatype=GEO.wktLiteral)))
    return g


def latitudeLongitude2(iri, subject, g):
    if subject.get("latitude") is not None and subject.get("longitude") is not None:
        wkt = (
            "POINT("
            + str(subject.get("latitude"))
            + " "
            + str(subject.get("longitude"))
            + ")"
        )
        GeometryBNode = BNode()
        g.add((iri, GEO.hasGeometry, GeometryBNode))
        g.add((GeometryBNode, RDF.type, GEO.Geometry))
        g.add((GeometryBNode, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

        g.bind("ex", EX)

        # returns nothing


def tenement(iri, subject, g):
    if subject.get("tenement") is not None:
        t = URIRef(EX_tenement + clean_id(str(subject.get("tenement"))))
        g.add((iri, EX.hasTenement, t))
    return g


def tenement2(iri: URIRef, tenement_id: str, g: Graph) -> Graph:
    """This function is the same as tenement() but uses type hinting"""
    if tenement_id is not None:
        t = URIRef(EX_tenement + clean_id(tenement_id))
        g.add((iri, EX.hasTenement, t))
    return g


def make_geometry(
        g: Graph,
        feature_iri: URIRef,
        wkt: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        elevation: Optional[float] = None,
        shapely_object: Optional[Union[Point, Polygon, LineString]] = None,
        description: Optional[str] = None
) -> None:
    # make the wkt
    if wkt is not None:
        pass

    if longitude is not None and latitude is not None:
        if elevation is not None:
            wkt = f"POINTZ({longitude} {latitude} {elevation})"
        else:
            wkt = f"POINT({longitude} {latitude})"

    if shapely_object is not None:
        wkt = shapely_object.wkt

    # if, at this point, wkt and description are still none, exit as we have nothing
    if wkt is None and description is None:
        return

    # we have either wkt and/or description, so make basic Geometry
    geom = BNode()
    g.add((feature_iri, GEO.hasGeometry, geom))
    g.add((geom, RDF.type, GEO.Geometry))

    if wkt is not None:
        g.add((geom, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))

    if description is not None:
        g.add((geom, SDO.description, Literal(description, datatype=XSD.string)))
