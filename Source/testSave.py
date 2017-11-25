import json

json_data = open("testdata.json").read()

data = json.loads(json_data)
survey_name = data["survey_name"]
survey_properties = data["survey_properties"]
questions = data["as;dlkfj"]
print data
