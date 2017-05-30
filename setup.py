import setuptools

__version__ = "0.1.0"

install_requires = [x.strip() for x in open('requirements.txt').readlines()]

setuptools.setup(
    name="Hameg Plug",
    version=__version__,
    url="https://jonas.steinka.mp",

    author="Jonas Steinkamp",
    author_email="jonas@steinka.mp",

    description="A package with some hameg plug for the openhtf framework.",
    long_description=open('README.md').read(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 2.7',
    ],

    include_package_data=True,
    packages=setuptools.find_packages(),

    install_requires=install_requires,
)
