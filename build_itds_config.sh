#!/bin/bash
echo "Clear old results"
rm output/itds-config.mtz 2> /dev/null

echo "Create iTDS MTZ package"
# this renaming shuffle is needed while the pTDS does not yet accept "." and "-" in transform names
cd mtz
mv ./TransformSets ./TransformSetsBackup
mv ./TransformSetsTDS ./TransformSets
zip -q -x .empty -r ../output/itds-config.mtz ./TransformSets ./Entities ./EntityCategories ./Icons
mv ./TransformSets ./TransformSetsTDS
mv ./TransformSetsBackup ./TransformSets
cd ../

echo "All done. MTZ packages can be imported in Maltego and don't forget to copy ./trx/gunicorn/ at the execution path provided in the configuration."
