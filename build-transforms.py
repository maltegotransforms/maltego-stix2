#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, sys

from maltego_stix2 import VERSION

from local_config import python_path, local_execution_path, trx_server_host, itds_seed_name
from maltego_stix2.config import _heritage_config


def row_to_itds_row(row, transform_function_name):
    description = row["description"]
    ui_name = description.split(":")[1].strip()
    ui_name = f"{ui_name} [STIX2]"
    input_type = row["input_type"]
    host = trx_server_host
    if host.endswith("/"):
        host = host[:-1]

    return {
        "Owner": "ANSSI",
        "Author": "Maltego, ANSSI",
        "Disclaimer": "",
        "Description": description,
        "Version": VERSION,
        "Name": transform_function_name,
        "UIName": ui_name,
        "URL": f"{host}/run/{transform_function_name}",
        "entityName": input_type,
        "oAuthSettingId": "",
        "transformSettingIDs": "",
        "seedIDs": itds_seed_name,
    }


def build(input_name, with_opencti=False):

    keys = ["Transform id", "Description", "Input type", "Sets"]

    t_template = ""
    with open("./templates/template.transform", "r") as i:
        t_template = i.read()

    ts_template = ""
    with open("./templates/template.transformsettings", "r") as i:
        ts_template = i.read()

    s_template = ""
    with open("./templates/template.tas", "r") as i:
        s_template = i.read()

    set_template = ""
    with open("./templates/template.set", "r") as i:
        set_template = i.read()

    python_template_file = ""
    with open("./templates/transform.py", "r") as i:
        python_template_file = i.read()

    csv_content = []
    with open(input_name) as csvfile:
        r = csv.reader(csvfile, delimiter=",", quotechar="'")
        for line in r:
            csv_content.append(line)

    transforms = ""
    transforms_sets = {}

    # Add a Maltego-Base -> Maltego-STIX2 convertion transform when a mapping is defined
    for stix_entity_name, maltego_entity_mapping in _heritage_config.items():
        if not maltego_entity_mapping.use_mapping_for_reverse_conversion:
            continue

        if stix_entity_name.startswith("x-opencti-") and not with_opencti:
            continue

        if not maltego_entity_mapping.entity_type:
            continue

        csv_content.append(
            [
                "stix2." + stix_entity_name + ".convert-to-stix",
                "STIX2: "
                    + maltego_entity_mapping.entity_type.split(".")[-1]
                    + " to STIX2",
                    maltego_entity_mapping.entity_type,
                    "STIX2-Converter",
                ]
            )

    itds_transforms_rows = []

    for row in csv_content[1:]:
        d = {}
        for key in keys:
            if csv_content[0].index(key) >= 0:
                d[key] = csv_content[0].index(key)
            else:
                print("A key is missing, exiting...")
                sys.exit(0)

        t_data = {
            "transformName": row[d["Transform id"]],
            "description": row[d["Description"]],
            "input_type": row[d["Input type"]],
        }
        if (
            t_data["input_type"].startswith("maltego.STIX2.x-opencti-")
            and not with_opencti
        ):
            continue
        else:
            t_output = t_template.format(**t_data)
            with open(
                "./mtz/TransformRepositories/Local/"
                + row[d["Transform id"]]
                + ".transform",
                "w",
            ) as o:
                o.write(t_output)

            if row[d["Sets"]] != "":
                sets = row[d["Sets"]].split(",")
                for cset in sets:
                    if cset not in transforms_sets:
                        transforms_sets[cset] = []
                    transforms_sets[cset].append(row[d["Transform id"]])

            transform_function = row[d["Transform id"]].replace(".","").replace("-","").replace("_","")

            itds_row = row_to_itds_row(t_data, transform_function)
            itds_transforms_rows.append(itds_row)

            ts_data = {
                "python_path": python_path,
                "local_execution_path": local_execution_path,
                "transform_function": transform_function,
            }
            ts_output = ts_template.format(**ts_data)
            with open(
                "./mtz/TransformRepositories/Local/"
                + row[d["Transform id"]]
                + ".transformsettings",
                "w",
            ) as o:
                o.write(ts_output)

            transforms += '      <Transform name="' + row[d["Transform id"]] + '"/>\n'

            with open("./trx/gunicorn/transforms/" + transform_function + ".py", "w") as o:
                o.write(python_template_file.format(
                    functionName=transform_function,
                    transformName=row[d["Transform id"]].split(".")[-1],
                    entityType=row[d["Input type"]]
                ))

    s_data = {"transforms": transforms[:-1]}
    s_output = s_template.format(**s_data)
    with open("./mtz/Servers/" + "Local.tas", "w") as o:
        o.write(s_output)

    for cset, ctransforms in transforms_sets.items():
        set_data = {
            "transformSetName": cset,
            "transforms": "\n".join(
                list(map(lambda r: '      <Transform name="' + r + '"/>', ctransforms))
            ),
        }
        set_output = set_template.format(**set_data)
        with open(
            "./mtz/TransformSets/"
            + cset.lower().replace(" ", "").replace(":", "")
            + ".set",
            "w",
        ) as o:
            o.write(set_output)

        tds_set_data = {
            "transformSetName": cset,
            "transforms": "\n".join(
                list(map(lambda r: '      <Transform name="paterva.v2.' + r.replace(".","").replace("-","").replace("_","") + '"/>', ctransforms))
            ),
        }
        tds_set_output = set_template.format(**tds_set_data)
        with open(
                "./mtz/TransformSetsTDS/"
                + cset.lower().replace(" ", "").replace(":", "")
                + ".set",
                "w",
        ) as o:
            o.write(tds_set_output)

    if itds_transforms_rows:
        with open("output/importable_itds_config.csv", "w") as outf:
            writer = csv.DictWriter(
                outf, fieldnames=list(itds_transforms_rows[0].keys()), delimiter=",", quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
            for data in itds_transforms_rows:
                writer.writerow(data)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        build(sys.argv[1], with_opencti=True)
    elif len(sys.argv) > 1:
        build(sys.argv[1])
    else:
        print("Expected use: build-transforms.py transforms.csv (--with-opencti)")
