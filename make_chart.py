#!/usr/bin/python
import os
import ghtools
from string import Template
from ghtools import cli
from ghtools.github.organisation import Organisation
from ghtools.github.repo import Repo
from sets import Set
import pickle 


# ortho
GRAPHVIZ_TEMPLATE = """
digraph G {
    node[fontname="Helvetica"];
    edge[dir=none];
    graph[overlap=false,splines=ortho];

    $users

}
"""

def make_graphviz_dotfile(set_of_links):
  graph = Template(GRAPHVIZ_TEMPLATE)
  graphviz_format_links = setof_links_to_graphviz(set_of_links)
  return graph.substitute(users=graphviz_format_links)

def setof_links_to_graphviz(set_of_links):
  result = ""
  for user in derive_users(set_of_links):
    result += "   " + user + "[shape=box, color=blue];" 
  for link in set_of_links:
    result +=  "  " + sanitize(link[0]) + '->' + sanitize(link[1]) + "; \n"
  for repo in derive_repos(set_of_links):
    result += "   " + repo + "[shape=record, color=red];"
  return result

def derive_repos(setlinks):
  out = Set()
  for link in setlinks:
    out.add(sanitize(link[1]))
  return out

def derive_users(setlinks):
  out = Set()
  for link in setlinks:
    out.add(sanitize(link[0]))
  return out

def sanitize(text):
  return text.replace("-", "_")

PICKLE = 'data.pkl'

def filter_repos(set_of_links, blacklist):
  return [com for com in set_of_links if com[1] not in blacklist]

def write_to_file(content, outputfile):
  with open (outputfile, 'w') as f:
    f.write(content)

if __name__ == '__main__':
  blacklist = [
      "wiki",
      "puppet",
      "vcloud-provisioner",
      "development",
      "alphagov-deployment",
      "gds-provisioner",
      "private-utils",
      ]
  pickle_file = open(PICKLE, 'rb')
  set_of_links=pickle.load(pickle_file)
  print blacklist
  filtered_set_of_links=filter_repos(set_of_links, blacklist)
  write_to_file(make_graphviz_dotfile(filtered_set_of_links), "output.out")
  
