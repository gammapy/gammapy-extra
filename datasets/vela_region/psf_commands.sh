LIVETIME=livetime_cube.fits

gtpsf expcube=$LIVETIME outfile=vela_psf.fits irfs=P7REP_CLEAN_V15 \
      ra=135.5285829 dec=-40.5546939 emin=10000 emax=500000 \
      nenergies=20 thetamax=10 ntheta=300 \
