
historical_circuit = [
    {'id': 1, 'name': 'Cotonou Dantokpa Market', 'description': 'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts and textiles', 'latitude': 6.3671, 'longitude': 2.4335},
    {'id': 2, 'name': 'Ouidah Museum of History', 'description': 'A museum that provides insights into the history of the slave trade in Benin', 'latitude': 6.3633, 'longitude': 2.0851},
    {'id': 3, 'name': 'Royal Palaces of Abomey', 'description': 'Historical palaces that were once the seat of the Kingdom of Dahomey', 'latitude': 7.1829, 'longitude': 1.9912},
    {'id': 4, 'name': 'Porto-Novo', 'description': 'The capital city of Benin, known for its colonial architecture and vibrant culture', 'latitude': 6.4969, 'longitude': 2.6289}
]



beach_circuit = [
    {'id': 1, 'name': 'Fidjrosse Beach', 'description': 'A beautiful sandy beach perfect for relaxation, swimming, and enjoying local seafood', 'latitude': 6.3650, 'longitude': 2.3758},
    {'id': 2, 'name': 'Cotonou Dantokpa Market', 'description': 'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts and textiles', 'latitude': 6.3671, 'longitude': 2.4335},
    {'id': 3, 'name': 'Ganvie Lake Village', 'description': 'A village built on stilts in Lake Nokoué, often referred to as the "Venice of Africa"', 'latitude': 6.4969, 'longitude': 2.4183},
    {'id': 4, 'name': 'Nokoué Lake', 'description': 'A large lake known for its biodiversity and the stilt village of Ganvie', 'latitude': 6.4833, 'longitude': 2.4167}
]



nature_circuit = [
    {'id': 1, 'name': 'Pendjari National Park', 'description': 'A UNESCO World Heritage site known for its wildlife, including elephants, lions, and hippos', 'latitude': 11.0416, 'longitude': 1.4141},
    {'id': 2, 'name': 'Tanougou Falls', 'description': 'A beautiful waterfall located near Pendjari National Park', 'latitude': 10.7480, 'longitude': 1.4472},
    {'id': 3, 'name': 'Boukoumbé', 'description': 'A town known for its traditional Tata Somba houses', 'latitude': 10.2552, 'longitude': 1.1128}
]



artistic_circuit = [
    {'id': 1, 'name': 'Cotonou Dantokpa Market', 'description': 'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts and textiles', 'latitude': 6.3671, 'longitude': 2.4335},
    {'id': 2, 'name': 'Ouidah Museum of History', 'description': 'A museum that provides insights into the history of the slave trade in Benin', 'latitude': 6.3633, 'longitude': 2.0851},
    {'id': 3, 'name': 'Royal Palaces of Abomey', 'description': 'Historical palaces that were once the seat of the Kingdom of Dahomey', 'latitude': 7.1829, 'longitude': 1.9912},
    {'id': 4, 'name': 'Porto-Novo', 'description': 'The capital city of Benin, known for its colonial architecture and vibrant culture', 'latitude': 6.4969, 'longitude': 2.6289}
]



adventure_circuit = [
    {'id': 1, 'name': 'Pendjari National Park', 'description': 'A UNESCO World Heritage site known for its wildlife, including elephants, lions, and hippos', 'latitude': 11.0416, 'longitude': 1.4141},
    {'id': 2, 'name': 'Tanougou Falls', 'description': 'A beautiful waterfall located near Pendjari National Park', 'latitude': 10.7480, 'longitude': 1.4472},
    {'id': 3, 'name': 'Boukoumbé', 'description': 'A town known for its traditional Tata Somba houses', 'latitude': 10.2552, 'longitude': 1.1128},
    {'id': 4, 'name': 'Ganvie Lake Village', 'description': 'A village built on stilts in Lake Nokoué, often referred to as the "Venice of Africa"', 'latitude': 6.4969, 'longitude': 2.4183}
]



import folium
import pandas as pd

# Coordinates for different circuits
historical_circuit = [
    {'id': 1, 'name': 'Cotonou Dantokpa Market', 'description': 'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts and textiles', 'latitude': 6.3671, 'longitude': 2.4335},
    {'id': 2, 'name': 'Ouidah Museum of History', 'description': 'A museum that provides insights into the history of the slave trade in Benin', 'latitude': 6.3633, 'longitude': 2.0851},
    {'id': 3, 'name': 'Royal Palaces of Abomey', 'description': 'Historical palaces that were once the seat of the Kingdom of Dahomey', 'latitude': 7.1829, 'longitude': 1.9912},
    {'id': 4, 'name': 'Porto-Novo', 'description': 'The capital city of Benin, known for its colonial architecture and vibrant culture', 'latitude': 6.4969, 'longitude': 2.6289}
]

