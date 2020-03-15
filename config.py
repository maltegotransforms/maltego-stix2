# Config of JSON-REF STIX 2 Schemas to process
# Each element should follow the format :
# {
# 	 "path": string, # path to a folder containing a JSON REF schema
# 	 "category": string   # Maltego Entity Category to group entities generated from this schema
# }
#
schema_config = [
    {
        "path": "./cti-stix2-json-schemas/schemas/sdos/",
        "category": "STIX 2 domain objects",
    },
    {
        "path": "./cti-stix2-json-schemas/schemas/sros/",
        "category": "STIX 2 relationship objects",
    },
    {
        "path": "./cti-stix2-json-schemas/schemas/observables/",
        "category": "STIX 2 observables",
    },
    {
        "path": "./cti-stix2-json-schemas-extended/schemas/sdos/",
        "category": "STIX 2 domain objects",
    },
]

# Config to handle Maltego entities inheritance
# Format :
# "stix_type": "parent_maltego_entity_id"
heritage_config = {
    "autonomous-system": "maltego.AS",
    "domain-name": "maltego.Domain",
    "directory": "maltego.custom.entities.indicators.systemindicator",
    "file": "maltego.custom.entities.AnyFile",
    "email-addr": "maltego.EmailAddress",
    "email-message": "maltego.Document",
    "identity": "maltego.Organization",
    "incident": "maltego.Incident",
    "indicator": "maltego.String",
    "infrastructure": "maltego.custom.entities.indicators.networkindicator",
    "intrusion-set": "cyrildemonceaux.Attacker",
    "ipv4-addr": "maltego.IPv4Address",
    "ipv6-addr": "maltego.custom.entities.infrastructure.IPv6Address",
    "location": "maltego.Location",
    "mac-addr": "maltego.custom.entities.indicators.networkindicator",
    "malware": "maltego.custom.entities.malwares.MalwareFamily",
    "mutex": "maltego.custom.entities.configuration.Mutex",
    "process": "maltego.custom.entities.indicators.systemindicator",
    "threat-actor": "cyrildemonceaux.Attacker",
    "url": "maltego.URL",
    "user-account": "maltego.custom.entities.indicators.systemindicator",
    "vulnerability": "maltego.Exploit",
    "windows-registry-key": "maltego.custom.entities.indicators.systemindicator",
    "x509-certificate": "maltego.custom.entities.certificates.Certificatex509",
}

# Config of PNG files to process to create Maltego icons
# Each element should follow the format :
# {
# 	"path": string, # path to a folder containing PNG files. A recursive search is done inside this folder.
# 	"filter": string   # part of the PNG files names to proces
# 	"replace": {"string_to_replace": "replacement"} # Search and replace in PNG file names
# }
# The icon name should shart with the type of the entity (eg "malware")
# If several icons are available for each entity, the filter parameter can be used to filter
# on the ones to keep. The icons names shoud contain this string just after the entity type.
icons_config = [
    {
        "path": "./stix2-graphics/icons/png/",
        "filter": "-round-flat-300",
        "replace": {"coa": "course_of_action", "http": "url"},
    }
]
