import numpy as np
import pandas as pd


def join_data(colorado, california, newjersey,florida, socio_economic):
    # def combine_tables():
    table1 = colorado()
    table2 = california()
    table3 = newjersey()
    table4 = florida()
    socioecon = socio_economic()

    join_cocanjfl = pd.concat([table1, table2, table3, table4])
    join_cocanjfl = join_cocanjfl.reset_index()
    join_cocanjfl = join_cocanjfl.drop(['index'], axis=1)

    socio_pollute = socioecon.merge(join_cocanjfl, how="left", on="county")

    print(socio_pollute.head())
    return socio_pollute


if __name__ == '__main__':
    from co_data import get_data as colorado
    from ca_data import get_data as california
    from nj_data import get_data as newjersey
    from fl_data import get_data as florida
    from us_data import get_data as socio_economic
    join_data(colorado, california, newjersey,florida, socio_economic)
