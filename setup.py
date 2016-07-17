from setuptools import setup, find_packages

setup(
    name='DHTxx',
    version='2.0.0',
    description='Library to get data from DHT11 or DHT22 sensor',
    url='https://github.com/jdupl/dht-python',
    author='Justin Duplessis',
    author_email='jdupl@linux.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='dhtxx dht22 dht11 iot raspberrypi rpi pi pine64',
    packages=find_packages(exclude=['contrib', 'docs', 'tests',
                                    'usage_example.py']),
    test_suite="tests",
    install_requires=['RPi.GPIO'],
    extras_require={
        'test': ['nose'],
    }
)
