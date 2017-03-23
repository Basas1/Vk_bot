from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='Vk_bot',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='G&A Dev',
    author_email='',
    description='Bot for social networking service vk.com',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=['requests', 'vk_api', 'selenium']
)
