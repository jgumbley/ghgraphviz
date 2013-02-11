#!/usr/bin/python
import os
import ghtools
from string import Template
from ghtools import cli
from ghtools.github.organisation import Organisation
from ghtools.github.repo import Repo
from sets import Set

ORGANISATION = "alphagov"
PRIVATE_ONLY = False 

GRAPHVIZ_TEMPLATE = """
digraph G {

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
  for link in set_of_links:
    result +=  "  " + link[0] + "->" + link[1] + "; \n"
  return result

def all_private_repos():
  org_api = Organisation(ORGANISATION)
  result = "" 
  for repo in org_api.list_repos():
    if repo["private"]:
      repos.append( { "name": repo["name"], "private": repo["private"] } )
  return result 

BRAKER=1000

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


if __name__ == '__main__':
  login()
  set_of_links = commits_for_repo("puppet")
  write_to_file(graphviz_dotfile(set_of_links), "output.out")
  
