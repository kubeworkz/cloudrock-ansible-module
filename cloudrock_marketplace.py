#!/usr/bin/python
# has to be a full import due to Ansible 2.0 compatibility
import yaml
from ansible.module_utils.basic import AnsibleModule, to_text
from cloudrock_client import (
    CloudrockClientException,
    cloudrock_client_from_module,
    cloudrock_full_argument_spec,
)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'CloudRock',
}

DOCUMENTATION = '''
---
module: cloudrock_marketplace
short_description: Create order item in Cloudrock Marketplace.
version_added: 0.1
description:
  - Create marketplace order item via Cloudrock API.
requirements:
  - python = 3.8
  - requests
  - python-cloudrock-client
options:
  access_token:
    description:
      - An access token which has permissions to create a marketplace order item.
    required: true
  api_url:
    description:
      - Fully qualified url to the Cloudrock.
    required: true
  project:
    required: true
    description:
      - The name or UUID of the project to add an order item to.
  offering:
    required: true
    description:
      - The name or UUID of the offering to add an order item to.
  plan:
    required: true
    description:
      - The name or UUID of the order item plan.
  attributes:
    default: None
    description:
      - Order item attributes or path to JSON or YAML file with order item attributes.
  limits:
    default: None
    description:
      - Order item limits or path to JSON or YAML file with order item limits.
'''

EXAMPLES = '''
- name: Create a new marketplace order item.
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Add order item
      cloudrock_marketplace:
        access_token: b83557fd8e2066e98f27dee8f3b3433cdc4183ce
        api_url: https://cloudrock.example.com:8000/api
        project: Project
        offering: 7887745b83c74fc38d695ed58648ea20
        plan: 4d50f6584ed84df3b6c83075044fd284

- name: Create a new marketplace order item using names.
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Add order item
      cloudrock_marketplace:
        access_token: b83557fd8e2066e98f27dee8f3b3433cdc4183ce
        api_url: https://cloudrock.example.com:8000/api
        project: Project
        offering: Offering name
        plan: Plan name

- name: Create a new marketplace order item using attributes as file path.
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Add order item
      cloudrock_marketplace:
        access_token: b83557fd8e2066e98f27dee8f3b3433cdc4183ce
        api_url: https://cloudrock.example.com:8000/api
        project: Project
        offering: Offering name
        plan: Plan name
        attributes: /home/user/attributes

- name: Create a new marketplace order item using attributes as dictionary.
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Add order item
      cloudrock_marketplace:
        access_token: b83557fd8e2066e98f27dee8f3b3433cdc4183ce
        api_url: https://cloudrock.example.com:8000/api
        project: Project
        offering: Offering name
        plan: Plan name
        attributes:
          name: my name
'''


def send_request_to_cloudrock(client, module):
    project = module.params['project']
    offering = module.params['offering']
    plan = module.params['plan']
    attributes = module.params.get('attributes')
    limits = module.params.get('limits')

    def get_file_content(path):
        if path:
            value = yaml.safe_load(path)
            if isinstance(value, str):
                with open(value) as f:
                    return yaml.safe_load(f.read())
            else:
                return value

    attributes = get_file_content(attributes) or {}
    limits = get_file_content(limits) or {}

    response = client.create_marketplace_order(
        project, offering, plan, attributes, limits
    )
    order_item = response['items'][0]
    return order_item, True


def main():
    module = AnsibleModule(
        argument_spec=cloudrock_full_argument_spec(
            project=dict(type='str', required=True),
            offering=dict(type='str', required=True),
            plan=dict(type='str', required=True),
            attributes=dict(type='str', default=None),
            limits=dict(type='str', default=None),
        )
    )

    client = cloudrock_client_from_module(module)

    try:
        order_item, has_changed = send_request_to_cloudrock(client, module)
    except (IOError, OSError) as e:
        module.fail_json(msg="Unable to open file: %s" % to_text(e))
    except CloudrockClientException as e:
        module.fail_json(msg=str(e))
    else:
        module.exit_json(order_item=order_item, changed=has_changed)


if __name__ == '__main__':
    main()
