class ATNF(object):

    """ATNF pulsar catalog"""
    files = dict(version='ATNF_version.txt',
                 parameters='ATNF_parameters.txt',
                 data='ATNF_data.txt',
                 fits='ATNF_data.fits',
                 main='ATNF.fits',
                 good_ones='ATNF_good_ones.fits',
                 gps='ATNF_gps.fits',
                 latex='ATNF.tex')

    def make(self):
        logging.info('Making ATNF')
        # self.download()
        # self.fits()
        self.main()
        # self.good_ones()
        # self.gps_select(self.files['good_ones'], self.files['gps'])
        # self.write_mysql(self.files['gps'], table_name='ATNF')

    def download(self):
        """Download ATNF pulsar catalog data and software and compile it.
        I prefer executing these steps by hand, these are just my written
        notes how to do it."""
        logging.info('ATNF.download')
        url = 'http://www.atnf.csiro.au/research/pulsar/psrcat/psrcat_pkg.tar.gz'
        logging.info('Execute the following steps by hand to update the ATNF catalog:')
        logging.info('cd %s' % os.getcwd())
        logging.info('wget %s' % url)
        logging.info('tar zxvf psrcat_pkg.tar.gz')
        logging.info('cd psrcatPackage')
        logging.info('makeit')
        logging.info('Now you can use the psrcat tool to query the catalog,'
                     'Use ./psrcat -h to see available options.')

    def fits(self):
        """Convert all catalog info to FITS format"""
        logging.info('ATNF.fits')
        tool = './psrcatPackage/psrcat'
        tool += ' -db_file ./psrcatPackage/psrcat.db'
        cols = 'PSRJ PSRB NAME '
        cols += 'RAJ DECJ PMRA PMDEC RAJD DECJD GL GB PML PMB '
        cols += 'DM P0 P1 BINARY DIST_DM DIST_A DIST DIST1 RADDIST '
        cols += 'SURVEY ASSOC TYPE DATE OSURVEY '
        cols += 'AGE AGE_I BSURF_I EDOT_I EDOTD2 PMTOT VTRANS BSURF B_LC EDOT'
        os.system('%s -v > %s' % (tool, self.files['version']))
        os.system('%s -p > %s' % (tool, self.files['parameters']))
        os.system('echo "# %s" > %s' % (cols, self.files['data']))
        os.system('%s -o short -c "%s"'
                  ' -nonumber -nohead'  # -null null
                  # ' | egrep -v "unknown survey|---|(hms)"'
                  ' | egrep -v "unknown survey"'
                  ' | sed "s/*/null/g" >> %s' %
                  (tool, cols, self.files['data']))

    def main(self):
        logging.info('ATNF.main')
        cmd = ['addcol Source_Name "NAME"']
        cmd.append('addcol RAJ2000 "radiansToDegrees(hmsToRadians(RAJ))"')
        cmd.append('addcol DEJ2000 "radiansToDegrees(dmsToRadians(DECJ))"')
        cmd.append('addskycoords icrs galactic RAJ2000 DEJ2000 GLON GLAT')
        # TODO: Add meta info
        # Add version info
        # lines = file(self.files['version']).readlines()
        # software_version, catalog_version = [_.split()[-1] for _ in lines]
        # cmd.append('meta SW "%s"' % software_version)
        # cmd.append('setparam asdf %s' % software_version)
        tpipe(self.files['fits'], self.files['main'],
              cmd, verbose=self.verbose)

