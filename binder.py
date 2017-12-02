"""This script is executed from Dockerfile configuration file
It installs software dependencies declared in environment.yml
in the docker container built for the Binder service.
"""
import pip
import yaml
import sys
import conda.cli

with open("environment.yml") as stream:
    content = yaml.load(stream)

for chan in content['channels']:
    print("RUN conda config --add channels {}".format(chan))
    conda.cli.main('conda', 'config',  '--add', 'channels', chan)

for pack in content['dependencies']:
    if isinstance(pack, str):
        print("RUN conda install -q -y {}".format(pack))
        conda.cli.main('conda', 'install',  '-y', '-q', pack)
    else:
        print("RUN pip install {}".format(pack['pip'][0]))
        pip.main(["install", pack['pip'][0]])
