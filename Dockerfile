# This is the Dockerfile to run Gammapy on Binder
#

FROM continuumio/miniconda3:4.3.27p0
MAINTAINER Gammapy developers <gammapy@googlegroups.com>

# compilers
RUN apt-get install -y build-essential

# install dependencies
RUN conda config --add channels conda-forge
RUN conda config --add channels astropy
RUN conda config --add channels sherpa

RUN conda install -q -y python==3.6
RUN conda install -q -y cython>=0.27
RUN conda install -q -y numpy>=1.13
RUN conda install -q -y astropy
RUN conda install -q -y uncertainties
RUN conda install -q -y scipy>=0.19.1
RUN conda install -q -y scikit-image
RUN conda install -q -y matplotlib>=2.0
RUN conda install -q -y astropy>=2.0
RUN conda install -q -y regions>=0.2
RUN conda install -q -y reproject
RUN conda install -q -y iminuit
RUN conda install -q -y healpy
RUN conda install -q -y photutils
RUN conda install -q -y aplpy
RUN conda install -q -y pyyaml
RUN conda install -q -y sherpa>=4.9.1
RUN conda install -q -y click

# install good version of Jupyter notebook
RUN pip install --no-cache-dir notebook==5.*

# install last version of gammapy
RUN /bin/bash -c "git clone https://github.com/gammapy/gammapy.git && \
                  cd gammapy && \
                  python setup.py install"

# add gammapy user running the jupyter notebook process
ENV NB_USER gammapy
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

# start Jupyter server in home dir
WORKDIR ${HOME}

# env vars used in notebooks for gammapy user
ENV GAMMAPY_EXTRA /home/${NB_USER}
