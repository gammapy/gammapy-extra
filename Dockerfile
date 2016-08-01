FROM andrewosh/binder-base

MAINTAINER adonath <axel.donath@mpi-hd.mpg.com>

USER main
# Install requirements for Python 2
RUN pip install gammapy regions wcsaxes

ENV GAMMAPY_EXTRA $HOME/notebooks
ENV OPTS= "$OPTS --NotebookApp.default_url=/notebooks/notebooks/index.ipynb "

# Install requirements for Python 3
# This doesn't work, that pip isn't available
#RUN /home/main/anaconda/envs/python3/bin/pip install gammapy regions wcsaxes
