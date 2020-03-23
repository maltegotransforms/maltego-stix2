#!/bin/bash

echo "Clear old results"
rm output/entities.mtz 2> /dev/null
rm output/entities.py 2> /dev/null
rm -R mtz/Icons/ mtz/Entities/ mtz/EntityCategories/ 2> /dev/null
mkdir mtz/ 2> /dev/null
mkdir mtz/Icons/
mkdir mtz/Icons/STIX2/
mkdir mtz/Entities/
mkdir mtz/EntityCategories/
mkdir output/ 2> /dev/null

echo "Add core entity"
cp ./templates/STIX2.core.entity ./mtz/Entities/

echo "Build Maltego Entities"
python3 build-stix-entities.py

echo "Process icons"
python3 build-icons.py

echo "Generate .mtz"
cd mtz
zip -q -x .empty -r ../output/entities.mtz ./Entities ./EntityCategories ./Icons
cd ../

echo "Copy entities.py in ./src/"
cp ./output/entities.py ./src/