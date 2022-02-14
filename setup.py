from setuptools import find_packages, setup

setup(
    name='genomaviz',
    packages=find_packages(include=['genomaviz']),
    version='0.1.2',
    description='Python library for Genomawork visualizations',
    author='Tamara Cucumides - Pablo Larrea',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
