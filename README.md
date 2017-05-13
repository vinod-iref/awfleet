Give the awfleet file execution permissions by:
  - sude chmod 755 awfleet

First run the following command and configure the region, secret and access keys and give it a block name:
  - ./awfleet --configure

Give the json file containing the spot instance specifications to the program with the following command:
  - ./awfleet --request-spot path/to/config.json