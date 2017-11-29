# This is the Dockerfile to run Gammapy on Binder
#

FROM continuumio/miniconda3:4.3.27p0
MAINTAINER Gammapy developers <gammapy@googlegroups.com>

# compilers
RUN apt-get install -y build-essential

# install dependencies, including the dev version of Gammapy
RUN conda env create -f environment.yml
RUN source activate gammapy-tutorial

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

# start Jupyter server in notebooks dir
WORKDIR ${HOME}/notebooks

# env vars used in notebooks for gammapy user
ENV GAMMAPY_EXTRA /home/${NB_USER}
