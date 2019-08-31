import click
from .control import Control


control = Control()

context_settings = {
	'help_option_names': ('-h', '--help')
}
@click.group(context_settings=context_settings)
def cli():
	'''
	dotcontrol is a dot file manager.
	'''


@cli.command('.', help='list dots in a profile.')
@click.option('-p', '--profile', help='specify profile(s) to list, separate with comma withour whitespace.')
@click.option('-a', '--all', is_flag=True, help='list dots in all profiles.')
def list_dots(profile, all):
	if all:
		profiles = control.iter_profiles()
	else:
		if not profile:
			profiles = (control.current_profile,)
		else:
			profiles = (control.get_profile(name) for name in profile.split(','))
	for profile in profiles:
		click.secho(profile.name, fg='cyan')
		for dot in profile.iter_dots():
			if dot.changed:
				click.secho('* ', fg='red', nl=False)
			click.secho(dot.normalized_origin_path, bold=True)


@cli.command('+', help='add or update dot(s).')
@click.option('-p', '--profile', help='specify profile to add or update dot(s).')
@click.argument('paths', nargs=-1, required=True)
def set_dots(profile, paths):
	if not profile:
		profile = control.current_profile
	else:
		profile = control.get_profile(profile)
	
	for path in paths:
		profile.set_dot(path)


@cli.command('-', help='delete dot(s).')
@click.option('-p', '--profile')
@click.argument('paths', nargs=-1, required=True)
def delete_dots(profile, paths):
	if not profile:
		profile = control.current_profile
	else:
		profile = control.get_profile(profile)
	
	for path in paths:
		profile.delete_dot(path)


@cli.command('p', help='list profiles, or switch to a profile is specifed, which will be created if not existing yet.')
@click.argument('profile', nargs=1, required=False)
def list_or_switch_profile(profile):
	if profile:
		control.switch_profile(profile)
	else:
		for profile in control.iter_profiles():
			if profile.name == control.current_profile.name:
				click.secho('*', fg='green', nl=False)
			if profile.config['sync_type'] != 'local':
				click.secho('=', fg='cyan', nl=False)
			click.echo('\t', nl=False)
			click.echo(profile.name)


@cli.command('p=', help='set up remote profile.')
@click.argument('type') 
@click.argument('args', nargs=-1, required=True)
def setup_remote_profile(type, args):
	control.setup_profile(type, args)


@cli.command('p-', help='delete profile(s).')
@click.argument('profile', nargs=-1, required=True)
def delete_profiles(profile):
	for name in profile:
		if name == control.current_profile.name:
			click.secho('! keeping currently in use profile', fg='red', nl=False)
			click.secho(name, fg='cyan')
			continue
		control.delete_profile(name)


@cli.command('=+', help='set up sync.')
@click.argument('type')
@click.argument('remote', type=str)
def set_sync(type, remote):
	control.set_sync(type, remote)


@cli.command('=.', help='commit changes. may add arguments of configured sync program.')
@click.argument('args', nargs=-1)
def commit_changes(args):
	control.commit_changes(*args)


@cli.command('[=', help='pull from remote. may add arguments of configured sync program.')
@click.argument('args', nargs=-1)
def sync_pull(args):
	control.sync_pull(*args)


@cli.command('=]', help='push to remote. may add arguments of configured sync program.')
@click.argument('args', nargs=-1)
def sync_push(args):
	control.sync_push(*args)


@cli.command('=', help='list sync info, or run commands of configure sync program, if specifed.')
@click.argument('args', nargs=-1)
def sync_info_or_run_command(args):
	if len(args) is 0:
		click.secho('sync type', fg='cyan', nl=False)
		click.echo(': {}'.format(control.config['sync_type']))
		click.secho('sync remote', fg='cyan', nl=False)
		click.echo(': {}'.format(control.config['sync_remote']))
	else:
		control.sync_command(*args)


@cli.command('[-', help='discard last changes to dot(s).')
@click.argument('paths', nargs=-1, required=True)
def discard_changes(paths):
	for path in paths:
		control.current_profile.get_dot(path).link_back(overwrite=True)
