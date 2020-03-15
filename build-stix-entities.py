import os
import json
from config import schema_config, heritage_config


def resolve_refs(schema, path):
    if isinstance(schema, dict):
        if "$ref" in schema and not schema["$ref"].startswith("#"):
            with open(os.path.join(path, schema["$ref"]), "r") as ref_file:
                ref_schema = json.load(ref_file)
                for key, value in schema.items():
                    if key != "$ref":
                        ref_schema[key] = value
                return resolve_refs(
                    ref_schema, os.path.dirname(os.path.join(path, schema["$ref"]))
                )
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


categories = []

# Read schemas
for schema in schema_config:
    for entity_file_name in os.listdir(schema["path"]):
        with open(os.path.join(schema["path"], entity_file_name), "r") as entity_file:
            entity_schema = json.load(entity_file)
            entity_schema = resolve_refs(entity_schema, schema["path"])

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
                                "description": value["description"]
                                if "description" in value
                                else "",
                                "value": value["enum"][0],
                            }
                            fields[
                                key
                            ] = '         <Field name="{name}" type="{type}" nullable="true" hidden="false" readonly="true" description="{description}">\n            <DefaultValue>{value}</DefaultValue>\n            <SampleValue>{value}</SampleValue>\n         </Field>\n'.format(
                                **data
                            )
                        else:
                            data = {
                                "name": key,
                                "type": property_type,
                                "description": value["description"]
                                if "description" in value
                                else "",
                            }
                            fields[
                                key
                            ] = '         <Field name="{name}" type="{type}" nullable="true" hidden="false" readonly="false" description="{description}"/>\n'.format(
                                **data
                            )

            # Export entity
            with open("./templates/template.entity", "r") as entity_template:
                base_entity = ""
                if (
                    entity_schema["title"] in heritage_config
                    and heritage_config[entity_schema["title"]] != ""
                ):
                    base_entity = (
                        "      <BaseEntity>"
                        + heritage_config[entity_schema["title"]]
                        + "</BaseEntity>"
                    )
                data = {
                    "id": "STIX2." + entity_schema["title"],
                    "displayName": entity_schema["title"].replace("-", " ").title(),
                    "namePlural": entity_schema["title"].replace("-", " ").title(),
                    "description": entity_schema["description"].strip(),
                    "category": schema["category"],
                    "smallIconResource": "stix2_"
                    + entity_schema["title"].replace("-", "_"),
                    "largeIconResource": "stix2_"
                    + entity_schema["title"].replace("-", "_"),
                    "mainValue": (
                        "name"
                        if "name" in fields
                        else (
                            "value"
                            if "value" in fields
                            else (
                                "relationship_type"
                                if "relationship_type" in fields
                                else "id"
                            )
                        )
                    ),
                    "fields": "".join(v for k, v in fields.items()),
                    "baseEntities": base_entity,
                }
                t = entity_template.read()
                with open("./mtz/Entities/" + data["id"] + ".entity", "w") as output:
                    output.write(t.format(**data))

                print(
                    entity_schema["title"].replace("-", " ").title().replace(" ", "")
                    + ' = "'
                    + data["id"]
                    + '"'
                )

            # Export category if new
            if schema["category"] not in categories:
                with open("./templates/template.category", "r") as entity_template:
                    data = {"name": schema["category"]}
                    t = entity_template.read()
                    with open(
                        "./mtz/EntityCategories/"
                        + schema["category"].lower().replace(" ", "-")
                        + ".category",
                        "w",
                    ) as output:
                        output.write(t.format(**data))

                    categories.append(schema["category"])
