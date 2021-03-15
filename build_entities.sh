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
cp ./templates/maltego.STIX2.core.entity ./mtz/Entities/

echo "Build Maltego Entities"
if [ $# -eq 0 ] ;
then
	python3 build-stix-entities.py
else
	python3 build-stix-entities.py --with-opencti
fi

echo "Process icons"
if [ $# -eq 0 ] ;
then
	python3 build-icons.py
else
	python3 build-icons.py --with-opencti
fi

echo "Generate .mtz"
cd mtz
zip -q -x .empty -r ../output/entities.mtz ./Entities ./EntityCategories ./Icons
cd ../

echo "All done. MTZ packages can be imported in Maltego."