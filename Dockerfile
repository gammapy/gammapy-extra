FROM andrewosh/binder-base

MAINTAINER adonath <axel.donath@mpi-hd.mpg.com>

USER main
# Install requirements for Python 2
RUN pip install gammapy regions wcsaxes

# Install requirements for Python 3
RUN /home/main/anaconda/envs/python3/bin/pip install gammapy regions wcsaxes
