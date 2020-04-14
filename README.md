![alt text](./assets/card.png)

# Maltego STIX2 entities

This project allow you to generate a set of Maltego entities generated from official STIX 2 schemas.
It also contains generic transforms to explore the properties of STIX 2 entities.

## Dependencies in submodules

We are using the following assets to generate STIX2 Maltego entities:

- STIX 2 schemas : https://github.com/oasis-open/cti-stix2-json-schemas
- Icons : https://github.com/freetaxii/stix2-graphics (Copyright 2016-2019 Bret Jordan, All rights reserved.)

## Generation

```
$ git clone https://github.com/amr-cossi/maltego-stix2
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
$ git submodule update --remote
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

## Contributing

### Code of Conduct

We follow a standard [Code of Conduct](CODE_OF_CONDUCT.md) that we expect project participants to adhere to. Please read the [full text](CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.

### How to contribute

This module is not a huge project with an intense roadmap. Feel free to contribute through issues linked to pull requests for new features and bug solving.

### TODO: known wanted enhancements

- Rely on external library to parse JSON-ref files