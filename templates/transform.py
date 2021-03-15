#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from maltego_trx.maltego import MaltegoMsg
from maltego_trx.transform import DiscoverableTransform
from stix2transform import stix2_transform


class {functionName}(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response):
        stix2_transform("{transformName}", "{entityType}", request, response)
