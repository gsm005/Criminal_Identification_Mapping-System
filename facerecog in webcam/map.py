import webbrowser
import pandas as pd
import folium
from folium import FeatureGroup
from folium.plugins import MarkerCluster
import geocoder

#Create the base Map
m = folium.Map(location=[21.0000,78.0000], title='OurMap', zoom_start=5)

#Create the markers
markerCluster = MarkerCluster().add_to(m)
g = geocoder.ip('me')
ls=list(map(str,g.latlng))
lat =ls[0]
lang=ls[1]
folium.Marker(location=[lat, lang],popup='Current_location', icon=folium.Icon(color='red')).add_to(markerCluster)
m.save("index.html")
webbrowser.open('index.html')