# dht11-python
Read a DHT11 sensor from any Raspberry Pi (or Pine64 with [port](https://github.com/swkim01/RPi.GPIO-PineA64)) with Python 3.x


## Install library

#### Manually

`sudo python3 setup.py install`

#### Pip

`pip install -e git+ssh://github.com/jdupl/dht11-python.git#egg=DHT11`

#### Setup-requires

`-e git+ssh://github.com/jdupl/dht11-python.git#egg=DHT11`


## Usage
See `usage_example.py`.


## Run tests

Recommended: `virtualenv env && . env/bin/activate`

`python3 setup.py tests`
