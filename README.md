# Maltego STIX2 entities

This project allow you to generate a set of Maltego entities generated from official STIX 2 schemas.

## Sources in submodule

We are using the following sources to generate Maltego entities:

- STIX 2 schemas : https://github.com/oasis-open/cti-stix2-json-schemas
- Icons : https://freetaxii.github.io/stix2_0

## Generation

```
$ git clone https://github.com/amr-cossi/Maltego-STIX2
$ cd Maltego-STIX2
$ git submodule init
```

### Requirements

Please install the following requirements before generating the Maltego entities:

- Python >= 3.6
- Libraries in requirements.txt

```
$ pip3 install -r requirements.txt
```

### Generate

To generate 

```
$ git submodule update
$ ./build.sh
```

## Use

Import the file `entities.mtz` in Maltego using the "Import config" menu.

## TODO

- Add mini-transforms to extract data from fields : e.g : explode alias