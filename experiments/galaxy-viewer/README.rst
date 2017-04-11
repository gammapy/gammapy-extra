Galaxy Viewer
=============

What is this?
-------------

This is a prototype 3-dimensional interactive gamma-ray Milky Way viewer
using `OpenGL`_ via `vispy`_ implemented at the `EuroScipy 2014`_ sprint
by Rob Reilink (@rreilink) and Christoph Deil (@cdeil).

How do I run this?
------------------

To run it simply install `vispy`_ and `QT`_ and then on the command line run
this command which will open up a QT window and display an interactive Galaxy::

   $ python run.py

To produce different example input Galactic source catalogs, install
`Gammapy`_ and then modify and run this script::

   $ python make_sources.py

TODO
----

This is a one-day hack ... for this to become a nice demo the following
improvements should be implemented:

* Nice 3d navigation
    - check out how e.g. `Stellarium`_ or `astrorank`_ do the navigation.
    - could be done with mouse events, e.g. using shift to change between
      rotation and 3d movement.
* Draw coordinate system (lon, lat) or Galactic (x, y, z)
   - Should be done as a separate "program" (kind of a separate layer)
   - A lot of work ... every little thing has to be drawn individually
* Add controls
   - there could e.g. be colormap controls or a time slider or ...
   - have to commit to making a QT app or e.g. an ipython notebook
     ... or make a web page with javascript controls so that it can
     be shared on the web?
   - pretty easy to implement and layout for a QT app.
* Display images
   - Examples that display images on a sphere are:
       - `thecmb`_ looking at the sphere from the outside ...
         this could be very nice for the sun or earth
       - `astrorank`_ looking at the sphere from the inside ...
         this could be very nice e.g. for `Fermi allsky`.
   - Use scenegraph texture visual to transform between (u, v)
     pixel coordinates in the image and (x, y) coordinate on the screen.


Notes
-----

Here's a collection of useful links:

* http://www.astronexus.com/hyg
* https://developer.apple.com/opengl/

.. _Fermi allsky: http://fermi.gsfc.nasa.gov/ssc/observations/types/allsky/
.. _thecmb: http://www.thecmb.org/
.. _astrorank: http://www.asterank.com/3d/
.. _Gammapy: https://github.com/gammapy/gammapy
.. _OpenGL: http://www.opengl.org/
.. _Stellarium:  http://www.stellarium.org/
.. _QT: http://qt-project.org/
.. _vispy: http://vispy.org/
.. _EuroScipy 2014: https://www.euroscipy.org/2014/
.. _galaxy demo: http://vispy.org/examples/demo/gloo/galaxy.html
