In this repos there are the cube fits file necessary for a spectral 3D analysis:
-counts_cube.fits: counts for all the reco energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab

-bkg_cube.fits: bkg counts for all the reco energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab

-exposure_cube.fits: exposure for all the reco energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab. You use this cube if you don't take into consideration an energy resolution for the 3D spectral analysis

-psf_cube.fits: mean psf of the 4 Crab runs for all the reco energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab. You use this cube if you don't take into consideration an energy resolution for the 3D spectral analysis

-exposure_cube_etrue.fits: exposure for all the true energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab. You use this cube if you take into consideration an energy resolution for the 3D spectral analysis

-psf_cube_etrue.fits: mean psf of the 4 Crab runs for all the true energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab. You use this cube if you take into consideration an energy resolution for the 3D spectral analysis

-rmf.fits: mean rmf of the 4 Crab runs. This is a `~gammapy.irf.EnergyDispersion` object

-significance_cube.fits: signifiance for all the reco energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab

-excess_cube.fits: excess for all the reco energies in a (50,50) pixel images. One pixel is 0.02deg znd the images is center on the Crab

There is also the script make.py that made these cubes from the dataset in $GAMMAPY_EXTRA/datasets/hess-crab4-hd-hap-prod2. You create a new dataset in /data with an hdu table that contains a link to the acceptance curve to use for each run situated in the directory /background in order to create a FOV bacground model.
For the moment you create your acceptance curves based on the 4 test Crab runs from the counts outside the exclusion regions. This is not physical. When the data will be available, the background model will be based on around 8000 AGN runs.
