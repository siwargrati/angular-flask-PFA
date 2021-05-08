#!/usr/bin/env python
# coding: utf-8

# # CSV to RDF Conversion Example
#
# CSV is by far the most common format of "open data" on the web. This small tutorial shows how CSV can be converted to RDF in a programmatic fashion. Other tools exist, such as [OpenRefine](http://openrefine.org) with the [RDF extension](https://github.com/fadmaa/grefine-rdf-extension/releases) or [LODRefine](https://github.com/sparkica/LODRefine) (which has RDF support built-in) but they do not really scale beyond simple datasets, and do not offer a repeatable framework (as e.g. can be used in a conversion pipeline).
#
# ### Reading a CSV file
#
# Make sure the file `example.csv` is in the same directory as this IPython notebook.

# In[35]:


import csv


def csv2rdf():
  filename = 'C:\dataset\output.csv'
  with open(filename, 'r') as csvfile:
    # Set the right quote character and delimiter
    csvreader = csv.reader(csvfile, quotechar='"', delimiter=',')

    # If the first row contains header information, we can retrieve it like so:
    header = next(csvreader)
    print(header)

    print("Lines")
    for line in csvreader:
      # Line is an array of the columns in the file
      # Make sure to check the encoding of the strings in the array... this often causes issues
      print(line)

  # Alternatively, you can use a `csv.DictReader` object to turn the entire CSV file into a list of dictionaries. Note that this will load the CSV file into memory. For large CSV files, it is better to process the file line by line.

  # In[36]:

  from csv import DictReader

  filename = "C:\dataset\output.csv"

  with open(filename, 'r') as csvfile:
    csv_contents = [{k: v for k, v in row.items()}
                    for row in csv.DictReader(csvfile, skipinitialspace=True, quotechar='"', delimiter=',')]

  print(csv_contents)

  # ### Setting up stuff for RDF
  #
  # We import the things we'll need from `rdflib`:
  #
  # * `Dataset` is the object in which we will store our RDF graphs
  # * `URIRef` is the datatype for URI-resources
  # * `Literal` is the datatype for literal resources (strings, dates etc.)
  # * `Namespace` is used to create namespaces (parts of the URI's we are going to make)
  # * `RDF`, `RDFS`, `OWL` and `XSD` are built in namespaces
  #
  # **NB**: We'll use "group 20" for this example, but you should replace it with your own group name!

  # In[37]:

  from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD

  # A namespace for our resources
  data = 'http://data.krw.d2s.labs.vu.nl/PFA/resource/'
  DATA = Namespace(data)
  # A namespace for our vocabulary items (schema information, RDFS, OWL classes and properties etc.)
  vocab = 'http://data.krw.d2s.labs.vu.nl/PFA/vocab/'
  VOCAB = Namespace('http://data.krw.d2s.labs.vu.nl/PFA/vocab/')

  # The URI for our graph
  graph_uri = URIRef('http://data.krw.d2s.labs.vu.nl/PFA/resource/examplegraph')

  # We initialize a dataset, and bind our namespaces
  dataset = Dataset()
  dataset.bind('pfadata', DATA)
  dataset.bind('pfavocab', VOCAB)

  # We then get a new graph object with our URI from the dataset.
  graph = dataset.graph(graph_uri)

  # ### Let's make some RDF from our CSV Dictionary
  #
  # A straightforward conversion:
  #
  # * Make sure you have URIRef objects for all resources you want to make
  # * Make sure you have Literal objects for all literal values you need. Be sure to use the proper datatype or a language tag.
  # * Decide on what URI will be the 'primary key' for each row.
  # * Decide on the terms you are going to use to create the relations (predicates, properties)
  # * Add the triples to the graph

  # In[38]:

  # IRI baker is a library that reliably creates valid (parts of) IRIs from strings (spaces are turned into underscores, etc.).
  from iribaker import to_iri

  # Let's iterate over the dictionary, and create some triples
  # Let's pretend we know exactly what the 'schema' of our CSV file is
  for row in csv_contents:
    country = URIRef(to_iri(data + row['Country']))
    # But we'd also like to use the name as a label (with a language tag!)
    country_name = Literal(row['Country'], datatype=XSD['string'])

    # `Address` is a literal (a string)
    poidss = Literal(row['Poids'], datatype=XSD['string'])

    graph.add((country, VOCAB['country'], country_name))

    # All set... we are now going to add the triples to our graph
    graph.add((country, VOCAB['country'], country_name))
    graph.add((country, VOCAB['poids'], poidss))

  # Let's see how this turned out:

  # In[39]:

  print(dataset.serialize(format='trig'))

  # ### Saving the RDF to a file

  # In[40]:

  f = open('C:\dataset\output1.rdf', 'wb')
  graph.serialize(f, format='trig')

  # ### Now, with a bit more thought
  #
  # Actually, we were a bit naive just now.
  #
  # * We are implicitly defining a schema: all property names are schema information. We might want to include an (externally defined) schema information.
  # * Some of these properties may have useful standard names (e.g. for the `g20vocab:name` property we can use `rdfs:label`).
  # * We have not specified types for our URIs.
  # * The CSV-file specific named graph may not be the best place for some of our information (e.g. the names of things that may occur in multiple graphs).
  # * And we have 2 *different* Amsterdam resources... one in NL, the other one in the US.

  # In[41]:

  # Clear the graph from the dataset (because we're going to start anew)
  dataset.remove_graph(graph)
  # And get a new object (with the same URI, to create some confusion)
  graph = dataset.graph(graph_uri)

  # Load the externally defined schema into the default graph (context) of the dataset

  dataset.default_context.parse('vocab.ttl', format='turtle')

  # Let's iterate over the dictionary, and create some triples
  # Let's pretend we know exactly what the 'schema' of our CSV file is
  for row in csv_contents:
    country = URIRef(to_iri(data + row['Country']))
    country_name = Literal(row['Country'], datatype=XSD['string'])

    poids = Literal(row['Poids'], datatype=XSD['string'])

    # All set... we are now going to add the triples to our graph
    graph.add((country, RDFS.label, country_name))
    graph.add((country, VOCAB['poids'], poids))

  # Let's see:

  # In[42]:

  print(dataset.serialize(format='trig'))

  # ### ... and Save the RDF to a file

  # In[43]:

  with open('C:\dataset\example-extended.rdf', 'wb') as f:
    dataset.serialize(f, format='trig')

  # ### But for the smartypants...
  #
  # We can actually do without a lot of the explicit assertion of types, since the domain and range definitions already provide us with the miminal information needed to infer the types of all of these things.
  #
  # Let's run the conversion again, without adding the types, and inspect the outcome in TopBraid (or Stardog).
  #
  # Since we've been adding stuff to the default graph, we have to re-initialize our dataset entirely.

  # In[44]:

  # We initialize a fresh dataset, and bind our namespaces
  dataset = Dataset()
  dataset.bind('pfadata', DATA)
  dataset.bind('pfavocab', VOCAB)

  # And get a new object (with the same URI, to create some confusion)
  graph = dataset.graph(graph_uri)

  # Load the externally defined schema into the default graph (context) of the dataset
  dataset.default_context.parse('vocab.ttl', format='turtle')

  # Let's iterate over the dictionary, and create some triples
  # Let's pretend we know exactly what the 'schema' of our CSV file is
  for row in csv_contents:
    # `Country` is a resource
    country = URIRef(to_iri(data + row['Country']))
    # But we'd also like to use the name as a label (with a language tag!)
    country_name = Literal(row['Country'], lang='en')

    # `Address` is a literal (a string)
    poids = Literal(row['Poids'], datatype=XSD['string'])

    # All set... we are now going to add the triples to our graph
    graph.add((country, RDFS.label, country_name))
    graph.add((country, VOCAB['poids'], poids))
    graph.add((country, VOCAB['poids'], poids))

  # Check that indeed the types are missing from the named graph:

  # In[45]:

  print(dataset.serialize(format='trig'))

  # ### And Save the RDF again...

  # In[46]:

  with open('C:\dataset\example-inferencing.rdf', 'wb') as f:
    dataset.serialize(f, format='trig')
