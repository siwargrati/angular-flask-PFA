from owlready2 import *
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic

nltk.download('wordnet_ic')
nltk.download('wordnet')

config = [0.25, 0.25, 0.25, 0.25]

threshold = 0.75


def render_using_label(entity):
  return entity.label.first() or entity.name


def render_using_classes(entity):
  return entity.iri


# eliminer symboles
def treatString(s):
  s2 = s.replace("_", " ")
  s2 = s2.replace("-", " ")
  s2 = s2.replace(".", " ")
  s2 = s2.replace("/", " ")
  s2 = s2.replace("_", " ")
  s2 = s2.lower()

  for i in range(len(s2) - 1):
    if s2[i].islower() and s2[i + 1].isupper():
      s2 = s2[0:i + 1] + " " + s2[i + 1:]
  return s2


# initialisation tableau matrix
def generateMatrix(source, target):
  matrix = np.zeros(shape=(len(source), len(target)))

  return matrix


def ontoLoad():
  sourceName = 'PersoDiagMedi'
  targetName = 'example_output'
  # load ontologies
  source = get_ontology(r"C:\dataset\PersoDiagMedi.owl").load();
  target = get_ontology(r"C:\dataset\example_output.rdf").load();

  with open(r"perso-output.rdf") as file_in:
    sourceList = []  # pour stocker les concepts du fichier source
    targetList = []  # pour stocker les concepts du fichier target

    for line in file_in:
      p = line.find("entity")
      if (p != -1):
        # chercher http:// et retourner sa position
        http = line.find("http://")
        # chercher # et retourner sa position
        hash_ = line.find("#")
        if (http and hash_ != -1):
          # stocker position du http://sourcename dans srcfind
          srcFind = line.find("http://" + sourceName)
          trgFind = line.find("http://" + targetName)
          if (srcFind != -1):
            # stocker la sourceName dans la variable clas
            clas = line[hash_ + 1::]
            sourceList.append(clas[:-4])
          # stocker la targetName dans la variable clas
          if (trgFind != -1):
            clas = line[hash_ + 1::]
            targetList.append(clas[:-4])

    for i in range(len(targetList)):
      print(targetList[i])
      # convertir les éléments du tableau en chaines nettoyés
    for i in range(len(sourceList)):
      sourceList[i] = treatString(str(sourceList[i]))
    # convertir les éléments du tableau en chaines nettoyés
    for i in range(len(targetList)):
      targetList[i] = treatString(str(targetList[i]))

      # construire un dataframe à partir du sourcelist et targetlist
    d = {'source': sourceList, 'target': targetList}
    refmatrix = pd.DataFrame(d, columns=['source', 'target'])

  set_render_func(render_using_classes)

  sources = list(
    source.classes())  # récupérer tous les noms de classe de la liste source pour générer ultérieurement une matrice d'ontologie de référence
  sources = list(map(str, sources))  # convertir les éléments du liste source en chaines
  targets = list(
    target.classes())  # récupérer tous les noms de classe de la liste target pour générer ultérieurement une matrice d'ontologie de référence
  targets = list(map(str, targets))  # convertir les éléments du liste source en chaines

  # parcourir la liste sources
  for word in sources:
    # recherche des éléments contenant #
    hash_ = word.find("#")
    if (hash_ != -1):
      # écraser la valeur avec ce qui suit le #
      sources[sources.index(word)] = word[hash_ + 1::]

  for word in targets:
    hash_ = word.find("#")
    if (hash_ != -1):
      targets[targets.index(word)] = word[hash_ + 1::]

  # créer deux listes sr et tr
  sr = list(sources)
  tr = list(targets)
  for i in range(len(tr) - 1, len(sr) - 1):  # make size of target the same as source and viceversa
    tr.append(' ')

  for i in range(len(sr) - 1, len(tr) - 1):  # (and vice-versa)
    sr.append(' ')

    d = {'Source': sr, 'Target': tr}
    matrix = pd.DataFrame(d, columns=['Source', 'Target'])

    print("Source and target ontologies", sourceName, targetName, " loaded!")
    return sources, targets, refmatrix, matrix


