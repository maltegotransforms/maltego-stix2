# Config of JSON-REF STIX 2 Schemas to process
# Each element should follow the format :
# {
#     "path": string, # path to a folder containing a JSON REF schema
#     "category": string   # Maltego Entity Category to group entities generated from this schema
# }
# 
schema_config = [
	{
		"path": "./cti-stix2-json-schemas/schemas/sdos/",
		"category": "STIX 2 domain objects"
	},
	{
		"path": "./cti-stix2-json-schemas/schemas/sros/",
		"category": "STIX 2 relationship objects"
	},
	#{
	#	"path": "./cti-stix2-json-schemas/schemas/observables/",
	#	"category": "STIX 2 observables"
	#},
	{
		"path": "./cti-stix2-json-schemas-extended/schemas/sdos/",
		"category": "STIX 2 domain objects"	
	}
]

# Config of PNG files to process to create Maltego icons
# Each element should follow the format :
# {
#     "path": string, # path to a folder containing PNG files. A recursive search is done inside this folder.
#     "filter": string   # part of the PNG files names to proces
# }
# The icon name should shart with the type of the entity (eg "malware") 
# If several icons are available for each entity, the filter parameter can be used to filter
# on the ones to keep. The icons names shoud contain this string just after the entity type.
icons_config = [
	{
		"path": "./stix2-graphics/icons/png/",
		"filter": "-round-flat-300"
	}
]