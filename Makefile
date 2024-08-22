#
export COLLECTION_NAMESPACE ?= bodsch
export COLLECTION_NAME      ?= email
export COLLECTION_ROLE      ?=
export COLLECTION_SCENARIO  ?= default

.PHONY: install uninstall doc converge test destroy verify lint gh-clean

default: converge

install:
	@hooks/install

uninstall:
	@hooks/uninstall

doc:
	@hooks/doc

converge:
	@hooks/converge

test:
	@hooks/test

destroy:
	@hooks/destroy

verify:
	@hooks/verify

lint:
	@hooks/lint

gh-clean:
	@hooks/gh-clean
