#!/usr/bin/env python

from setuptools import setup

install_requires = [
    'requests>=2.6.0',
    'python-cloudrock-client>=0.1.7',
]

tests_requires = [
    'responses>=0.5.0',
]


setup(
    name='cloudrock-ansible-module',
    version='1.1.2',
    author='ClourRock Team',
    author_email='support@cloudrock.ca',
    url='https://cloudrock.ca',
    license='MIT',
    description='Ansible module for the Cloudrock API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=[
        'cloudrock_client',
        'cloudrock_marketplace',
        'cloudrock_marketplace_os_get_instance',
        'cloudrock_marketplace_os_instance',
        'cloudrock_marketplace_os_volume',
        'cloudrock_os_floating_ip',
        'cloudrock_os_instance_volume',
        'cloudrock_os_security_group',
        'cloudrock_os_security_group_gather_facts',
        'cloudrock_os_snapshot',
        'cloudrock_batch_allocation',
        'cloudrock_batch_offering',
    ],
    install_requires=install_requires,
    tests_require=tests_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
