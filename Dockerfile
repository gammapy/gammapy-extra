# This is the Dockerfile to run Gammapy on Binder
#

FROM continuumio/miniconda3
MAINTAINER Gammapy developers <gammapy@googlegroups.com>

# compilers
RUN apt-get update && apt-get install -y build-essential

# install good version of notebook for Binder
RUN pip install --no-cache-dir notebook==5.*

# install dependencies - including the dev version of Gammapy
COPY environment.yml binder.py tmp/
WORKDIR tmp/
RUN conda install -q -y pyyaml
RUN python binder.py

# add gammapy user running the jupyter notebook process
ENV NB_USER gammapy
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# copy repo in /home/gammapy
COPY . ${HOME}

# setting ownerships
USER root
RUN chown -R ${NB_UID} ${HOME}

# start Jupyter server in notebooks dir
USER ${NB_USER}
WORKDIR ${HOME}/notebooks

# env vars used in notebooks
ENV GAMMAPY_EXTRA /home/${NB_USER}
