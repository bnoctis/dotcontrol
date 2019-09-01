import subprocess as sp
from os.path import basename
from ..util import keep_cwd


def get_name(remote_location, *args):
	name = basename(remote_location)
	if name.endswith('.git'):
		name = name[:-4]

	return name


def command(profile, *args):
	with keep_cwd(profile.root_path):
		sp.run(['git'] + list(args))


def create_from(profile, remote_location, name, config):
	try:
		command(profile, ['clone', remote_location, name, '--depth=1'])
	except:
		raise Exception('cloning failed')

	config['sync_remote'] = remote_location


def setup(profile, remote_location, config, *args):
	with keep_cwd(profile.root_path):
		config['sync_type'] = 'git'
		config['sync_remote'] = remote_location

		sp.run(['git', 'init'])
		try:
			sp.run(['git', 'remote', 'add', 'origin', remote_location], check=True)
		except:
			sp.run(['git', 'remote', 'set-url', 'origin', remote_location])
		sp.run(['git', 'add', '.'])
		sp.run(['git', 'commit', '-m', 'initialize'])
		sp.run(['git', 'push', '-u', 'origin', 'master'])
	

def commit(profile, *args):
	command(profile, ['commit'] + args)


def pull(profile, *args):
	command(profile, ['pull'] + args)


def push(profile, *args):
	command(profile, ['push'] + args)
