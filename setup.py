from setuptools import setup


setup(
    name='angelikahub',
    version='0.1',
    description="Hub for the Angelika project",
    author='David, Torgeir',
    author_email='davidjh@stud.ntnu.no, torgehaa@stud.ntnu.no',
    url="https://github.com/torgeha/angelika-hub",
    packages = ['hub.src.hub', 'hub.src.hub.sensors', 'withings', 'withings.withings'],
    install_requires = ['requests'],
    keywords="angelikahub",
)