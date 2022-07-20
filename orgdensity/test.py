import os
import time
from typing import Optional

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from dash.dependencies import Input, Output

from client import LindasClient
from utils import plot_streets_heatmap, plot_switzerland

client = LindasClient("https://ld.admin.ch/query")

muni_id = 4001
streets = client.get_streets(muni_id)

for i, street in enumerate(streets):

    print(i, street)
    companies = client.get_companies_on_street(muni_id, street)
    time.sleep(1)
    # print(companies)

