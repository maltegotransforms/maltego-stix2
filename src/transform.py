#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## TODO
# Support adding for all STIX2 entities
# Orient relationship transforms with new 3.0.2 parameter
# Handle errors and messages

import argparse
from maltego_trx.maltego import *
from maltego_trx.entities import *
from entities import *
from config import local_execution_path, python_path
from utils import sanitize


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Maltego-STIX2 transforms")
    parser.add_argument(
        "--transform", dest="transformName", type=str, help="The transform to run"
    )

    args, unknown = parser.parse_known_args()

    # print(unknown)

    if len(unknown) > 0:
        # Create Maltego transgorm object
        transform = MaltegoTransform()

        # Parse Maltego input parameters
        client_msg = MaltegoMsg(LocalArgs=unknown)

        # Extract input entity parameters
        input_value = client_msg.Value
        input_id = (
            client_msg.getProperty("id") if client_msg.getProperty("id") else None
        )
        input_type = (
            client_msg.getProperty("type") if client_msg.getProperty("type") else None
        )
        input_name = (
            client_msg.getProperty("name") if client_msg.getProperty("name") else None
        )

        if "convert" in args.transformName:
            property_name = args.transformName.split("-")[1]
            if property_name == "hash":
                entity = transform.addEntity(File, sanitize(input_value, True))
                entity.addProperty(
                    fieldName="hashes", value=[sanitize(input_value, True)]
                )
        elif "explode" in args.transformName:
            property_name = args.transformName.split("-")[1]
            entity_type = Phrase
            maltego_property = None
            if property_name == "aliases":
                entity_type = Alias
            if property_name == "created_by_ref":
                entity_type = Identity
                maltego_property = "id"
            if property_name == "hashes":
                entity_type = "maltego.Hash"
            property_str = (
                client_msg.getProperty(property_name)
                if client_msg.getProperty(property_name)
                else None
            )
            if property_str and len(property_str) > 0:
                # STR to LST allowing several formats
                property_str = property_str.replace(
                    '", "', "','"
                )  # quote {"} separator {, }
                property_str = property_str.replace(
                    '","', "','"
                )  # quote {"} separator {,}
                property_str = property_str.replace(
                    "', '", "','"
                )  # quote {'} separator {, }
                # Clean begining of the list
                if property_str.startswith("["):
                    property_str = property_str[1:]
                if property_str.startswith("'"):
                    property_str = property_str[1:]
                if property_str.startswith('"'):
                    property_str = property_str[1:]
                # Clean end of the list
                if property_str.endswith("]"):
                    property_str = property_str[:-1]
                if property_str.endswith("'"):
                    property_str = property_str[:-1]
                if property_str.endswith('"'):
                    property_str = property_str[:-1]
                property_lst = property_str.split("','")

                for value in property_lst:
                    if len(value) > 0:
                        entity = transform.addEntity(entity_type, sanitize(value, True))
                        if maltego_property:
                            entity.addProperty(
                                fieldName=maltego_property, value=sanitize(value, True)
                            )

        # Output Maltego XML result
        print(transform.returnOutput())
