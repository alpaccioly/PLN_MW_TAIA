
import re
import sys
import Util
import os.path
import pickle


wikipediaPageList = Util.wikipediaPageList

i = 261
page = wikipediaPageList[i]
print i,"|",page.title
print len(page.links)
page.links = [("graph theory", "https://en.wikipedia.org/wiki/Graph_theory"),
("graph","https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)"),
("subset","https://en.wikipedia.org/wiki/Subset"),
("vertices","https://en.wikipedia.org/wiki/Vertex_(graph_theory)"),
("edge", "https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms#edge"),
("undirected graphs","https://en.wikipedia.org/wiki/Undirected_graph"),
("directed graphs","https://en.wikipedia.org/wiki/Directed_graph"),
("multigraphs","https://en.wikipedia.org/wiki/Multigraph"),
("Induced paths", "https://en.wikipedia.org/wiki/Induced_path"),
("paths","https://en.wikipedia.org/wiki/Path_(graph_theory)"),
("shortest path","https://en.wikipedia.org/wiki/Shortest_path"),
("distance-hereditary graphs","https://en.wikipedia.org/wiki/Distance-hereditary_graph"),
("induced cycles","https://en.wikipedia.org/wiki/Induced_cycle"),
("cycles","https://en.wikipedia.org/wiki/Cycle_(graph_theory)"),
("girth","https://en.wikipedia.org/wiki/Girth_(graph_theory)"),
("strong perfect graph teorem","https://en.wikipedia.org/wiki/Strong_perfect_graph_theorem"),
("complements","https://en.wikipedia.org/wiki/Complement_graph"),
("perfect graphs","https://en.wikipedia.org/wiki/Perfect_graph"),
("cliques","https://en.wikipedia.org/wiki/Clique_(graph_theory)"),
("independent sets","https://en.wikipedia.org/wiki/Independent_set_(graph_theory)"),
("complete graphs", "https://en.wikipedia.org/wiki/Complete_graph"),
("edgeless graphs", "https://en.wikipedia.org/wiki/Edgeless_graph"),
("neighbourhood","https://en.wikipedia.org/wiki/Neighbourhood_(graph_theory)"),
("adjacent", "https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms#adjacent"),
("induced subgraph isomorphism problem","https://en.wikipedia.org/wiki/Induced_subgraph_isomorphism_problem"),
("subgraph isomorphism problem","https://en.wikipedia.org/wiki/Subgraph_isomorphism_problem"),
("clique problem","https://en.wikipedia.org/wiki/Clique_problem"),
("NP-complete","https://en.wikipedia.org/wiki/NP-complete")]

print page.title
print len(page.links)
count = 2
path = os.path.dirname(os.path.abspath(__file__)) + '/files/test/'
# Saving the object in a file
file = path+ str(count) + ".pkl"
with open(file, 'wb') as output:
    pickle.dump(page, output, pickle.HIGHEST_PROTOCOL)
    count = count + 1

print "Done"    