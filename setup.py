from setuptools import find_packages, setup
setup(
    name='B2912A_lib',
    packages=['B2912A_lib'],
    version='1.0.1',
    description='A Semtech/Agilent B2912A SMU library',
    author='Enric Puigvert Coromina',
    license='Universitat de Barcelona',
    install_requires=['pyvisa', 'pyvisa_py','numpy'],
    setup_requires=['pytest-runner'],
    test_suite='tests',
)
