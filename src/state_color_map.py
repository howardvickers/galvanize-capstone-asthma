import csv
from bs4 import BeautifulSoup
import time


def create_map(state_data):

    a = state_data.set_index('fips').to_dict()
    d = a['pred']

    print('This is the dictionary for the state_pred_map: ', d)

    # load SVG map
    svg = open('static/images/co_counties_blank.svg', 'r').read()

    # load into Beautiful Soup
    soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

    # find counties
    paths = soup.findAll('path')

    # map colors
    # colors = ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"]
    colors = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"]

    # county style
    path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1; stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt; marker-start:none;stroke-linejoin:bevel;fill:'

    # color the counties based on asthma rate
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


    ts = time.time()
    print(ts)
    # output map
    mymap = soup.prettify()
    state_pred_map = 'static/images/state_pred_map_{}.svg'.format(ts)
    open(state_pred_map, 'w').write(mymap)
    return state_pred_map
