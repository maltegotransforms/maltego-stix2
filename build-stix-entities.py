import os
import json

schema_paths = [
	"./cti-stix2-json-schemas/schemas/sdos/",
	"./cti-stix2-json-schemas/schemas/sros/"
]

def resolve_refs(schema, path):
	if isinstance(schema, dict):
		if "$ref" in schema and not schema["$ref"].startswith("#"):
			with open(os.path.join(path, schema["$ref"]), "r") as ref_file:
				ref_schema = json.load(ref_file)
				for key, value in schema.items():
					if key != "$ref":
						ref_schema[key] = value
				return resolve_refs(ref_schema, os.path.dirname(os.path.join(path, schema["$ref"])))
		else:
			new_dict = {}
			for key, value in schema.items():
				new_dict[key] = resolve_refs(value, path)
			return new_dict
	elif isinstance(schema, list):
		new_list = []
		for l in schema:
			new_list.append(resolve_refs(l, path))
		return new_list
	else:
		return schema

# Read schemas
for schema_path in schema_paths:
	for entity_file_name in os.listdir(schema_path):
		with open(os.path.join(schema_path, entity_file_name), "r") as entity_file:
			entity_schema = json.load(entity_file)
			entity_schema = resolve_refs(entity_schema, schema_path)

			fields = {}
			# Only the last occurrence of each proprety is kept to handle inheritance
			for properties in entity_schema["allOf"]:
				if "properties" in properties:
					for key, value in properties["properties"].items():
						property_type = "string"
						if "type" in value:
							if value["type"] == "array":
								property_type = "string[]"
						if "enum" in value and len(value["enum"]) == 1:
							data = {
								"name": key,
								"type": property_type,
								"description": value["description"] if "description" in value else "",
								"value": value["enum"][0]
							}
							fields[key] = '         <Field name="{name}" type="{type}" nullable="true" hidden="false" readonly="true" description="{description}">\n            <DefaultValue>{value}</DefaultValue>\n            <SampleValue>{value}</SampleValue>\n         </Field>\n'.format(**data)
						else:
							data = {
								"name": key,
								"type": property_type,
								"description": value["description"] if "description" in value else ""
							}
							fields[key] = '         <Field name="{name}" type="{type}" nullable="true" hidden="false" readonly="false" description="{description}"/>\n'.format(**data)

			# Export entity
			with open("./templates/template.entity", "r") as entity_template:
				data = {
					"id": "STIX2." + entity_schema["title"],
					"displayName": entity_schema["title"].replace('-', ' ').title(),
					"namePlural": entity_schema["title"].replace('-', ' ').title(),
					"description": entity_schema["description"].strip(),
					"category": "STIX 2",
					"smallIconResource": "stix2_" + entity_schema["title"].replace('-', '_'),
					"largeIconResource": "stix2_" + entity_schema["title"].replace('-', '_'),
					"mainValue": "name" if "required" in entity_schema and "name" in entity_schema["required"] else "id",
					"fields": "".join(v for k,v in fields.items())
				}
				t = entity_template.read()
				with open("./mtz/Entities/"+data["id"]+".entity", "w") as output:
					output.write(t.format(**data))

				print(entity_schema["title"].replace('-', ' ').title().replace(' ', '') + ' = "' + data["id"] + '"')