# Linux Virtualization Server
An (awesome) alternative to ESXi.


## Introduction

### Commands


| Command           | Provided By   | Description                                                                     |
|------------------ | ------------- | ------------------------------------------------------------------------------- |
| `ipconfig`        |               | `ip` is more robust and should be used instead of `ipconfig`.                   |
| `ip`              |               | Manipulate interfaces, devices, routing, policy routing & tunnels (`man ip`).   |
| `dhclient`        |               |                                                                                 |
| `dnsmasq`         |               |                                                                                 |
| `brctl`           |               |                                                                                 |
| `vconfig`         | vlan          |                                                                                 |
| `ovs-vsctl`       | openvswitch   | manage the switch                                                               |
| `ovs-dpctl`       | openvswitch   | datapath management                                                             |
| `ovs ofctl`       | openvswitch   | openflow management                                                             |
| `ovs-vswitchd`    | openvswitch   | manage the switch configuration                                                 |


Note: `ipconfig` will not display interfaces configured by openvswitch, while `ip link show` will.


### Configuration Files

| Path                                  | Description                                                                 |
| ------------------------------------- | --------------------------------------------------------------------------- |
| `/etc/networks`                       | Routing configuration file.                                                 |
| `/etc/network/interfaces`             | NIC configuration file.                                                     |
| `/etc/resolv.conf`                    | "Finalized" DNS resolution configuration. Dynamically generated.            |
| `/etc/resolvconf/resolv.conf.d/base`  | Basic resolver information. Always included in resolv.conf.                 | 
| `/etc/resolvconf/resolv.conf.d/head`  | Prepended to resolv.conf.                                                   |
| `/etc/resolvconf/resolv.conf.d/tail`  | Appended to resolv.conf.                                                    | 
| `/etc/dhcp/dhclient.conf`             | 
| `/etc/default/openvswitch-switch`


### Example Commands

- `ip link show`
- `ip link set eth0 down`
- `ip link set eth0 up`
- `ip address show`
- `ip address add 1.1.1.1 dev eth0`
- `ip address add 1.1.1.1/24 dev eth0`
- `ip address delete 1.1.1.1 dev eth0`

    <!-- References
    http://www.tecmint.com/ip-command-examples/
    https://www.tty1.net/blog/2010/ifconfig-ip-comparison_en.html
    http://www.cyberciti.biz/faq/setting-up-an-network-interfaces-file/
    http://www.tldp.org/HOWTO/NET3-4-HOWTO.html
    http://linuxconfig.org/configuring-virtual-network-interfaces-in-linux
    http://xmodulo.com/install-configure-kvm-open-vswitch-ubuntu-debian.html
    -->

### Interfaces

- br0 - An internal, virtual bridged interface added automatically by kvm.
- virbr0 - An internal, nat interface added by kvm.


## Setup

### 8021q
First, we need to setup 802.1q (trunking):

    # install the vlan package
    sudo apt-get install vlan

    # enable the 8021q kernel module
    sudo modprobe 8021q

    # enable 8021q during boot
    sudo sh -c 'echo 8021q >> /etc/modules' 

Now, if you run `lsmod | grep 8021q`, you should see the kernel module loaded, and if you `cat /etc/modules` you should
should 8021q listed to start automatically during boot.

    <!--
    http://myhomelab.blogspot.com/2014/01/8021q-vlan-trunk-in-linux.html
    -->

### Openvswitch

- muti-layer virtual switching platform for linux
- supports netflow
- included in linux 3.3+ by default
- default switch for kvm

Setup instructions:

    # install packages
    sudo apt-get install openvswitch-switch openvswitch-common bridge-utils

    # display ovs interfaces (shouldn't be any)
    sudo ovs-vsctl show

    # add an internal bridge interfaces named "br0"
    sudo ovs-vsctl add-br br0

    # br0 should be displayed now
    sudo ovs-vsctl show

    # add the interface to the bridge (this will kill the connection)
    sudo ovs-vsctl add-port br0 p1p1

    # enable openvswitch bridge compatibility for applications without native support
    sudo bash -c 'echo "BRCOMPAT=yes" >> /etc/default/openvswitch-switch'

    # restart networking
    sudo service networking restart

    <!-- References
    http://openvswitch.org/
    http://assafmuller.com/2013/10/13/open-vswitch-basics/
    http://openvswitch.org/support/dist-docs/tutorial/Tutorial.md.txt
    http://networkstatic.net/openflow-openvswitch-lab/
    http://www.slideshare.net/rajdeep/openvswitch-deep-dive
    https://www.rivy.org/2012/11/switch-your-kvm-from-regular-bridge-to-open-vswitch/
    http://www.areteix.net/blog/2013/02/open-vswitch-on-ubuntu-12-04-lts/
    http://www.admin-magazine.com/CloudAge/Articles/Virtual-switching-with-Open-vSwitch
    https://www.rivy.org/2014/04/install-a-kvm-host-on-ubuntu-14-04-trusty-tahr/
    https://www.youtube.com/watch?v=SGjhx1SyzLE
    https://peterkieser.com/tag/openvswitch/
    https://www.snip2code.com/Snippet/185077/Open-vSwitch-with-KVM-for-Ubuntu-14-04
    -->

### KVM

    lsmod | grep kvm

    virbr0 - nat interface setup by libvirt

    /var/lib/libvirt/network/default.xm

    sudo virsh net-list

    sudo apt-get install gcc make autoconf automake gettext git nginx /
        python-cherrypy3 python-cheetah python-libvirt \
        libvirt-bin python-imaging \
        python-pam python-m2crypto python-jsonschema \
        qemu-kvm libtool python-psutil python-ethtool \
        sosreport python-ipaddr python-ldap \
        python-lxml nfs-common open-iscsi lvm2 xsltproc \
        python-parted python-guestfs libguestfs-tools \
        websockify novnc spice-html5

    wget -P /tmp http://kimchi-project.github.io/kimchi/downloads/kimchi-1.4.0-0.noarch.deb

    <--
    http://www.linux-kvm.org/page/Main_Page
    http://libvirt.org/

    https://github.com/kimchi-project/kimchi
    http://www.beisner.com/corp/virtual-bare-metal-provisioning-with-maas-on-kvm/
    http://www.jackwparks.com/2014/06/home-lab-openvswitch-vlans/
    http://www.microhowto.info/howto/configure_an_ethernet_interface_as_a_vlan_trunk.html
    http://myhomelab.blogspot.com/2014/01/8021q-vlan-trunk-in-linux.html
    http://2014.texaslinuxfest.org/sites/default/files/tlf_2014_kimchi-cloud.pdf

    http://ngineered.co.uk/howto-install-kvm-and-openvswitch-in-ubuntu-14-04/
    http://lost-and-found-narihiro.blogspot.com/2014/07/ubuntu-1404-install-open-vswitch-with.html
    -->
