# DHTxx-python
Read a DHT11 or DHT22 sensor from any Raspberry Pi (or Pine64 with [port](https://github.com/swkim01/RPi.GPIO-PineA64)) with Python 3.x


## Install library

#### Manually

`sudo python3 setup.py install`

#### Pip

`pip install -e git+ssh://github.com/jdupl/dhtxx-python3.git#egg=DHTxx`

#### Setup-requires

`-e git+ssh://github.com/jdupl/dhtxx-python3.git#egg=DHTxx`


## Usage
See `usage_example.py`.


## Run tests

Recommended: `virtualenv env && . env/bin/activate`

`python3 setup.py tests`
