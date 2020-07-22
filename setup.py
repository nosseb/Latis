from setuptools import setup

setup(
    name='Latis',
    version=0.1,
    description='A module to extract data from Latispro\'s .ltp files.',
    keywords='Latis ltp .ltp',
    author='Robinson Besson',
    author_email='robinson.besson@nosseb.fr',
    url='https://github.com/nosseb/Latis',
    packages=['Latis'],
    package_dir={'Latis': 'src'},
    install_requires=['xmltodict>=0.12.0'],
)
