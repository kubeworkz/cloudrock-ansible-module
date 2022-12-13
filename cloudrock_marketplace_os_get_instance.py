#!/usr/bin/python
# has to be a full import due to Ansible 2.0 compatibility
from ansible.module_utils.basic import AnsibleModule
from cloudrock_client import CloudrockClientException, cloudrock_client_from_module

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'CloudRock',
}

DOCUMENTATION = '''
---
module: cloudrock_marketplace_os_get_instance
short_description: Get existing OpenStack instance
version_added: 0.1
description:
  - Get an OpenStack instance
requirements:
  - python = 3.8
  - requests
  - python-cloudrock-client
options:
  access_token:
    description:
      - An access token which has permissions to create an OpenStack instances.
    required: true
  api_url:
    description:
      - Fully qualified url to the Cloudrock.
    required: true
  name:
    description:
      - The name or UUID of existing OpenStack instance.
    required: true
  project:
    description:
      - The name or UUID of the project where instance is created.
    required: true
'''

EXAMPLES = '''
- name: Get an OpenStack instance
  hosts: localhost
  tasks:
    - name: get instance
      cloudrock_marketplace_os_get_instance:
        access_token: b83557fd8e2066e98f27dee8f3b3433cdc4183ce
        api_url: https://cloudrock.example.com:8000/api
        name: Warehouse instance
        project: OpenStack Project
'''


def main():
    fields = {
        'api_url': {'required': True, 'type': 'str'},
        'access_token': {'required': True, 'type': 'str'},
        'name': {'required': True, 'type': 'str'},
        'project': {'required': False, 'type': 'str'},
    }
    module = AnsibleModule(argument_spec=fields)

    client = cloudrock_client_from_module(module)
    try:
        instance = client.get_instance_via_marketplace(
            name=module.params['name'],
            project=module.params['project'],
        )
    except CloudrockClientException as e:
        module.fail_json(msg=str(e))
    else:
        module.exit_json(instance=instance)


if __name__ == '__main__':
    main()
