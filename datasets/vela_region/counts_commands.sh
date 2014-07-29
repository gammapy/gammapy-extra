EVENTS_LIST=events_list.txt
EVENTS=events.fits
COUNTS=counts_cube.fits
SPACECRAFT=spacecraft.fits

gtselect infile=$EVENTS_LIST outfile=$EVENTS \
         ra=135.528583 dec=-40.554694 \
         rad=1 tmin=239587200 tmax=397353600 emin=50 \
         emax=500000 zmax=105 \

gtbin algorithm=CCUBE evfile=$EVENTS outfile=$COUNTS \
      scfile=$SPACECRAFT nxpix=50 nypix=50 binsz=0.1 \
      xref=263.05836967702709 yref=3.9298511274632784 axisrot=0 proj=CAR coordsys=GAL \
      ebinalg=LOG emin=10000 emax=500000 enumbins=3 \


