from gammapy.data import ObservationTable


intable = ObservationTable.read('observation_table.fits')

for row in intable:
    infile = row['PHAFILE']
    phafile = infile.split('/')[-1]
    outfile = '$GAMMAPY_EXTRA/datasets/hess-crab4_pha/ogip_data/{}'.format(phafile)
    row['PHAFILE'] = outfile

intable.write('observation_table.fits', overwrite=True)
