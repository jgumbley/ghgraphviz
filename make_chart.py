#!/usr/bin/python
import os
import subprocess
import ghtools
from string import Template
from ghtools import cli
from ghtools.github.organisation import Organisation

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

def graphviz_dotfile():
  graph = Template(GRAPHVIZ_TEMPLATE)
  return graph.substitute(users=all_private_repos())

def all_private_repos():
  org = Organisation(ORGANISATION)
  result = "" 
  for repo in org.list_repos():
    if repo["private"]:
      #repos.append( { "name": repo["name"], "private": repo["private"] } )
      repo = Repo(args.repo)
      result +=  "  " + repo["name"].replace("-", "") + "; \n"
  return result 

if __name__ == '__main__':
  login()
  write_to_file(graphviz_dotfile(), "output.out")
  
