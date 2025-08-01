
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import json
import pytest
import os

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('instance')


def pp_json(json_thing, sort=True, indents=2):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def base_directory():
    """
    """
    cwd = os.getcwd()

    if 'group_vars' in os.listdir(cwd):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = f"molecule/{os.environ.get('MOLECULE_SCENARIO_NAME')}"

    return directory, molecule_directory


def read_ansible_yaml(file_name, role_name):
    """
    """
    read_file = None

    for e in ["yml", "yaml"]:
        test_file = "{}.{}".format(file_name, e)
        if os.path.isfile(test_file):
            read_file = test_file
            break

    return f"file={read_file} name={role_name}"


@pytest.fixture()
def get_vars(host):
    """
        parse ansible variables
        - defaults/main.yml
        - vars/main.yml
        - vars/${DISTRIBUTION}.yaml
        - molecule/${MOLECULE_SCENARIO_NAME}/group_vars/all/vars.yml
    """
    base_dir, molecule_dir = base_directory()
    distribution = host.system_info.distribution
    operation_system = None

    if distribution in ['debian', 'ubuntu']:
        operation_system = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        operation_system = "redhat"
    elif distribution in ['arch', 'artix']:
        operation_system = f"{distribution}linux"

    # print(" -> {} / {}".format(distribution, os))
    # print(" -> {}".format(base_dir))

    file_defaults = read_ansible_yaml(f"{base_dir}/defaults/main", "role_defaults")
    file_vars = read_ansible_yaml(f"{base_dir}/vars/main", "role_vars")
    file_distibution = read_ansible_yaml(f"{base_dir}/vars/{operation_system}", "role_distibution")
    file_molecule = read_ansible_yaml(f"{molecule_dir}/group_vars/all/vars", "test_vars")
    # file_host_molecule = read_ansible_yaml("{}/host_vars/{}/vars".format(base_dir, HOST), "host_vars")

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")
    # host_vars          = host.ansible("include_vars", file_host_molecule).get("ansible_facts").get("host_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)
    # ansible_vars.update(host_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def test_directories(host, get_vars):
    """
    """
    directories = [
        "/etc/postfix",
        "/etc/postfix/maps.d",
        "/etc/postfix/postfix-files.d",
        "/etc/postfix/dynamicmaps.cf.d",
        "/etc/postfix/virtual",
        "/etc/postfix/sasl",
    ]
    directories.append(get_vars.get("postfix_config_directory"))

    for dirs in directories:
        d = host.file(dirs)
        assert d.is_directory


def test_files(host, get_vars):
    """
      created config files
    """
    files = [
        "/etc/postfix/main.cf",
        "/etc/postfix/maps.d/generic",
        "/etc/postfix/maps.d/header_checks",
        "/etc/postfix/maps.d/recipient_canonical_maps",
        "/etc/postfix/maps.d/sender_canonical_maps",
        "/etc/postfix/maps.d/sender_dependent_relayhost_maps",
        "/etc/postfix/maps.d/transport_maps",
        "/etc/postfix/maps.d/virtual",
        "/etc/postfix/master.cf",
        "/etc/postfix/virtual/mysql/mc_mbr_access_maps.cf",
        "/etc/postfix/virtual/mysql/mc_recipient_bcc_maps.cf",
        "/etc/postfix/virtual/mysql/mc_recipient_canonical_maps.cf",
        "/etc/postfix/virtual/mysql/mc_relay_ne.cf",
        "/etc/postfix/virtual/mysql/mc_relay_recipient_maps.cf",
        "/etc/postfix/virtual/mysql/mc_sasl_access_maps.cf",
        "/etc/postfix/virtual/mysql/mc_sasl_passwd_maps.cf",
        "/etc/postfix/virtual/mysql/mc_sasl_passwd_maps_sender_dependent.cf",
        "/etc/postfix/virtual/mysql/mc_sasl_passwd_maps_transport_maps.cf",
        "/etc/postfix/virtual/mysql/mc_sender_bcc_maps.cf",
        "/etc/postfix/virtual/mysql/mc_sender_dependent_default_transport_maps.cf",
        "/etc/postfix/virtual/mysql/mc_tls_enforce_in_policy.cf",
        "/etc/postfix/virtual/mysql/mc_tls_policy_override_maps.cf",
        "/etc/postfix/virtual/mysql/mc_transport_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_alias_domain_catchall_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_alias_domain_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_alias_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_domains_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_mailbox_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_relay_domain_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_resource_maps.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_sender_acl.cf",
        "/etc/postfix/virtual/mysql/mc_virtual_spamalias_maps.cf",
    ]

    files.append(get_vars.get("postfix_mailname_file"))
    files.append(get_vars.get("postfix_aliases_file"))

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """
      created user
    """
    shell = '/usr/sbin/nologin'

    distribution = host.system_info.distribution

    if distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        shell = "/sbin/nologin"
    elif distribution == 'arch':
        shell = "/usr/bin/nologin"
    elif distribution == 'artix':
        shell = "/bin/nologin"

    user_name = "postfix"
    u = host.user(user_name)
    g = host.group(user_name)

    assert g.exists
    assert u.exists
    assert user_name in u.groups
    assert u.shell == shell


def test_service_running_and_enabled(host, get_vars):
    """
      running service
    """
    service_name = "postfix"

    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def test_listening_socket(host, get_vars):
    """
    """
    listening = host.socket.get_listening_sockets()
    interfaces = host.interface.names()
    eth = []

    if "eth0" in interfaces:
        eth = host.interface("eth0").addresses

    for i in listening:
        print(i)

    for i in interfaces:
        print(i)

    for i in eth:
        print(i)

    distribution = host.system_info.distribution
    release = host.system_info.release

    bind_address = eth[0]
    bind_port = 25
    socket_name = "private/smtp"

    listen = []
    listen.append(f"tcp://{bind_address}:{bind_port}")

    if not (distribution == 'ubuntu' and release == '18.04'):
        listen.append(f"unix://{socket_name}")

    for spec in listen:
        socket = host.socket(spec)
        assert socket.is_listening
