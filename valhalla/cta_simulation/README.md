# CTA simulation

This directory contains a copy of some code that was
removed from Gammapy, because we want to make room
for rewriting this functionality and the tutorial notebook in a better way.

Note that one option for you could be to use Gammapy v0.7.
This will always remain as-is and as it was working.

* Docs: http://docs.gammapy.org/0.7/
* Code: https://github.com/gammapy/gammapy/tree/v0.7

If you want to import and use the code from here, you can add this folder
to your `$PYTHONPATH` and change the import line in your scripts or
notebooks, e.g. from this:

    from gammapy.scripts.cta_utils import CTAObservationSimulation

to this:

    from cta_utils import CTAObservationSimulation

and that will give you the `cta_utils.py` file from this folder.

The code here is a copy of the `cta_utils.py` and `cta_irf` files,
the exact version before it was removed from Gamampy.

For more information, see https://github.com/gammapy/gammapy/issues/1551

Comment by Christoph: Overall I'm not sure how helpful this
`gammapy-extra/valhalla/cta_simulation` is, i.e. when you'd want to use it.
My recommendation would be that you either use Gammapy v0.7 for your study / publication,
or if you need to update for some reason, rewrite your scripts or notebooks
using the better code we have developed in Gammapy, i.e. use v0.8 or v0.9.
Please do report any issues or problems or missing features - we want to help!
