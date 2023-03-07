from setuptools import setup, find_packages

setup(
    name='sandwich_shop',
    version='1.0',
    packages=[find_packages()],
    install_requires=[
        # Add any dependencies your package requires here
    ],
    entry_points={
        'runners': [
            'sandwich_shop = sandwich_shop:main'
        ]
    }
)
