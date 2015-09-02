#!/usr/bin/python
from ovirtsdk.api import API
from ovirtsdk.xml import params
## All existent bond should be listed here.
## the list can be obtained using SDK.
bonds = ['bond0']

api = API (url = "https://rhevm.example.com",
           username = 'admin@internal',
           password = 'XXX',
           ca_file = "/etc/pki/ovirt-engine/ca.pem",
           persistent_auth = False);

## take first host
## Can be done by name or id as well
## host = api.hosts.get(name = "XXXX")
host = api.hosts.list()[0]

hostnics = host.nics.list()

## The logic here is to filter out bond slaves
## It can be done in more elegant way by using nic.get_bonding().get_slaves...
## We have to include nics with assigned networks and bond interfaces
## Bond slaves should be filtered out
setupnics = [nic for nic in hostnics if nic.get_network() or nic.get_name() in bonds]
newnic = params.HostNIC (network = params.Network(name = 'addme'),
                          name = 'bond0.2',
                          boot_protocol = "static",
                          ip = params.IP(
                              address = "192.168.176.2",
                              netmask = '255.255.255.0',
                              gateway = '192.168.176.1'),
                          override_configuration = 'true'
                          )
print("Trying to call setupnetworks with the list : %s " %",".join([x.get_name() for x in setupnics]))

for nic in hostnics:
    nic.set_override_configuration(True)

host.nics.setupnetworks (params.Action (force = 'false',
                                       check_connectivity = "true",
                                       host_nics = params.HostNics (host_nic = setupnics + [newnic])))

