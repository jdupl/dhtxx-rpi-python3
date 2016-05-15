from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='DHT11',
    ext_modules=cythonize("dht11.pyx"),
)
