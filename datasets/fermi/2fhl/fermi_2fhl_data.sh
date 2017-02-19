# This is as script to prepare Fermi 2FHL all sky data

# Basic analysis Parameters
EMIN=50000
EMAX=2000000
ZMAX=105
EVENT_CLASS=128
EVENT_TYPE=3
IRF=P8R2_SOURCE_V6 # Corresponding to event type 128
EBINALG=LOG

# Time cuts taken from reference event list, another reference is missing.
TMIN=239557702.597728
TMAX=444440996.314882

# WCS parameters for HGPS region, can be changed later to all sky
NXPIX=9400
NYPIX=500
BINSZ=0.02
PROJ=CAR
XREF=341
YREF=0
COORDSYS=GAL
NEBINS=5

# Raw data files, to be set by the user
#PHOTON_FILES=
#SPACECRAFT=

PHOTON_FILES_LIST=fermi_2fhl_filelist.txt
find $PHOTON_FILES -name lat_photon_weekly* > $PHOTON_FILES_LIST

# Data files
EVENTS=events/fermi_2fhl_events_all.fits
EVENTS_SELECTED=events/fermi_2fhl_events_selected.fits
EVENTS_SELECTED_GTI=events/fermi_2fhl_events.fits
LIVETIME=fermi_2fhl_livetime.fits
EXPOSURE=fermi_2fhl_exposure.fits
COUNTS=fermi_2fhl_counts.fits
PSF=fermi_2fhl_psf_gc.fits

# Merge weekly photon files and apply energy cut
gtselect evclass=INDEF evtype=INDEF infile=@$PHOTON_FILES_LIST outfile=$EVENTS \
         ra=0 dec=0 rad=180 tmin=$TMIN tmax=$TMAX zmax=180 emin=$EMIN emax=$EMAX

# Select events by event class and apply zmax cut
gtselect infile=$EVENTS outfile=$EVENTS_SELECTED \
         ra=0 dec=0 rad=180 evclass=$EVENT_CLASS evtype=$EVENT_TYPE \
         tmin=INDEF tmax=INDEF zmax=$ZMAX emin=$EMIN emax=$EMAX

# Update GTI list
gtmktime scfile=$SPACECRAFT filter="(DATA_QUAL>0)&&(LAT_CONFIG==1)" \
         roicut=no evfile=$EVENTS_SELECTED outfile=$EVENTS_SELECTED_GTI

# Compute livetime cube
gtltcube zmax=$ZMAX evfile=$EVENTS_SELECTED_GTI scfile=$SPACECRAFT \
         outfile=$LIVETIME dcostheta=0.025 binsz=1

# Compute counts cube
gtbin algorith=CCUBE evfile=$EVENTS_SELECTED_GTI outfile=$COUNTS scfile=$SPACECRAFT \
        nxpix=$NXPIX nypix=$NYPIX binsz=$BINSZ proj=$PROJ xref=$XREF yref=$YREF \
        coordsys=$COORDSYS ebinalg=$EBINALG emin=$EMIN emax=$EMAX enumbins=$NEBINS \
        axisrot=0

# Compute exposure cube
gtexpcube2 infile=$LIVETIME outfile=$EXPOSURE irf=$IRF cmap=none \
        nxpix=$NXPIX nypix=$NYPIX binsz=$BINSZ proj=$PROJ xref=$XREF yref=$YREF \
        coordsys=$COORDSYS ebinalg=$EBINALG emin=$EMIN emax=$EMAX enumbins=$NEBINS \
        axisrot=0 bincalc=EDGE

# Compute psf cube
gtpsf expcube=$LIVETIME outfile=$PSF irfs=$IRF ra=266.42 dec=-29.01 \
emin=$EMIN emax=$EMAX nenergies=$NEBINS thetamax=10 ntheta=300

# Zip files
gzip $EVENTS_SELECTED_GTI
gzip $COUNTS
gzip $EXPOSURE
gzip $LIVETIME
gzip $PSF

