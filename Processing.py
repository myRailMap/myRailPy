import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cartopy.io.img_tiles import OSM
from datetime import datetime

from journeys import get_line
from stations import get_stations_df, is_supported_station

stations = get_stations_df()

data = pd.read_csv('data.csv', parse_dates=["Departure (Local)", "Arrival (Local)"])
data = data[data["Departure (Local)"] <= datetime.now()]

data["origin_slug"] = data.Origin.str.lower().str.replace(" ", "-").str.replace("’", "").str.replace("'", "")
data["origin_slug"] = data.origin_slug.str.replace("ü", "u").str.replace("/", "-").str.replace("ä", "a")
data["origin_slug"] = data.origin_slug.str.replace("ö", "o").str.replace("é", "e").str.replace("è", "e")
data["origin_slug"] = data.origin_slug.str.replace("à", "a").str.replace("ç", "c").str.replace("ù", "u")
data["origin_slug"] = data.origin_slug.str.replace("â", "a").str.replace("ê", "e").str.replace("î", "i")
data["origin_slug"] = data.origin_slug.str.replace("(", "", regex=False).str.replace(")", "", regex=False)
data["destination_slug"] = data.Destination.str.lower().str.replace(" ", "-").str.replace("’", "").str.replace("'", "")
data["destination_slug"] = data.destination_slug.str.replace("ü", "u").str.replace("/", "-")
data["destination_slug"] = data.destination_slug.str.replace("ö", "o").str.replace("é", "e").str.replace("è", "e")
data["destination_slug"] = data.destination_slug.str.replace("à", "a").str.replace("ç", "c").str.replace("ù", "u")
data["destination_slug"] = data.destination_slug.str.replace("â", "a").str.replace("ê", "e").str.replace("î", "i")
data["destination_slug"] = data.destination_slug.str.replace("(", "", regex=False).str.replace(")", "", regex=False)

data['dep_lat'] = data['origin_slug'].map(stations.set_index('slug')['latitude'])
data['dep_lon'] = data['origin_slug'].map(stations.set_index('slug')['longitude'])
data['dest_lat'] = data['destination_slug'].map(stations.set_index('slug')['latitude'])
data['dest_lon'] = data['destination_slug'].map(stations.set_index('slug')['longitude'])

stations_visited = pd.concat([data["origin_slug"], data["destination_slug"]]).drop_duplicates().to_frame().rename(
    columns={0: "slug"})
stations_visited["latitude"] = stations_visited["slug"].map(stations.set_index('slug')['latitude'])
stations_visited["longitude"] = stations_visited["slug"].map(stations.set_index('slug')['longitude'])
stations_visited["name"] = stations_visited["slug"].map(stations.set_index('slug')['name'])
stations_visited = stations_visited.dropna()

journeys_to_plot = data[['origin_slug', 'destination_slug']].drop_duplicates()
journeys_to_plot = pd.DataFrame(journeys_to_plot.apply(np.sort, axis=1).to_list()).drop_duplicates().sort_values(
    by=0).dropna().reset_index()

imagery = OSM()
fig = plt.figure(dpi=500)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([-2, 18, 42, 54], ccrs.PlateCarree())
ax.add_image(imagery, 5)
for index, row in journeys_to_plot.iterrows():
    print(f"Plotting journey {index + 1}/{journeys_to_plot.shape[0]} from {row[0]} to {row[1]}")
    if is_supported_station(row[0]) and is_supported_station(row[1]):
        line = np.array(get_line(row[0], row[1]))
        ax.plot(line[:, 0], line[:, 1], color="red", linewidth=1, zorder=1)
ax.scatter(stations_visited["longitude"], stations_visited["latitude"], s=10, zorder=2, color="blue")

plt.show()
