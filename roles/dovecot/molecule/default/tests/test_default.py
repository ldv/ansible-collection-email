
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import json
import pytest
import os

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


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
        test_file = f"{file_name}.{e}"
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


@pytest.mark.parametrize("dirs", [
    "/etc/dovecot",
    "/etc/dovecot/auth.d",
    "/etc/dovecot/conf.d",
    "/etc/dovecot/sql.d",
    "/var/log/dovecot"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory


@pytest.mark.parametrize("files", [
    "/etc/dovecot/dovecot.conf",
    "/etc/dovecot/dovecot-dict-auth.conf.ext",
    "/etc/dovecot/dovecot-dict-sql.conf.ext",
    "/etc/dovecot/dovecot-ldap.conf.ext",
    "/etc/dovecot/dovecot-sql.conf.ext",
    "/etc/dovecot/conf.d/10-auth.conf",
    "/etc/dovecot/conf.d/10-director.conf",
    "/etc/dovecot/conf.d/10-logging.conf",
    "/etc/dovecot/conf.d/10-mail.conf",
    "/etc/dovecot/conf.d/10-master.conf",
    "/etc/dovecot/conf.d/10-ssl.conf",
    "/etc/dovecot/conf.d/10-tcpwrapper.conf",
    "/etc/dovecot/conf.d/15-lda.conf",
    "/etc/dovecot/conf.d/15-mailboxes.conf",
    "/etc/dovecot/conf.d/20-imap.conf",
    "/etc/dovecot/conf.d/20-lmtp.conf",
    "/etc/dovecot/conf.d/20-managesieve.conf",
    "/etc/dovecot/conf.d/20-pop3.conf",
    "/etc/dovecot/conf.d/20-submission.conf",
    "/etc/dovecot/conf.d/90-acl.conf",
    "/etc/dovecot/conf.d/90-plugin.conf",
    "/etc/dovecot/conf.d/90-quota.conf",
    "/etc/dovecot/conf.d/90-sieve-extprograms.conf",
    "/etc/dovecot/conf.d/90-sieve.conf",
    "/etc/dovecot/auth.d/auth-checkpassword.conf.ext",
    "/etc/dovecot/auth.d/auth-deny.conf.ext",
    "/etc/dovecot/auth.d/auth-dict.conf.ext",
    "/etc/dovecot/auth.d/auth-ldap.conf.ext",
    "/etc/dovecot/auth.d/auth-master.conf.ext",
    "/etc/dovecot/auth.d/auth-passwdfile.conf.ext",
    "/etc/dovecot/auth.d/auth-sql.conf.ext",
    "/etc/dovecot/auth.d/auth-static.conf.ext",
    "/etc/dovecot/auth.d/auth-system.conf.ext",
    "/etc/dovecot/auth.d/auth-vpopmail.conf.ext",
])
def test_files(host, files):
    f = host.file(files)
    assert f.is_file


def test_service_running_and_enabled(host, get_vars):
    """
      running service
    """
    service_name = "dovecot"

    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def test_listening_socket(host, get_vars):
    """
    """
    listening = host.socket.get_listening_sockets()

    for i in listening:
        print(i)

    listen = []
    listen.append("tcp://0.0.0.0:110")
    listen.append("tcp://0.0.0.0:143")
    listen.append("tcp://0.0.0.0:993")
    listen.append("tcp://0.0.0.0:995")

    for spec in listen:
        socket = host.socket(spec)
        assert socket.is_listening
