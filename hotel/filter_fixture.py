import json

input_file = 'hotel/fixtures/datos.json'
output_file = 'hotel/fixtures/datos_filtered.json'

with open(input_file, 'r') as f:
    data = json.load(f)

filtered_data = [
    item for item in data 
    if item['model'] not in ['auth.permission', 'contenttypes.contenttype']
]

with open(output_file, 'w') as f:
    json.dump(filtered_data, f, indent=4)

print(f"Filtered data saved to {output_file}")
