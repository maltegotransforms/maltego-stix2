# Maltego STIX2 entities

This project allow you to generate a set of Maltego entities generated from official STIX 2 schemas.
It also contains generic transforms to explore the properties of STIX 2 entities.

## Sources in submodule

We are using the following sources to generate Maltego entities:

- STIX 2 schemas : https://github.com/oasis-open/cti-stix2-json-schemas
- Icons : https://freetaxii.github.io/stix2_0

## Generation

```
$ git clone https://github.com/OpenCTI-Platform/maltego-stix2
$ cd maltego-stix2
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

The local transforms are leveraging the Maltego TRX library. The first step is to create the configuration file:

```
$ cp config.py.sample config.py
```

Update the file according to your setup and your needs and then execute:

To generate the `entities.mtz` file:

```
$ git submodule update
$ ./build_entities.sh
```

To generate the `transforms.mtz` file:

```
$ ./build_transforms.sh
```

If you specified a different path for the `src` directory of this repository, please copy the content in it:

```
$ cp -a src /path/to/your/project/maltego-stix2/src
```

## Use

Import the files `output/entities.mtz` and `output/transforms.mtz` in Maltego using the "Import config" menu.
