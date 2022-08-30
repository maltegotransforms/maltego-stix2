#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from PIL import Image
from maltego_stix2.config import _icons_config


def save_image(icon_path, size, out_path):
    im = Image.open(icon_path)
    im.thumbnail((size, size), Image.Resampling.BICUBIC)
    with open(out_path, "wb") as outfile:
        im.save(outfile, "PNG")
    im.close()


def build(with_opencti=False):
    output_dir = "./mtz/Icons/STIX2"

    for icons in _icons_config:
        for dirName, subdirList, fileList in os.walk(icons["path"]):
            for fname in fileList:
                if icons["filter"] in fname:
                    inpath = os.path.join(dirName, fname)

                    entity_name = "stix_two_" + fname.split(icons["filter"])[0].replace("-", "_")
                    for k, v in icons["replace"].items():
                        entity_name = entity_name.replace(k, v)

                    if not entity_name.startswith("x_opencti_") or with_opencti:
                        save_image(inpath, 48, os.path.join(output_dir, entity_name + "48.png"))
                        save_image(inpath, 32, os.path.join(output_dir, entity_name + "32.png"))
                        save_image(inpath, 24, os.path.join(output_dir, entity_name + "24.png"))
                        save_image(inpath, 16, os.path.join(output_dir, entity_name + ".png"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        build(with_opencti=True)
    else:
        build()
