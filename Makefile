.PHONY: all, init, deploy

$(shell test -e .env || cp .env-template .env)
include .env
export $(shell sed 's/=.*//' .env)

ansible_path := ./ci/ansible
ansible_prefix := ansible-playbook -u root --private-key=$(SSH_PRIVATE_KEY) -i $(ansible_path)/inventory.yml

all: deploy

deploy: setup
	@$(ansible_prefix) $(ansible_path)/playbook-main.yml

setup: check-env create-inventory

check-env:
	@test -e .env || (echo "Error: .env is missing! Run make init and fill .env with your parameters." && exit -1)

create-inventory:
	@sed 's/{{ SERVER_DOMAIN }}/$(SERVER_DOMAIN)/g' $(ansible_path)/inventory-template.yml > $(ansible_path)/inventory.yml

init: chmod-ssh-keys pip-install

pip-install:
	@pip install -r requirements.txt

chmod-ssh-keys:
	@chmod 600 ci/.ssh/id_rsa && chmod 640 ci/.ssh/id_rsa.pub

env:
	@env
