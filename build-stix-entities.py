#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, json
from collections import defaultdict

from maltego_stix2.config import _schema_config, _heritage_config, _MaltegoEntityMapping, digits


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


def generateFields(schemaAllOf, entity_mapping: _MaltegoEntityMapping):
    fields = {}
    original_field_names = set()
    for properties in schemaAllOf:
        if "properties" in properties:

            def shadows_buit_in_name(kv):
                return (
                    entity_mapping is not None and kv[0] in entity_mapping.property_map
                )

            # move the properties that are maltego-native to the top so they can be spotted more quickly
            # the STIX core properties will still be first in the final output
            prop_items_in_order = sorted(
                properties["properties"].items(), key=shadows_buit_in_name, reverse=True
            )
            for key, value in prop_items_in_order:
                original_field_names.add(key)

                if entity_mapping is not None:
                    key = entity_mapping.translate_prop_name(key)

                property_type = "string"
                if "type" in value:
                    if value["type"] == "array":
                        property_type = "string[]"

                desc = value["description"] if "description" in value else ""
                if "enum" in value and len(value["enum"]) == 1:
                    default_value = value["enum"][0]
                    fields[key] = (
                        f'         <Field name="{key}" type="{property_type}" nullable="true" hidden="false" '
                        f'readonly="true" description="{desc}">\n'
                        f"            <DefaultValue>{default_value}</DefaultValue>\n"
                        f"            <SampleValue>{default_value}</SampleValue>\n"
                        f"         </Field>\n"
                    )
                else:
                    fields[key] = (
                        f'         <Field name="{key}" type="{property_type}" nullable="true" hidden="false" '
                        f'readonly="false" description="{desc}"/>\n'
                    )
        elif "allOf" in properties:
            new_fields, o_fields = generateFields(properties["allOf"], entity_mapping)
            fields.update(new_fields)
            original_field_names.update(o_fields)

    # store the applied entity mapping as a hidden property on the entity so proper STIX entities can be recovered
    # more easily without needing to use this library
    name = "x_maltego_recovery_property_mapping"
    description = "The mapping of Maltego internal property names to STIX property names used for this entity."
    if entity_mapping is not None:
        mapping_d = defaultdict(list)
        for k, v in entity_mapping.property_map.items():
            mapping_d[v].append(k)
        mapping = json.dumps(mapping_d)
    else:
        mapping = "{}"
    fields[
        name
    ] = (  # TODO consider making this a hidden property? OTOH this way the change is more noticable to users
        f'         <Field name="{name}" displayName="{name}" type="string" nullable="true" hidden="false" '
        f'readonly="true" description="{description}">\n'
        f"            <DefaultValue>{mapping}</DefaultValue>\n"
        f"            <SampleValue>{mapping}</SampleValue>\n"
        f"         </Field>\n"
    )

    return fields, original_field_names


def build(with_opencti=False):
    categories = []
    entities_ref = {}

    # Read schemas
    for schema in _schema_config:
        if schema["tag"] == "default" or with_opencti:
            for entity_file_name in os.listdir(schema["path"]):
                with open(
                    os.path.join(schema["path"], entity_file_name), "r"
                ) as entity_file:
                    entity_schema = json.load(entity_file)

                    # TODO Rely on external library to parse JSON-ref files
                    entity_schema = resolve_refs(entity_schema, schema["path"])

                    entity_mapping: _MaltegoEntityMapping = _heritage_config.get(
                        entity_schema["title"]
                    )
                    if entity_mapping is None or entity_mapping.entity_type is None:
                        print(f"STIX entity '{entity_schema['title']}' is unmapped!")
                    fields, original_field_names = generateFields(
                        entity_schema["allOf"], entity_mapping=entity_mapping
                    )
                    if "oneOf" in entity_schema:
                        new_fields, o_fields = generateFields(
                            entity_schema["oneOf"], entity_mapping
                        )
                        fields.update(new_fields)
                        original_field_names.update(o_fields)

                    if "name" in original_field_names:
                        display_value = "name"
                    elif "value" in original_field_names:
                        display_value = "value"
                    elif "relationship_type" in original_field_names:
                        display_value = "id"
                    elif "opinion" in original_field_names:
                        display_value = "opinion"
                    else:
                        display_value = "id"

                    icon_name = f'stix_two_{entity_schema["title"].replace("-", "_")}'
                    for key, val in digits.items():
                        icon_name = icon_name.replace(key, val)

                    if entity_mapping is not None:
                        display_value = entity_mapping.translate_prop_name(display_value)
                        if entity_mapping.display_value_override:
                            display_value = entity_mapping.display_value_override
                        icon_name = entity_mapping.icon_override or icon_name
                    if "relationship_type" in original_field_names:
                        display_value = "relationship_type"

                    main_value = "id"

                    # Export entity
                    with open("./templates/template.entity", "r") as entity_template:
                        base_entity = ""

                        # Inherit the more specific type first so it shows up in the Maltego client's Entity Manager
                        if (
                            entity_mapping is not None
                            and entity_mapping.entity_type is not None
                        ):
                            base_entity += f"      <BaseEntity>{entity_mapping.entity_type}</BaseEntity>\n"

                        base_entity += (
                            "      <BaseEntity>maltego.STIX2.core</BaseEntity>"
                        )

                        data = {
                            "id": "maltego.STIX2." + entity_schema["title"],
                            "regex": "<![CDATA[^("
                            + entity_schema["title"]
                            + "--[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12})$]]>",
                            "displayName": "STIX2 "
                            + entity_schema["title"].replace("-", " ").title(),
                            "namePlural": entity_schema["title"]
                            .replace("-", " ")
                            .title(),
                            "description": entity_schema["description"].strip(),
                            "category": schema["category"],
                            "smallIconResource": icon_name,
                            "largeIconResource": icon_name,
                            "mainValue": main_value,
                            "displayValue": display_value,
                            "fields": "".join(v for k, v in fields.items()),
                            "baseEntities": base_entity,
                        }
                        t = entity_template.read()
                        with open(
                            "./mtz/Entities/" + data["id"] + ".entity", "w"
                        ) as output:
                            output.write(t.format(**data))

                        entities_ref[data["id"]] = (
                            entity_schema["title"]
                            .replace("-", " ")
                            .title()
                            .replace(" ", "")
                            + ' = "'
                            + data["id"]
                            + '"\n'
                        )

                    # Export category if new
                    if schema["category"] not in categories:
                        with open(
                            "./templates/template.category", "r"
                        ) as entity_template:
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

    # Export entities definition in Python format to extend Maltego TRX
    with open("./maltego_stix2/entities.py", "w") as output:
        output.write("".join(v for k, v in sorted(entities_ref.items())))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        build(with_opencti=True)
    else:
        build()
