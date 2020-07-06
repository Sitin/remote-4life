SHELL=/bin/bash
.PHONY: all, setup, deploy
.DELETE_ON_ERROR:

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))
ssh_dir := $(abspath $(current_dir)/ci/.ssh)

$(shell mkdir -p $(ssh_dir))

$(shell test -e .env || cp .env-template .env)
include .env
export $(shell sed 's/=.*//' .env)

ssh_private_key := $(abspath $(ssh_dir)/id_rsa)
server_domain := $(shell env `cat .env` python ci/bin/load_param.py server_domain)
linux_user := $(shell env `cat .env` python ci/bin/load_param.py linux_user)

ansible_path := ./ci/ansible
ansible_prefix := SSH_DIR=$(ssh_dir) ansible-playbook -u root --private-key=$(ssh_private_key) -i $(ansible_path)/inventory.yml

all: deploy

deploy: setup
	@$(ansible_prefix) $(ansible_path)/playbook-main.yml

ssh:
	@ssh -i ./ci/.ssh/id_rsa $(linux_user)@$(server_domain)

vnc-tunnel:
	@ssh -i ./ci/.ssh/id_rsa -L 59000:localhost:5901 -C -N $(linux_user)@$(server_domain)

setup: chmod-ssh-keys create-inventory

create-inventory:
	@sed 's/{{ server_domain }}/$(server_domain)/g' $(ansible_path)/inventory-template.yml > $(ansible_path)/inventory.yml

chmod-ssh-keys:
	@chmod -f 600 ci/.ssh/* || : && chmod -f 640 ci/.ssh/*.pub || :

load: load-config load-ssh

save: save-config save-ssh

load-config:
	@python ci/bin/load_config.py $(current_dir)config.yaml

load-ssh:
	@python ci/bin/load_ssh.py $(ssh_dir)

ensure-config:
	test -e config.yaml || cp config-template.yaml config.yaml

save-config:
	@python ci/bin/save_config.py $(current_dir)config.yaml

save-ssh:
	@python ci/bin/save_ssh.py $(ssh_dir)

clean:
	@rm -rf config.yaml

env:
	@env
