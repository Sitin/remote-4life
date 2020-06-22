.PHONY: all, init, deploy

include .env
export $(shell sed 's/=.*//' .env)

ansible_path := ./ci/ansible
ansible_prefix := ansible-playbook -u root --private-key=$(SSH_KEY_FILE) -i $(ansible_path)/inventory.yml

all: deploy

deploy: setup
	@$(ansible_prefix) $(ansible_path)/playbook-theia.yml

setup: check-env create-inventory

check-env:
	@test -e .env || (echo "Error: .env is missing! Run make init and fill .env with your parameters." && exit -1)

create-inventory:
	@sed 's/{{ THEIA_DOMAIN }}/$(THEIA_DOMAIN)/g' $(ansible_path)/inventory-template.yml > $(ansible_path)/inventory.yml

init:
	@test -e .env || cp .env-template .env

env:
	@env
