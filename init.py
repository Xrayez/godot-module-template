#!/usr/bin/env python3

import os
import json
import argparse

import config
import builders
from vcs import get_providers as get_vcs_providers
from messages import *


def init(name, output_path, config_path, force=False):
	root_dir = os.getcwd()
	
	# Load config
	try:
		with open(config_path) as config_data:
			module = json.load(config_data)
	except Exception as e:
		print_info('config: ' + str(e))
		return
		
	if output_path:
		module_path = os.path.join(output_path, module['short_name'])
	else:
		module_path = os.path.join(root_dir, module['short_name'])

	try:
		if os.path.exists(module_path) and force:
			revert(module_path)

		generate(module, module_path)
		
	except Exception as e:
		print_info(str(e))
		print_info(INFO_PASS_FORCE_CMD)
		
		
def revert(path):
	import shutil
	shutil.rmtree(path)


def generate(module, module_path):
	
	# Create folder
	os.makedirs(module_path)

	### Generate!
	
	# Essential
	builders.make_config(module, module_path)
	builders.make_register_types(module, module_path)
	
	# Optional
	if module['readme']['initialize']:
		builders.make_readme(module, module_path)
		
	if module['license']:
		builders.make_license(module, module_path)
	
	if module['version_control']:
		initialize_repository(module_path, module['version_control'])
		
		
def initialize_repository(module_path, vcs_name):
	
	for vcs in get_vcs_providers():
		if not vcs.can_handle(vcs_name):
			continue
		vcs.initialize(module_path)
	
		
def open_utf8(filename, mode):
	return open(filename, mode, encoding="utf-8")
		
	
def print_info(msg):
	print(__file__ + ': ' + msg)
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-n', '--name', default="")
	parser.add_argument('-o', '--output-path', default="")
	parser.add_argument('-c', '--config-path', default="configs/default.json")
	
	parser.add_argument('-f', '--force', action="store_true")
	
	module = parser.parse_args()
	init(module.name, module.output_path, module.config_path, module.force)
