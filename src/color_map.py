import csv
from bs4 import BeautifulSoup
# from data import make_fips_dicts
# from data import choose_states
from data import asthma_ca
from data import asthma_co
from data import asthma_fl
from data import asthma_nj




# Read in asthma rates
# nj = asthma_nj()[1]
# d = nj.set_index('fips').to_dict()['asthma_rate']

# ca = asthma_ca()[1]
# d = ca.set_index('fips').to_dict()['asthma_rate']

co = asthma_co()[1]
d = co.set_index('fips').to_dict()['asthma_rate']


# fl = asthma_fl()[1]
# d = fl.set_index('fips').to_dict()['asthma_rate']

#
# reader = csv.reader(open('unemployment09.csv'), delimiter=",")
# for row in reader:
#     try:
#         fips = asthma_nj()[1]['fips']
#         rate = asthma_nj()[1]['asthma_rate']
#         asthma[fips] = rate
#     except:
#         pass

# Load the SVG map
svg = open('../data/counties.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

# Find counties
paths = soup.findAll('path')

# Map colors
# colors = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"]
colors = ["#fff7f3", "#fde0dd", "#fcc5c0", "#fa9fb5", "#f768a1", "#dd3497", "#ae017e", "#7a0177", "#49006a"]




# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1; stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt; marker-start:none;stroke-linejoin:bevel;fill:'

# Color the counties based on unemployment rate
for p in paths:

    if p['id'] not in ["State_Lines", "separator"]:
        # pass
        try:
            rate = d[p['id']]
        except:
            continue

        if rate > 80:
            color_class = 8
        elif rate > 70:
            color_class = 7
        elif rate > 60:
            color_class = 6
        elif rate > 50:
            color_class = 5
        elif rate > 40:
            color_class = 4
        elif rate > 30:
            color_class = 3
        elif rate > 20:
            color_class = 2
        elif rate > 10:
            color_class = 1
        else:
            color_class = 0

        color = colors[color_class]
        p['style'] = path_style + color

# Output map
print (soup.prettify())
