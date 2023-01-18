import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

data = pd.read_csv("###Your DataFrame###", encoding="###If you have###")
data['checkouttime'] = pd.to_datetime(data['checkouttime'])

#creates a time axis
time_data = data[['checkouttime','lat','lon','ID','checkoutplace','amount']]
time_data = time_data.rename(columns={'checkouttime':'time','lat':'latitude','lon':'longitude'})
time_data['time'] = time_data['time'].dt.strftime('%Y-%m-%d %H:%M')
time_data = time_data[['time','latitude','longitude','ID','checkoutplace','amount']]

#Folium Map
m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=13)



#add transaction information to the time
time_data['time'] = pd.to_datetime(time_data['time'])
max_time = pd.to_datetime(time_data.time.max())

print(time_data['time'])
print(max_time)
timestamped_geo_json = TimestampedGeoJson(
                        {'type': 'FeatureCollection',
                        'features': [{
                        'type': 'Feature',
                        'geometry': {
                        'type': 'Point',
                        'coordinates': [row["longitude"], row["latitude"]],
                        },
                        'properties': {
                        'id': row["ID"],
                        'time': row["time"].strftime('%Y-%m-%d %H:%M'),
'popup': row["ID"] + '<br>' + row["ckeckouttime"] + '<br>' + row["time"].strftime("%Y-%m-%d %H:%M") + '<br>' + row["amount"],
                        'style': {'fillColor': '#0000ff', 'color': '#0000ff', 'weight': 2} if (max_time - row["time"]).seconds <= 1800 else {'fillColor': '#ff0000', 'color': '#ff0000', 'weight': 2}
                        } }
                        for i, row in time_data.iterrows()
                        ]},
                        period='PT1H', #If you want minitus, PT10M or PT30M.
                        add_last_point=True,
                        auto_play=True,
                        loop=True,
                        max_speed=0.5,
                        loop_button=True,
                        date_options='YYYY-MM-DD　HH:mm',
                        time_slider_drag_update=True
                        )

m.add_child(timestamped_geo_json)

#display map
m
m.save('map1.html')