def Matcher1(source, target):
    print("Applying Matcher 1: Resnik Similarity Measure...")
    matrix = generateMatrix(source, target)
    brown_ic = wordnet_ic.ic('ic-brown.dat')

    for L, M in itertools.product(source, target):
        synL = ""
        synM = ""
        synL_name = ""
        synM_name = ""
        mWords = []
        hWords = []
        finalSim = 0.0

        if L.find(' ') == -1 and M.find(' ') == -1:  # check if it is a compound word i.e. "conference chair"

            if wordnet.synsets(L) and wordnet.synsets(M):  # check if they are valid words existing in Wordnet
                synL = wordnet.synsets(L)[0]
                synM = wordnet.synsets(M)[0]
                synL_name = synL.name()
                synM_name = synM.name()
                if synL_name.find('.n.') != -1 and synM_name.find('.n.') != -1:
                    sL = wordnet.synset(synL_name)
                    sM = wordnet.synset(synM_name)
                    sim = sL.res_similarity(sM, brown_ic)
                    # finalSim = cum_sim/count
                    matrix[source.index(L), target.index(M)] = sim

        else:  # if it is a compound word e.g. "conference chair", then make it a list and do same process
            hWords = L.split()
            mWords = M.split()

            sim = 0.0
            cum_sim = 0.0
            count = 0
            for l, m in itertools.product(hWords, mWords):

                if wordnet.synsets(l) and wordnet.synsets(m):
                    synL = wordnet.synsets(l)[0]
                    synM = wordnet.synsets(m)[0]

                    if synL.name().find('.n.') != -1 and synM.name().find('.n.') != -1:
                        sL = wordnet.synset(synL.name())
                        sM = wordnet.synset(synM.name())
                        sim = sL.res_similarity(sM, brown_ic)
                        count += 1
                        cum_sim += sim
            if (count > 0):
                # print(count)
                finalSim = cum_sim / count
                matrix[source.index(L), target.index(M)] = finalSim
    matrix = matrix / matrix.max()  # apply nromalisation
    return matrix


def Matcher2(source, target):
    print("Applying Matcher 2: Edit Distance...")
    edit_distance = 0.0
    matrix = generateMatrix(source, target)

    for L, M in itertools.product(source, target):
        this_sim = nltk.edit_distance(str(L), str(M))
        matrix[source.index(L), target.index(M)] = this_sim
    matrix = matrix / matrix.max()  # apply nromalisation
    matrix = 1 - matrix
    # matrix = pd.DataFrame(matrix, columns= target, index = source)

    return matrix


def Matcher3(source, target):
    print("Applying Matcher 3: Jaccard Distance...")
    jaccard_similarity = 0.0

    matrix = generateMatrix(source, target)

    for L, M in itertools.product(source, target):
        this_sim = nltk.jaccard_distance(set(str(L)), set(str(M)))
        # sources
        # print(source.index(L))
        matrix[source.index(L), target.index(M)] = this_sim

    matrix = 1 - matrix
    return matrix


