FROM andrewosh/binder-base

MAINTAINER adonath <axel.donath@mpi-hd.mpg.com>

USER main

RUN conda config --add channels conda-forge
RUN conda config --add channels astropy
RUN conda config --add channels sherpa

RUN conda install -q pyyaml
RUN conda install -q sherpa
RUN conda install -q iminuit
RUN conda install -q healpy
RUN conda install -q regions
RUN conda install -q reproject
RUN conda install -q photutils
RUN conda install -q wcsaxes
RUN conda install -q aplpy
RUN conda install -q naima
RUN pip install uncertainties
RUN pip install git+https://github.com/gammapy/gammapy.git#egg=gammapy

ENV GAMMAPY_EXTRA $HOME/notebooks
#ENV OPTS= "$OPTS --NotebookApp.default_url=/notebooks/notebooks/index.ipynb "

# Install requirements for Python 3
# This doesn't work, that pip isn't available
#RUN /home/main/anaconda/envs/python3/bin/pip install gammapy regions wcsaxes
