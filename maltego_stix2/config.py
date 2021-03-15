# Config of JSON-REF STIX 2 Schemas to process
# Each element should follow the format :
# {
#    "path": string, # path to a folder containing a JSON REF schema
#    "category": string   # Maltego Entity Category to group entities generated from this schema
# }
#
from collections import defaultdict

_schema_config = [
    {
        "path": "./cti-stix2-json-schemas/schemas/sdos/",
        "category": "STIX 2 domain objects",
        "tag": "default",
    },
    {
        "path": "./cti-stix2-json-schemas/schemas/sros/",
        "category": "STIX 2 relationship objects",
        "tag": "default",
    },
    {
        "path": "./cti-stix2-json-schemas/schemas/observables/",
        "category": "STIX 2 observables",
        "tag": "default",
    },
    {
        "path": "./cti-stix2-json-schemas-extended/schemas/sdos/",
        "category": "STIX 2 domain objects",
        "tag": "opencti",
    },  # These schemas allow for custom extensions of the STIX2 format. The provided ones are used in OpenCTI
    {
        "path": "./cti-stix2-json-schemas-extended/schemas/observables/",
        "category": "STIX 2 observables",
        "tag": "opencti",
    },  # These schemas allow for custom extensions of the STIX2 format. The provided ones are used in OpenCTI
]

digits = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight",
    "9": "nine"
}

# Config of PNG files to process to create Maltego icons
# Each element should follow the format :
# {
#   "path": string, # path to a folder containing PNG files. A recursive search is done inside this folder.
#   "filter": string   # part of the PNG files names to process
#   "replace": {"string_to_replace": "replacement"} # Search and replace in PNG file names
# }
# The icon name should start with the type of the entity (eg "malware")
# If several icons are available for each entity, the filter parameter can be used to filter
# on the ones to keep. The icons names shoud contain this string just after the entity type.
_icons_config = [
    {
        "path": "./stix2-graphics/icons/png/",
        "filter": "-round-flat-300",
        "replace": {
            "coa": "course_of_action",
            "http": "url",
            "incident": "x_opencti_incident",
            **digits
        },
    },
    {
        "path": "./stix2-graphics-extended/icons/png/",
        "filter": "-round-flat-300",
        "replace": digits,
    },
]


class _MaltegoEntityMapping(object):
    def __init__(
        self,
        entity_type,
        property_map=None,
        display_value_override=None,
        icon_override=None,
        default_values=None,

        # this is for setting required maltego props that otherwise don't have a default (like URL's short-title)
        maltego_from_stix_extra_property_map=None,
        use_mapping_for_reverse_conversion=True,
    ):
        self.entity_type = entity_type
        self.property_map = property_map or {}
        self.icon_override = icon_override
        self.display_value_override = display_value_override
        self.default_values = default_values
        self.maltego_from_stix_property_map_extra = maltego_from_stix_extra_property_map
        self.use_mapping_for_reverse_conversion = use_mapping_for_reverse_conversion

    def translate_prop_name(self, stix_prop_name):
        return self.property_map.get(stix_prop_name, stix_prop_name)


