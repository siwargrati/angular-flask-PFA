import csv
from rdflib import Graph, Literal, Namespace, URIRef

def csv2rdf():
  input_file = list(csv.reader(open('C:\dataset\output4.csv')))

  subjectsClassName = "pfa"

  prefix = ("http://example.com/pfa2021/")
  # make a graph
  g = Graph()
  owl = Namespace("http://www.w3.org/2002/07/owl#")
  g.bind("owl", owl)
  rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
  g.bind("rdf", rdf)
  ex = Namespace(prefix)
  g.bind("ex", ex)

  rowIndex = 0
  for row in input_file:
    colIndex = 0
    subj = URIRef(row[0]) #fixer le subject à la premiére colonne de chaque ligne

    if subjectsClassName != "":
      g.add((subj, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(prefix + subjectsClassName)))
      g.add((URIRef(prefix + subjectsClassName), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#subClassOf"),
             URIRef("http://www.w3.org/2002/07/owl#Thing")))
    else:
      g.add(
        (subj, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/2002/07/owl#Thing")))

    #première ligne
    if rowIndex == 0:
      colIndex2 = 0
      for colVal in row:
        if colIndex2 > 0:
          cellBelow = input_file[rowIndex + 1][colIndex2]
          isObject = not cellBelow.__contains__(" ") and cellBelow.__contains__("dbpedia")
          name = prefix + colVal
          if isObject:
            g.add((URIRef(name), URIRef("http://www.w3.org/2002/07/owl#subPropertyOf"),
                   URIRef("http://www.w3.org/2002/07/owl#topObjectProperty")))
            g.add((URIRef(name), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                   URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Property")))
            g.add((URIRef(name), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                   URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")))
          if not isObject:
            g.add((URIRef(name), URIRef("http://www.w3.org/2002/07/owl#subPropertyOf"),
                   URIRef("http://www.w3.org/2002/07/owl#topDataProperty")))
            g.add((URIRef(name), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                   URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Property")))
            g.add((URIRef(name), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                   URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")))
        colIndex2 += 1

    if rowIndex > 0:
      for colVal in row:
        if colIndex > 0:
          name = prefix + input_file[0][colIndex]
          pred = URIRef(name)
          if colVal != "":
            if not colVal.__contains__(" ") and colVal.__contains__("dbpedia"):
              obj = URIRef(colVal)
            else:
              obj = Literal(colVal)
            g.add((subj, pred, obj))
        colIndex += 1
    rowIndex += 1

  g.serialize(destination='C:\dataset\example_output.ttl', format='turtle')
