"""Make SNRcat FITS table.
"""
from gammapy.catalog import SourceCatalogSNRcat


cat = SourceCatalogSNRcat()

print(cat.info('stats'))

# TODO: fix this issue, then continue
# https://github.com/gammapy/gammapy/issues/670

# Add snrcat_id field that's used as part of the URL to link to SNRcat
# snrcat_id = []
# for source in table:
#     if source['GLAT'] > 0:
#
#     glat_sign = ['p' fortable['GLAT']
#                  table['snrcat_id'] = [
#         'G{:05.1f}{}{03.1f}'.format(l, s, b)
#         for (l, s, b) in zip(table['GLON'], glat_sign, table['GLAT'])
#         ]