_heritage_config = {
    # We add property mappings even for properties that happen to have the same name in order to take note of the fact
    # that these properties do in fact "make sense" within STIX2. This is important when we convert STIX2 Maltego
    # Entities back to STIX2 objects.
    "artifact": _MaltegoEntityMapping(None, None, None, icon_override="stix_two_default_icon"),  # was: Assemble
    "autonomous-system": _MaltegoEntityMapping(
        "maltego.AS",
        {"number": "as.number"},
        display_value_override="as.number",
    ),
    "domain-name": _MaltegoEntityMapping("maltego.Domain", {"value": "fqdn"}),
    "directory": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon"),
    "file": _MaltegoEntityMapping(
        "maltego.File", {"path": "source", "name": "description"}, icon_override="stix_two_default_icon"  # was: Binary
    ),
    "email-addr": _MaltegoEntityMapping("maltego.EmailAddress", {"value": "email"}),
    "email-message": _MaltegoEntityMapping(
        "maltego.ConversationEmail",
        {"from_ref": "email", "to_refs": "email.recipients", "subject": "title"},
        icon_override="stix_two_email_msg",
        default_values={"is_multipart": False}
    ),
    "identity": _MaltegoEntityMapping("maltego.Organization", {"name": "title"}),
    "ipv4-addr": _MaltegoEntityMapping(
        "maltego.IPv4Address", {"value": "ipv4-address"}
    ),
    "location": _MaltegoEntityMapping(
        "maltego.Location",
        {
            "name": "location.name",
            "latitude": "latitude",
            "longitude": "longitude",
            "country": "country",
            "city": "city",
            "street_address": "streetaddress",
            "administrative_area": "location.area",
            "postal_code": "location.areacode",
        },
    ),
    "mac-addr": _MaltegoEntityMapping(
        "maltego.MacAddress", {"value": "macaddress"}
    ),  # added
    "threat-actor": _MaltegoEntityMapping(
        "maltego.Organization", {"name": "title"},
        use_mapping_for_reverse_conversion=False  # "every threat actor is an org but not vice versa"
    ),
    "url": _MaltegoEntityMapping(
        "maltego.URL", {"value": "url"}, maltego_from_stix_extra_property_map={"short-title": "value"}
    ),
    "user-account": _MaltegoEntityMapping(
        "maltego.Alias", {"user_id": "alias"}, display_value_override="alias"
    ),
    "x509-certificate": _MaltegoEntityMapping(
        "maltego.X509Certificate",
        {
            "subject": "subject",
            "serial_number": "serial",
            "issuer": "issuer",
            "validity_not_before": "validFrom",
            "validity_not_after": "validTo",
        },
        icon_override="stix_two_default_icon",
    ),
    #"note": None,
    "ipv6-addr": _MaltegoEntityMapping(
        "maltego.IPv6Address", {"value": "ipv6-address"}
    ),
    "x-opencti-hostname": _MaltegoEntityMapping("maltego.DNSName", {"value": "fqdn"}, icon_override="stix_two_default_icon"),
    "x-opencti-incident": _MaltegoEntityMapping("maltego.Incident", {"name": "title"}),
    "campaign": _MaltegoEntityMapping(
        "maltego.Event",
        {
            "name": "title",
            "first_seen": "starttime",
            "last_seen": "stoptime"
        }
    ),
    # "course-of-action": None,
    # "grouping": None,
    # "report": None,
    "vulnerability": _MaltegoEntityMapping(
        # Not 100% clean inheritance, since some Vulnerabilities are not CVE's.
        # However, maltego.CVE inherits maltego.Phrase, so for search Transforms this ends up working out fine
        # most of the time. Since we cannot retroactively make CVE inherit from Vulnerability, this is the next best
        # option for the time being.
        "maltego.CVE",
        property_map={"name": "text"}
        # icon_override="stix_two_default_icon"
    ),
    # "malware": None,
    # "observed-data": None,
    # "tool": None,
    # "attack-pattern": None,
    # "malware-analysis": None,
    # "opinion": None,
    # "indicator": None,
    # "intrusion-set": None,
    # "infrastructure": None,
    # "relationship": None,
    # "sighting": None,
    # "network-traffic": None,
    "windows-registry-key": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon"),
    "process": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon"),
    "software": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon"),
    "mutex": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon"),
    "x-opencti-text": _MaltegoEntityMapping(
        "maltego.Phrase",
        {"value": "text"},
        display_value_override="text",
        icon_override="stix_two_default_icon"
    ),
    "x-opencti-cryptographic-key": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon"),
    "x-opencti-cryptocurrency-wallet": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon"),
    "x-opencti-user-agent": _MaltegoEntityMapping(None, icon_override="stix_two_default_icon")
}

# can be used to initialize "best-guess" STIX2 from arbitrary Maltego entities
# TODO maybe it makes more sense to hard-code an extended version of this so we can cover more Maltego entities
_partial_reverse_type_map = {
    v.entity_type: k for k, v in _heritage_config.items()
    if v.entity_type is not None and v.use_mapping_for_reverse_conversion
}

# can be used to convert STIX2 Maltego entities back into proper STIX2 entities
_reverse_property_maps = defaultdict(dict)
for class_name, mapping in _heritage_config.items():
    if mapping.entity_type is not None:
        for _k, _v in mapping.property_map.items():
            if _v in _reverse_property_maps[class_name]:
                raise ValueError(
                    f"Invalid property mapping for {class_name} ({_v} is already mapped)."
                    " Mapping a stix property to multiple Maltego properties break conversion and is not allowed."
                    " If you need to always populate a required field, please use the 'default_values' parameter."
                )
            _reverse_property_maps[class_name][_v] = _k


