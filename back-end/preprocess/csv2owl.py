import csv
from datetime import datetime
import os

from rdflib.namespace import DC, OWL, RDF, RDFS, SKOS

from settings import CSV_DIRECTORY, ONTOLOGY_MAP


# columns in spreadsheet
C_URI = 0
C_LABEL = 1
C_DEF = 3
C_SEE_ALSO = 4

# columns in ontology spreadsheet
URI = 0
TITLE = 0
RIGHTS = 1
PUBLISHER = 2
LABEL = 3
CREATOR = 4
CONTRIBUTOR = 5
DEF = 6
DESC = 7
VERSION = 8
SEE_ALSO = 9


def write_ttl(ontology_name):
    date = datetime.now().strftime("%Y-%m-%d")
    # write out the top concepts
    out_file_name = "ontology.ttl"
    out_file = os.path.join("C:", "\dataset", out_file_name)
    f = open(out_file, "w")
    # prefixes
    #f.write("@prefix %s: <%s> .\n" % (ontology_name, ONTOLOGY_MAP[ontology_name]))

    f.write("@prefix dc: <%s> .\n" % DC)
    f.write("@prefix owl: <%s> .\n" % OWL)
    f.write("@prefix rdf: <%s> .\n" % RDF)
    f.write("@prefix rdfs: <%s> .\n" % RDFS)
    f.write("@prefix skos: <%s> .\n\n\n" % SKOS)

    _write_ontology(ontology_name, date, f)
    _write_classes(ontology_name, f)
    f.close()


def _write_ontology(ontology_name, date, f):
    in_file_name = "output4.csv"
    in_file = os.path.join(CSV_DIRECTORY, in_file_name)
    count = 0

    # ontology
    f.write("#\n")
    f.write("# ontology\n")
    f.write("#\n\n")

    with open(in_file, "rt") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                # header
                continue
            #f.write("<%s> a owl:Ontology ;\n" % (ONTOLOGY_MAP[ontology_name]))
            f.write('    dc:title "%s" ;\n' % row[TITLE])
            f.write('    dc:rights "%s"@en ;\n' % row[RIGHTS])
            #f.write('    dc:publisher "%s"@en ;\n' % row[PUBLISHER])
            #f.write('    rdfs:comment "%s" ;\n' % _parse(row[DEF]))
            #f.write('    rdfs:label "%s" ;\n' % _parse(row[LABEL]))

            # ontology
            creators = row[CREATOR].split(",")
            for creator in creators:
                f.write('    dc:creator "%s" ;\n' % creator)
            if row[CONTRIBUTOR]:
                contributors = row[CONTRIBUTOR].split(", ")
                for contributor in contributors:
                    f.write('    dc:contributor "%s" ;\n' % contributor)
            f.write('    owl:versionInfo "%s";\n' % row[VERSION])
            f.write('    dc:date "%s" ;\n' % date)

            if len(row) > SEE_ALSO and row[SEE_ALSO]:
                see_also = row[SEE_ALSO].split(", ")
                for also in see_also:
                    f.write("    rdfs:seeAlso <%s> ;\n" % also)
            f.write('    dc:description "%s" ;\n' % _parse(row[DESC]))
            f.write("    .\n\n")
            return


def _write_classes(ontology_name, f):
    in_file_name = "output4.csv"
    in_file = os.path.join(CSV_DIRECTORY, in_file_name)
    count = 0

    # classes
    f.write("#\n")
    f.write("# classes\n")
    f.write("#\n\n")

    with open(in_file, "rb") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if (count < 2) or row[C_URI].strip() == "":
                # header
                continue
            f.write(
                "<%s%s> a owl:Class ;\n" % (ONTOLOGY_MAP[ontology_name], row[C_URI])
            )
            f.write("    rdfs:isDefinedBy <%s> ;\n" % (ONTOLOGY_MAP[ontology_name]))
            f.write('    rdfs:label "%s" ;\n' % _parse(row[C_LABEL]))
            if len(row) > C_SEE_ALSO and row[C_SEE_ALSO]:
                see_also = row[C_SEE_ALSO].split(", ")
                for also in see_also:
                    f.write("    rdfs:seeAlso <%s> ;\n" % also)
            f.write('    dc:description "%s" ;\n' % _parse(row[C_DEF]))
            f.write("    .\n\n")


def _parse(obj):
    return obj.replace('"', "%22")

