from setuptools import setup, find_packages


setup(
    name='sese',
    version='1.0',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        
    ],
    entry_points={
        'console_scripts': ['sese = sese.__main__:main']
    }
)
