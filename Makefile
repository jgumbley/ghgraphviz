# A note on Make syntax..
# ---------------------------------------------------------------------
# target: dependency dependency
# <tab!>shell commands
#
# oh, and .PHONEY: a target means its a named target
# (rather than a REAL file target)

.PHONY: default
default authenticated: 
	@echo [All done]

GHAUTH_ENV=GITHUB_PUBLIC_OAUTH_TOKEN

check-env:
ifndef $(GHAUTH_ENV)
     $(error $(GHAUTH_ENV) is undefined, login with gh-login command)
endif

