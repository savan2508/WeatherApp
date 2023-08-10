from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='weathermap',
    version='1.0.8',
    packages=['weathermap'],
    description='Openweathermap api simplified',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Savan Patel',
    author_email='sawanpatel2508@gmail.com',
    url='https://github.com/savan2508/WeatherApp',
    keywords=['weather', 'forecast', 'openweathermap', 'openweather'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
