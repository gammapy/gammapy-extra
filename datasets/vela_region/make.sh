# Analysis Parameters
RA=128.836063542
DEC=-45.176431806
GLAT=-2.78733656284
GLON=263.552038198
EMIN=10000
EMAX=500000
ZMAX=100

# Files
EVENTS_LIST=events_list.txt
EVENTS=events_vela.fits
COUNTS=counts_vela.fits
SPACECRAFT=spacecraft.fits
LIVETIME=livetime_vela.fits
EXPOSURE=exposure_vela.fits
BACKGROUND=background_vela.fits
MODEL=background_model.xml
BACKGROUND2=total_vela.fits
MODEL2=total_model.xml

gtselect infile=$EVENTS_LIST outfile=$EVENTS 
         ra=$RA dec=$DEC 
         rad=5 tmin=239587200 tmax=397353600 emin=$EMIN 
         emax=$EMAX zmax=$ZMAX 

gtmktime scfile=$SPACECRAFT filter="DATA_QUAL>0 && LAT_CONFIG==1 && ABS(ROCK_ANGLE)<52" 
         roicut=no evfile=$EVENTS outfile=$EVENTS clobber=True

gtbin algorithm=CCUBE evfile=$EVENTS outfile=$COUNTS 
      scfile=$SPACECRAFT nxpix=50 nypix=50 binsz=0.1 
      xref=$GLON yref=$GLAT axisrot=0 proj=CAR coordsys=GAL 
      ebinalg=LOG emin=$EMIN emax=$EMAX enumbins=20 

gtltcube zmax=$ZMAX evfile=$EVENTS scfile=$SPACECRAFT 
         outfile=$LIVETIME dcostheta=0.25 binsz=2 

gtexpcube2 infile=$LIVETIME cmap=$COUNTS 
           outfile=$EXPOSURE irf=P7REP_CLEAN_V15 

gtmodel srcmaps=$COUNTS bexpmap=$EXPOSURE 
         expcube=$LIVETIME srcmodel=$MODEL 
         irfs=P7REP_CLEAN_V15 outfile=$BACKGROUND 

gtmodel srcmaps=$COUNTS bexpmap=$EXPOSURE 
         expcube=$LIVETIME srcmodel=$MODEL2 
         irfs=P7REP_CLEAN_V15 outfile=$BACKGROUND2 

gtpsf expcube=$LIVETIME outfile=vela_psf.fits irfs=P7REP_CLEAN_V15 
      ra=$RA dec=$DEC emin=$EMIN emax=$EMAX 
      nenergies=20 thetamax=10 ntheta=300 
