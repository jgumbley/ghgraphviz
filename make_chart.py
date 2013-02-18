#!/usr/bin/python
import os
import ghtools
from string import Template
from ghtools import cli
from ghtools.github.organisation import Organisation
from ghtools.github.repo import Repo
from sets import Set
import pickle 

ORGANISATION = "alphagov"
PRIVATE_ONLY = False 

# ortho
GRAPHVIZ_TEMPLATE = """
digraph G {
    node[fontname="Helvetica"];
    edge[dir=none];
    graph[overlap=false,splines=ortho];

    $users

}
"""

def login():
  if not os.environ.has_key("GITHUB_PUBLIC_OAUTH_TOKEN"):
    print("login using gh-login -s repo")

def write_to_file(content, outputfile):
  with open (outputfile, 'w') as f: 
    f.write (content)

def graphviz_dotfile(set_of_links):
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

def all_private_repos():
  org_api = Organisation(ORGANISATION)
  result = Set()
  for repo in org_api.list_repos():
    #print repo
    if repo["private"]:
        result = result.union(commits_for_repo(repo["name"]))
  return result 

BRAKER=100

def commits_for_repo(repo_name):
  repo_api = Repo(ORGANISATION+"/"+repo_name)
  links = Set()
  n = 0
  for u in repo_api.list_commits():
    if u["committer"] != None:
      links.add( ( u["committer"]["login"], repo_name) )
    n+=1
    if n>BRAKER:
      break 
  return links

PICKLE = 'data.pkl'

def grab_and_pickle():
  login()
  set_of_links = all_private_repos()
  output = open(PICKLE, 'wb')
  pickle.dump(set_of_links, output)

if __name__ == '__main__':
  #grab_and_pickle()
  pickle_file = open(PICKLE, 'rb')
  set_of_links=pickle.load(pickle_file)
  write_to_file(graphviz_dotfile(set_of_links), "output.out")
  
