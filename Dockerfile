# This is the Dockerfile to run Gammapy on Binder
#
# - Installation is for Python 3 using Anaconda
# - TODO: if possible, don't give users the option to
#   select Python 2 kernel on Binder

FROM andrewosh/binder-python-3.5
MAINTAINER Gammapy developers <gammapy@googlegroups.com>
USER main

RUN conda config --add channels conda-forge
RUN conda config --add channels astropy
RUN conda config --add channels sherpa

# RUN conda create -y --name gammapy-env python=3 anaconda
# RUN /bin/bash -c "source activate gammapy-env"

# Check if we're using the right Python, pip and conda
RUN which python
RUN python --version
RUN which pip
RUN which conda

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

# RUN pip install --no-deps gammapy regions wcsaxes
RUN pip install --no-deps uncertainties
RUN pip install --no-deps git+https://github.com/gammapy/gammapy.git#egg=gammapy

ENV GAMMAPY_EXTRA $HOME/notebooks
#ENV OPTS= "$OPTS --NotebookApp.default_url=/notebooks/notebooks/index.ipynb "

# Check if things look OK
RUN which python
RUN python --version
RUN python -c 'import gammapy; print(gammapy.__version__)'
