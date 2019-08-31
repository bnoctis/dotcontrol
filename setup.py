from setuptools import setup, find_packages


setup(
	name='dotcontrol',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'.c=dotcontrol.cli:cli'
		]
	}
)
