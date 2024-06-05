from setuptools import setup

setup(
    name='battleship',
    packages=['battleship'],
    include_package_data=True,
    host='0.0.0.0',
    port=8002,
    install_requires=[
        'flask',
    ],
)