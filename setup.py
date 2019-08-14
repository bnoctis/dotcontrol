from setuptools import setup
import dotcontrol


setup(
	name='dotcontrol',
	version=dotcontrol.__version__,
	description='a dot file manager',
	url='https://github.com/mwoyuan/dotcontrol.git',
	author='Mwo Yuan',

	py_modules=['dotcontrol'],
	python_requires='>=3.5',
	install_requires=['toml', 'click'],

	entry_points={
		'console_scripts': [
			'dot=dotcontrol:cli'
		]
	}
)
