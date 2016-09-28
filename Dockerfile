FROM andrewosh/binder-base

MAINTAINER adonath <axel.donath@mpi-hd.mpg.com>

USER main

RUN conda config --add channels conda-forge
RUN conda config --add channels astropy
RUN conda config --add channels sherpa

RUN conda install -q -y pyyaml
RUN conda install -q -y sherpa
RUN conda install -q -y iminuit
RUN conda install -q -y healpy
RUN conda install -q -y regions
RUN conda install -q -y reproject
RUN conda install -q -y photutils
RUN conda install -q -y wcsaxes
RUN conda install -q -y aplpy
RUN conda install -q -y naima
RUN pip install --no-deps uncertainties
RUN pip install --no-deps git+https://github.com/gammapy/gammapy.git#egg=gammapy

ENV GAMMAPY_EXTRA $HOME/notebooks
#ENV OPTS= "$OPTS --NotebookApp.default_url=/notebooks/notebooks/index.ipynb "

# Install requirements for Python 3
# This doesn't work, that pip isn't available
#RUN /home/main/anaconda/envs/python3/bin/pip install gammapy regions wcsaxes