beach_circuit = [
    {'id': 1, 'name': 'Fidjrosse Beach', 'description': 'A beautiful sandy beach perfect for relaxation, swimming, and enjoying local seafood', 'latitude': 6.3650, 'longitude': 2.3758},
    {'id': 2, 'name': 'Cotonou Dantokpa Market', 'description': 'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts and textiles', 'latitude': 6.3671, 'longitude': 2.4335},
    {'id': 3, 'name': 'Ganvie Lake Village', 'description': 'A village built on stilts in Lake Nokoué, often referred to as the "Venice of Africa"', 'latitude': 6.4969, 'longitude': 2.4183},
    {'id': 4, 'name': 'Nokoué Lake', 'description': 'A large lake known for its biodiversity and the stilt village of Ganvie', 'latitude': 6.4833, 'longitude': 2.4167}
]

nature_circuit = [
    {'id': 1, 'name': 'Pendjari National Park', 'description': 'A UNESCO World Heritage site known for its wildlife, including elephants, lions, and hippos', 'latitude': 11.0416, 'longitude': 1.4141},
    {'id': 2, 'name': 'Tanougou Falls', 'description': 'A beautiful waterfall located near Pendjari National Park', 'latitude': 10.7480, 'longitude': 1.4472},
    {'id': 3, 'name': 'Boukoumbé', 'description': 'A town known for its traditional Tata Somba houses', 'latitude': 10.2552, 'longitude': 1.1128}
]

artistic_circuit = [
    {'id': 1, 'name': 'Cotonou Dantokpa Market', 'description': 'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts and textiles', 'latitude': 6.3671, 'longitude': 2.4335},
    {'id': 2, 'name': 'Ouidah Museum of History', 'description': 'A museum that provides insights into the history of the slave trade in Benin', 'latitude': 6.3633, 'longitude': 2.0851},
    {'id': 3, 'name': 'Royal Palaces of Abomey', 'description': 'Historical palaces that were once the seat of the Kingdom of Dahomey', 'latitude': 7.1829, 'longitude': 1.9912},
    {'id': 4, 'name': 'Porto-Novo', 'description': 'The capital city of Benin, known for its colonial architecture and vibrant culture', 'latitude': 6.4969, 'longitude': 2.6289}
]

adventure_circuit = [
    {'id': 1, 'name': 'Pendjari National Park', 'description': 'A UNESCO World Heritage site known for its wildlife, including elephants, lions, and hippos', 'latitude': 11.0416, 'longitude': 1.4141},
    {'id': 2, 'name': 'Tanougou Falls', 'description': 'A beautiful waterfall located near Pendjari National Park', 'latitude': 10.7480, 'longitude': 1.4472},
    {'id': 3, 'name': 'Boukoumbé', 'description': 'A town known for its traditional Tata Somba houses', 'latitude': 10.2552, 'longitude': 1.1128},
    {'id': 4, 'name': 'Ganvie Lake Village', 'description': 'A village built on stilts in Lake Nokoué, often referred to as the "Venice of Africa"', 'latitude': 6.4969, 'longitude': 2.4183}
]

# Create a folium map centered around a central point in Benin
map_benin = folium.Map(location=[9.3077, 2.3158], zoom_start=7)

# Function to add a circuit to the map with a specified color and create a feature group for each circuit
def add_circuit_to_map(circuit_list, color, name):
    feature_group = folium.FeatureGroup(name=name)
    locations = []
    for place in circuit_list:
        folium.Marker(
            location=[place['latitude'], place['longitude']],
            popup=place['name'],
            icon=folium.Icon(color=color)
        ).add_to(feature_group)
        locations.append((place['latitude'], place['longitude']))
    folium.PolyLine(locations, color=color, weight=2.5, opacity=1).add_to(feature_group)
    feature_group.add_to(map_benin)

# Add circuits to the map with different colors
add_circuit_to_map(historical_circuit, 'red', 'Historical and Cultural Heritage')
add_circuit_to_map(beach_circuit, 'blue', 'Coastal and Beach Relaxation')
add_circuit_to_map(nature_circuit, 'green', 'Natural Wonders and Safari')
add_circuit_to_map(artistic_circuit, 'purple', 'Artistic and Educational Trip')
add_circuit_to_map(adventure_circuit, 'orange', 'Adventure and Exploration')

# Add layer control to the map
folium.LayerControl().add_to(map_benin)

# Save the map to an HTML file
map_benin.save('benin_tourist_circuits.html')

# Save the coordinates as a dataframe file
data = []
for circuit, places in zip(['Historical and Cultural Heritage', 'Coastal and Beach Relaxation', 'Natural Wonders and Safari', 'Artistic and Educational Trip', 'Adventure and Exploration'],
                           [historical_circuit, beach_circuit, nature_circuit, artistic_circuit, adventure_circuit]):
    for place in places:
        data.append({'circuit': circuit, 'id': place['id'], 'name': place['name'], 'description': place['description'], 'latitude': place['latitude'], 'longitude': place['longitude']})

df = pd.DataFrame(data)
df.to_csv('benin_tourist_circuits.csv', index=False)
