COUNTS=counts_cube.fits
LIVETIME=livetime_cube.fits
EXPOSURE=exposure_cube.fits
BACKGROUND=background_cube.fits
MODEL=model.xml

gtmodel srcmaps=$COUNTS bexpmap=$EXPOSURE \
         expcube=$LIVETIME srcmodel=$MODEL \
         irfs=P7REP_CLEAN_V15 outfile=$BACKGROUND \

