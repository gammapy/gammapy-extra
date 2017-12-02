gammapy-extra
=============

The main `gammapy` repository is located at
https://github.com/gammapy/gammapy
and contains the code and Sphinx docs.

The `gammapy-extra` repository is located at
https://github.com/gammapy/gammapy-extra
and contains everything that is considered too large
in terms of filesize to be part of the main repo.

Currently we have the following folders:

* `datasets` : Gammapy example datasets
* `notebooks` : Gammapy IPython notebooks
* `logo` : Gammapy logo and banner

Jupyter notebooks stored in **notebooks** folder may be also found in the
`Gammapy documentation website <http://docs.gammapy.org/en/latest/tutorials.html>`__
as fixed-text Sphinx formatted files, as well as in the
`NBViewer platform <http://nbviewer.jupyter.org/github/gammapy/gammapy-extra/blob/master/index.ipynb>`__.


Binder
------

Try Gammapy online in Binder: https://mybinder.org/v2/gh/gammapy/gammapy-extra.git/binder

Controlled via ``Dockerfile`` in ``binder`` branch of this gammapy-extra repo.

In case you would like to chek the Binder Gammapy space with a modified ``Dockerfile``:

- Check in yout desktop the Docker image is built successfully running the following command in your ``gammapy-extra`` local folder: ``docker build -t gammapy-tutorial .``
- Go to https://mybinder.org
- Provide URL of your GitHub **fork and branch** 
- Click on launch bouton
- Follow the logs clicking on 'Build logs'

.. image:: http://mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/gammapy/gammapy-extra.git/binder
