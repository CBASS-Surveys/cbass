import json

json_data = open("testdata.json").read()

data = json.loads(json_data)
survey_name = data["survey_name"]
survey_properties = data["survey_properties"]
print survey_properties.keys()
print survey_properties.items()