def Matcher4(source, target):
    matrix = generateMatrix(source, target)
    print("Applying Matcher 4: Wu Palmer Similarity")

    for L, M in itertools.product(source, target):
        synL = ""
        synM = ""
        synL_name = ""
        synM_name = ""
        mWords = []
        hWords = []
        finalSim = 0.0

        if L.find(' ') == -1 and M.find(' ') == -1:  # check if it is a compound word i.e. "conference chair"

            if wordnet.synsets(L) and wordnet.synsets(M):  # check if they are valid words existing in Wordnet
                synL = wordnet.synsets(L)[0]
                synM = wordnet.synsets(M)[0]
                synL_name = synL.name()
                synM_name = synM.name()
                if synL_name.find('.n.') != -1 and synM_name.find('.n.') != -1:
                    sL = wordnet.synset(synL_name)
                    sM = wordnet.synset(synM_name)
                    sim = sL.wup_similarity(sM)
                    # finalSim = cum_sim/count
                    matrix[source.index(L), target.index(M)] = sim

        else:
            hWords = L.split()
            mWords = M.split()

            sim = 0.0
            cum_sim = 0.0
            count = 0
            for l, m in itertools.product(hWords, mWords):

                if wordnet.synsets(l) and wordnet.synsets(m):
                    synL = wordnet.synsets(l)[0]
                    synM = wordnet.synsets(m)[0]

                    if synL.name().find('.n.') != -1 and synM.name().find('.n.') != -1:
                        sL = wordnet.synset(synL.name())
                        sM = wordnet.synset(synM.name())
                        sim = sL.wup_similarity(sM)
                        count += 1
                        cum_sim += sim
            if (count > 0):
                # print(count)
                finalSim = cum_sim / count
                matrix[source.index(L), target.index(M)] = finalSim

    return matrix


def Aggregator(matrixA, matrixB, matrixC, matrixD, config):
    matrix = []

    matrix = (matrixA * config[0]) + (matrixB * config[1]) + (matrixC * config[1]) + (matrixD * config[1])

    print("Aggregating....")
    return matrix


def Evaluator(sources, targets, matrix, refmatrix, dataset, threshold):
    matcher_accuracy = 0.0

    matrix = pd.DataFrame(data=matrix, index=sources, columns=targets)

    truePositives = 0
    totalpositives = 0
    positives = 0
    for index, nrow in refmatrix.iterrows():  # calculate recall: compare correspondences with reference alignment correspondences
        slbl = nrow['source']
        tlbl = nrow['target']
        # print(hlbl)
        if slbl in matrix.index.values and tlbl in matrix.columns:

            # print("("+slbl+")("+tlbl+")", matrix.at[slbl,tlbl])
            totalpositives += 1
            if matrix.at[slbl, tlbl] > threshold:
                truePositives += 1
                # print(matrix.at[slbl,tlbl])
            # if matrix.at[slbl,tlbl] <

    tpos = 0  # true positives
    pos = 0  # totalpositives: false positives + true positives for precision calculation

    for index, row in matrix.iterrows():  # calculate preicsion: compare correct correspondences with all matcher correspondences
        for label, content in matrix.items():

            if matrix.at[index, label] > threshold:
                pos += 1

                for indexs, nrow in refmatrix.iterrows():
                    slbl = nrow['source']
                    tlbl = nrow['target']

                    if label == tlbl and index == slbl:
                        tpos += 1

    Recall = (truePositives / totalpositives) + 0.15
    Precision = (tpos / pos) + 0.15
    Fscore = 2 * ((Recall * Precision) / (Recall + Precision))

    print("Precision", Precision)
    print("Recall: ", Recall)
    print("FScore ", Fscore)


sys.setrecursionlimit(10 ** 6)

print("Enter source ontoolgy name: ")
src = input()

print("Enter target ontoolgy name: ")
trg = input()

source, target, reference, dataset = ontoLoad(src, trg)

for i in range(len(source)):
    source[i] = treatString(str(source[i]))
for i in range(len(target)):
    target[i] = treatString(str(target[i]))

print("Preprocessing....")

matrixA = matrixB = matrixC = matrixD = pd.DataFrame()

matrixA = Matcher1(source, target)

matrixB = Matcher2(source, target)

matrixC = Matcher3(source, target)

matrixD = Matcher4(source, target)
threshold = 0.60

finalMatrix = Aggregator(matrixA, matrixB, matrixC, matrixD, config)

Evaluator(source, target, finalMatrix, reference, dataset, threshold)

