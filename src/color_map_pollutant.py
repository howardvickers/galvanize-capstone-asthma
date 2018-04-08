import csv
from bs4 import BeautifulSoup
from cairosvg import svg2png

# from data import make_fips_dicts
# from data import choose_states
from data import asthma_ca
from data import asthma_co
from data import asthma_fl
from data import asthma_nj
from data import all_socio_econ_data

_, fips_lookup = all_socio_econ_data()
fips_feature_dict = fips_lookup.set_index('fips').to_dict()

fips_lookup_co = fips_lookup[fips_lookup.state == 'colorado']
fips_feature_dict_co = fips_lookup_co.set_index('fips').to_dict()

chart_list = ['obese_adult', 'smoke_adult', 'uninsured', 'air_poll_partic', 'unemployment']
# colors from http://colorbrewer2.org
colors_dict = { 'obese_adult'       : ["#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"],
                'smoke_adult'       : ["#fcfbfd", "#efedf5", "#dadaeb", "#bcbddc", "#9e9ac8", "#807dba", "#6a51a3", "#54278f", "#3f007d"],
                'uninsured'         : ["#fff5eb", "#fee6ce", "#fdd0a2", "#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#a63603", "#7f2704"],
                'air_poll_partic'   : ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"],
                'unemployment'      : ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"]
                }

# Load the SVG map
svg = open('static/images/co_counties_blank.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

# Find counties
paths = soup.findAll('path')

# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1; stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt; marker-start:none;stroke-linejoin:bevel;fill:'

# create each map
for feature in chart_list:
    # d = fips_feature_dict[feature]
    d = fips_feature_dict_co[feature]

    # get colors for this map
    colors = colors_dict[feature]

    # find min and max values
    key_min = min(d.keys(), key=(lambda k: d[k]))
    val_min = d[key_min]
    key_max = max(d.keys(), key=(lambda k: d[k]))
    val_max = d[key_max]

    # calculate 10% steps
    val_10 = val_min + (val_max-val_min)*1/10
    val_20 = val_min + (val_max-val_min)*2/10
    val_30 = val_min + (val_max-val_min)*3/10
    val_40 = val_min + (val_max-val_min)*4/10
    val_50 = val_min + (val_max-val_min)*5/10
    val_60 = val_min + (val_max-val_min)*6/10
    val_70 = val_min + (val_max-val_min)*7/10
    val_80 = val_min + (val_max-val_min)*8/10
    val_90 = val_min + (val_max-val_min)*9/10

    # color the counties based on feature rate
    for p in paths:

        if p['id'] not in ["State_Lines", "separator"]:
            # pass
            try:
                rate = d[p['id']]

            except:
                continue

            if rate > val_90:
                color_class = 8
            elif rate > val_80:
                color_class = 7
            elif rate > val_70:
                color_class = 6
            elif rate > val_60:
                color_class = 5
            elif rate > val_40:
                color_class = 4
            elif rate > val_30:
                color_class = 3
            elif rate > val_20:
                color_class = 2
            elif rate > val_10:
                color_class = 1
            else:
                color_class = 0

            color = colors[color_class]
            p['style'] = path_style + color

    # Output and save each map
    mymap = soup.prettify()
    filename = 'static/images/co_{}.svg'.format(feature)
    open(filename, 'w').write(mymap)

    # svg2png(bytestring=mymap,write_to='static/images/co_{}.png')
