#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from maltego_stix2.util import maltego_to_stix2, stix2_to_maltego
from maltego_trx.maltego import *
from maltego_trx.entities import *
from maltego_stix2.entities import *
from maltego_stix2.config import _partial_reverse_type_map
import json


def stix2_transform(transformName, entityType, client_msg: MaltegoMsg, response):
    # Extract input entity parameters

    entity_type = entityType
    if not client_msg.Genealogy:
        client_msg.Genealogy = [{"Name": entity_type}]

    for e_type in client_msg.Genealogy:
        for name in list(client_msg.Properties):
            v3_property_name = translate_legacy_property_name(e_type["Name"], name)
            if v3_property_name is not None:
                client_msg.Properties[v3_property_name] = client_msg.Properties[name]

    client_msg.clearLegacyProperties()

    if "convert-to-stix" in transformName:
        if entity_type in _partial_reverse_type_map:
            permissive_stix2_object = maltego_to_stix2(
                client_msg,
                transform=response,
                allow_custom_types=True,
                allow_custom_fields=True,
                allow_skipping_stix2_coercion=False
            )
            if permissive_stix2_object is not None:
                entity = stix2_to_maltego(permissive_stix2_object)
                response.entities.append(entity)

    elif "explode" in transformName:
        permissive_stix2_object = maltego_to_stix2(
            client_msg,
            transform=response,
            allow_custom_types=True,
            allow_custom_fields=True,
            allow_skipping_stix2_coercion=False
        )
        property_name = transformName.split("-")[1]
        entity_type = Phrase
        maltego_property = None
        if property_name == "aliases":
            entity_type = Alias
        elif property_name == "created_by_ref":
            entity_type = Identity
            maltego_property = "id"
        elif property_name == "hashes":
            entity_type = "maltego.Hash"
        elif property_name == "labels":
            entity_type = "maltego.Phrase"
        else:
            entity_type = "maltego.Phrase"

        property_value = None
        if permissive_stix2_object and property_name in permissive_stix2_object:
            property_value = permissive_stix2_object[property_name]

        if property_value and len(property_value) > 0:
            if isinstance(property_value, list):
                property_lst = property_value
            elif isinstance(property_value, dict):
                property_lst = [v for k, v in property_value.items()]
            else:
                property_lst = [property_value]

            for value in property_lst:
                if len(value) > 0:
                    entity = MaltegoEntity(
                        type=entity_type, value=value
                    )
                    if maltego_property:
                        entity.addProperty(
                            fieldName=maltego_property, value=value
                        )
                    response.entities.append(entity)
