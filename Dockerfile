FROM andrewosh/binder-base

MAINTAINER adonath <axel.donath@mpi-hd.mpg.com>

USER main

RUN conda config --add channels astropy --add channels sherpa
RUN conda install pyyaml
RUN conda install sherpa
RUN pip install regions
RUN pip install healpy
RUN pip install reproject
RUN pip install photutils
RUN pip install wcsaxes
RUN pip install aplpy
RUN pip install naima
RUN pip install iminuit
RUN pip install uncertainties
RUN pip install git+https://github.com/gammapy/gammapy.git#egg=gammapy

ENV GAMMAPY_EXTRA $HOME/notebooks
#ENV OPTS= "$OPTS --NotebookApp.default_url=/notebooks/notebooks/index.ipynb "

# Install requirements for Python 3
# This doesn't work, that pip isn't available
#RUN /home/main/anaconda/envs/python3/bin/pip install gammapy regions wcsaxes
