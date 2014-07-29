EVENTS=events.fits
COUNTS=counts_cube.fits
SPACECRAFT=spacecraft.fits
LIVETIME=livetime_cube.fits
EXPOSURE=exposure_cube.fits


gtltcube evfile=$EVENTS scfile=$SPACECRAFT \
         outfile=$LIVETIME dcostheta=0.25 binsz=2 \

gtexpcube2 infile=$LIVETIME cmap=$COUNTS \
           outfile=$EXPOSURE irf=P7REP_CLEAN_V15 \
