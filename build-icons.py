import os
from PIL import Image

icon_path = "./stix2-graphics/icons/png/"
model = "-round-flat-300"
output_dir = "./mtz/Icons/STIX2"

for dirName, subdirList, fileList in os.walk(icon_path):
    for fname in fileList:
        if model in fname:
        	image = Image.open(os.path.join(dirName, fname))

        	entity_name = "stix2_"+fname.split(model)[0].replace("-", "_")
        	entity_name = entity_name.replace("coa", "course_of_action")

        	new_image_96 = image.resize((96, 96))
        	new_image_96.save(os.path.join(output_dir, entity_name+"96.png"))

        	new_image_48 = image.resize((48, 48))
        	new_image_48.save(os.path.join(output_dir, entity_name+"48.png"))

        	new_image_32 = image.resize((32, 32))
        	new_image_32.save(os.path.join(output_dir, entity_name+"32.png"))

        	new_image_24 = image.resize((24, 24))
        	new_image_24.save(os.path.join(output_dir, entity_name+"24.png"))

        	new_image_16 = image.resize((16, 16))
        	new_image_16.save(os.path.join(output_dir, entity_name+".png"))