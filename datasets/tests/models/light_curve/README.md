# Light curve model example file

This is one light curve model example file from the CTA first data challenge.

The model is given by `TeV_J1224+2122` from `model_agn.xml`, copied to `model.xml` here.
The curve is given as a table in `lightcrv_PKSB1222+216.fits`.

This is a format that was introduced by Gammalib, it is described a bit here:

* http://cta.irap.omp.eu/gammalib-devel/users/user_manual/modules/model.html#light-curve
* http://cta.irap.omp.eu/gammalib-devel/doxygen/classGModelTemporalLightCurve.html

The description says that linear interpolation in time should be used, so we'll do the same in Gammapy.
