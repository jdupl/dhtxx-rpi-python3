from setuptools import setup, find_packages

setup(
    name='DHT11',
    version='0.1.0',
    description='Library to get results from DHT11 sensor',
    url='https://github.com/jdupl/dht-python',
    author='Justin Duplessis',
    author_email='jdupl@linux.com',

    license='GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='dht11 iot raspberrypi rpi pi',
    packages=find_packages(exclude=['contrib', 'docs', 'tests',
                                    'usage_example.py']),
    install_requires=['RPi.GPIO'],
    extras_require={
        'test': ['nose'],
    }
)
