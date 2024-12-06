from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import GEO, RDF, RDFS

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
    if tenement_id is not None:
        t = URIRef(EX_tenement + clean_id(tenement_id))
        g.add((iri, EX.hasTenement, t))
    return g