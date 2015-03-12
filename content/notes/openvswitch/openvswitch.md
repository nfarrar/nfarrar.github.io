# Open vSwitch

## Overview
I started learning about [Open vSwitch][] because I wanted to start building more advanced networking topologies for my
home/lab [VMWare ESXi][] server. I've been using the free [VMWare ESXi][] hypervisor at home for several years now, and
I've started to feel the pain of the free version's limitations:

- No API access
- No Programmatic Interface/bindings for languages
- Management requires running a dedicated Windows VM for the client application
- No Web Interface

KVM by itself is great, but some of the things I do with ESXi becomes difficult (or impossible) without integrated
network virtualization (build into ESXi)

- Multiple virtualized firewalls
- Virtualized VPN server
- Virtualized IDS/network taps

I found the learning curve for [Open vSwitch][] to be pretty gnarly, so I focused on learning some basics
& troubleshooting first. I recommend installing it in a local VM to play around first and get comfortable with it,
before deploying.

### Server Hardware
In my basement, I have a rack, running on a dedicated power circuit, with various switches & routers, a NAS, and
a single VM Server. The VM Server runs my network & lab infrastructure. The hardware consists of my old gaming rig,
repurposed with some additional server-specific components:

- NORCO RPC-250, 2U Rack Mount Chassis
- ASUS Sabertooth X79 LGA 2011 Intel X79
- Intel Core i7-3820 
- Cooler Master GeminII M4 - Low Profile CPU Cooler
- G.SKILL Ripjaws Z Series 64GB
- Intel Pro 1000 PT Quad Port Gigabit PCIe NIC (EXPI9404PTG1P20)
- LSI Internal SATA/SAS 9211-8i 6Gb/s Raid Controller
- Samsung 840 Pro Series 256GB SSD (4x,Raid 0)
- ICY DOCK EZ-FIT MB990SP-B 2 x 2.5 Inch to 3.5 Chassis (2x for 4x SSDs)
- WD VelociRaptor WD5000HHTZ 10k 500GB (4x, Raid5)
- Athena Power AP-P4ATX85FE SLI Ready Active PFC 
- EVGA 512-P3-1300-LR GeForce 8400 GS 512MB Low Profile Video Card
- LG WH10LS30 10X Blu-ray Burner

The components are not *perfect*, the motherboard, processor, and original 32MB of memory were purchased for an
overclocked gaming rig. After running out of time to play games, I decided to repupose it as a VM server. The rack mount
case was a snap-decision, and caused a lot of difficulty - 2U is very limiting (in terms of space) and it was *really*
hard to cram everything in. Due to the case height I had a *very* limited set of options for the CPU cooler - none of my
Noctua or cooler-master heatsinks would fit in the case - and the Gemini was one of the only options I could find that
would fit well and keep the temperatures at an acceptable level.

I also snagged a Lantronix KVM/IP spider for cheap off craigslist for out of band, remote management since the processor
doesn't have KVM-IP built in, like a lot of the new Intel processors.

Overall, it's a great server for my own home/home office setup, but if I was to do it over from scratch with better
planning I'd do things very differently.

## Fundamentals


- http://www.jedelman.com/home/open-vswitch-101
- http://horms.net/projects/openvswitch/2012-01/openvswitch.en.pdf
- http://networkstatic.net/openvswitch-configure-from-packages-and-attaching-to-a-floodlight-openflow-controller/ 
 

### Terminology

| Terminology           | Description                                                                               |
| --------------------- | ----------------------------------------------------------------------------------------- |
| Bridge                | A bridge is a *"virtual switch"*. They can contain many *ports*.                          |
| Controller            |                                                                                           |
| Datapath              |                                                                                           |
| Flow                  |                                                                                           |
| Interface             | An ovs interface is a virtual NIC. They are always contained by an ovs *port*.            |
| Megaflow              |                                                                                           |
| Port                  | An ovs port is a (virtual) virtual interface. A port contains one or more interfaces.     |

### Components

| Component             | Run Level     | Description                                                               |
| --------------------- | ------------- | ------------------------------------------------------------------------- |
| openvswitch_mod.ko    | Kernel Space  | 
| ovs-vswitchd          | User Space    | 
| ovsdb-server          | User Space    | 


Kernel module (Fast path) – I would equate the kernel module to ASICs on a hardware switch.  It is where all of your
packet processing takes place, i.e. data plane.  The Virtual Ethernet Module (VEM) in the Nexus 1000V would be
comparable to the kernel module in Open vSwitch.

vSwitch daemon (ovs-vswitchd) – also called a controller in some documentation, is the Linux process that runs in user
space (not the kernel) that dictates how the kernel  module will be programmed – think of this as a locally significant
control plane.  This daemon runs on every physical host.  Because I am seeing this called a controller in some docs, it
is important to understand, this is not a SDN or OpenFlow controller by any means and it’s just a controller in the
sense that it controls a local data plane module. 

Database Server – More officially, it is called the Open vSwitch Database (OVSDB) server.  If you choose to run the
vSwitch daemon, you will need this database.  This is the database that will store all of your cool and working
configurations.  Luckily this isn’t OpenStack and you don’t need to go out and learn MySQL or anything like that (I kid,
I kid).  This server uses JSON for its database schema and it communicates externally and to the vSwitch daemon using
a management protocol, namely OVSDB, which is using JSON-RPC.

## Commands
There are a ton of command interfaces for Open vSwitch. As I learned them, I started adding them to the following
"cheatsheet" with a short description so I had something to reference:

| Command       | Subcommand                    | Description                                                       |
| ------------- | ----------------------------- | ----------------------------------------------------------------- |
| ovs-vsctl     | *                             | Utility for querying & configuring ovs-svswitchd.                 |
| ovs-appctl    | *                             | Utility for configuring running open vswitch daemons.             |
| ovs-ofctl     | *                             | Utility for interfacing with open flow switch instances.          | 
| ovs-vswitchd  | *                             | Utility for interfacing with a vswitchd instance.                 |
| ovs-dpctl     | *                             | Utility for configuring datapaths.                                |
| ovsdb-tool    | *                             | Utility for managing Open vSwitch databases.                      |
| ovs-vsctl     | show                          |                                                                   |
| ovs-vsctl     | list br                       |                                                                   | 
| ovs-vsctl     | list port                     |                                                                   |
| ovs-vsctl     | list [table]                  |                                                                   |
| ovs-vsctl     | list-br                       |                                                                   | 
| ovs-vsctl     | list-ports [bridge]           |                                                                   | 
| ovs-vsctl     | add-br [bridge]               |                                                                   |
| ovs-vsctl     | add-port [bridge] [port]      |                                                                   |
| ovs-ofctl     | dump-flows [bridge]           |                                                                   |
| ovs-ofctl     | add-flow [bridge] [flow]      |                                                                   |
| ovs-ofctl     | del-flows [bridge] [flow]     |                                                                   |
| ovs-ofctl     | snoop [bridge]                |                                                                   |
| ovs-appctl    | bridge/dump-flows [bridge]    |                                                                   |
| ovs-dpctl     | show                          |                                                                   |
| ovs-dpctl     | show                          | Show datapaths and attached interfaces.                           |
| ovs-dpctl     | dump-flows [bridge]           |                                                                   |
| ovs-dpctl     | dump-dps
| ovsdb-tool    | show-log                      |                                                                   |

On Ubuntu, Open vSwitch includes a sysv init script for managing the openvswitch-switch service with:

- `service openvswitch-switch status`
- `service openvswitch-switch start`
- `service openvswitch-switch restart`
- `service openvswitch-switch stop`

### Files

| File                          | Description                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------- |
| /var/log/messages             |                                                                                   |
| /var/log/openvswitch          |                                                                                   |
| /etc/openvswitch/conf.db      |                                                                                   |


## Lab Setup

### Basic Installation & Configuration
This walks through a rediculously basic setup of Open vSwitch on Ubuntu 14.04, with some linux networking fundamentals.
When I started trying to figure out Open vSwitch I needed to learn a bunch of this stuff and figuring it out took a lot
experimentation.

The default Ubuntu repositories have a precompiled Open vSwitch package for Ubuntu 14.04:

    sudo apt-get -y install openvswitch-switch

This installs the openvswitch-switch sysv init script, which allows us to control the openvswitch service:

    $ sudo service openvswitch status
    openvswitch-switch start/running

To look at what's been modified and installed by default, we can use `ip`, `ovs-vsctl show` and `ovs-dpctl show`:

    $ sudo ip link show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default 
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    3: ovs-system: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default 

    $ sudo ovs-vsctl show
    766fec6a-e1a9-42ad-84b9-e62e4e11caac
    ovs_version: "2.0.2"

    $ sudo ovs-dpctl show
	lookups: hit:37470 missed:1082 lost:0
	flows: 0
	port 0: ovs-system (internal)

The `ovs-system` interface required by linux to make Open vSwitch work correctly. The interface has the same name as the
default datapath. I haven't had a need to look into this too deeply yet, so I'm not sure if there is anything more
interesting about this.

Open vSwitch uses bridges to connect networks - in the ESXi world these are labeled as *"Virtual Switches"*. So our
first step is to create a bridge/virtual switch that connects Open vSwitch to the physical network. In my configuration,
the NIC connected to the physical network (not really, because this is a VM) is eth0.

To create our bridge, we use `ovs-vsctl add-br [bridge-name]`:

    $ ovs-vsctl add-br ovsbr0

Note: We can use any naming convention we want for the names, and most guides use `br0`, `br1`, etc. I've found that
(for me) prefixing the name with `ovs` makes things more clear once we start adding other types of virtual devices into
the mix with [KVM][]/[libvirt][], etc.

Now if we look at our interfaces, we'll see the ovs-br0:

    $ ip link show
    4: ovs-br0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default 

    $ sudo ovs-vsctl show
    766fec6a-e1a9-42ad-84b9-e62e4e11caac
        Bridge "ovsbr0"
            Port "ovsbr0"
                Interface "ovsbr0"
                    type: internal
        ovs_version: "2.0.2"

    $ sudo ovs-dpctl show
    system@ovs-system:
        lookups: hit:37475 missed:1085 lost:0
        flows: 0
        port 0: ovs-system (internal)
        port 1: ovsbr0 (internal)

And to bridge the virtual switch into the host's physical network, we need to add the port to the bridge (beware, this
will take down communications):

    $ sudo ovs-vsctl add-port ovsbr0 eth0

After adding eth0 to our bridge, communications are *"mysteriously"* disabled. If we take a look at our interfaces, we
see `eth0` and `br0`:

    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
        link/ether 00:0c:29:6a:26:3f brd ff:ff:ff:ff:ff:ff
        inet 172.16.18.105/24 brd 172.16.18.255 scope global eth0
        valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe6a:263f/64 scope link 
        valid_lft forever preferred_lft forever

    4: ovsbr0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default 
        link/ether 00:0c:29:6a:26:3f brd ff:ff:ff:ff:ff:ff
        inet6 fe80::60f2:51ff:fe2e:cb4/64 scope link 
        valid_lft forever preferred_lft forever

And we see the ports (bridge & NIC) in the datapath configuration:

    $ sudo ovs-dpctl show
    system@ovs-system:
        lookups: hit:37690 missed:1108 lost:0
        flows: 2
        port 0: ovs-system (internal)
        port 1: ovsbr0 (internal)
        port 2: eth0

If we take a look at our rating table, we see nothings changed from the way it would be on a *default* system setup:

    $ sudo ip route
    default via 172.16.18.1 dev eth0 
    172.16.18.0/24 dev eth0  proto kernel  scope link  src 172.16.18.105 

The `eth0` interface has an IP, and the interfaces IP address is being used to setup our default route. Since our
*topology* has changed - we don't want packets to come to the eth0 interface address, we want them to come to the
ovs-br0 interface be processed, and set to the correct system. To fix this, we need to remove the address from `eth0`
and assign an address to our switch interface:

    sudo ifconfig eth0 0
    sudo dhclient ovsbr0

And communications are *"mysteriously"* restored. :) The commands above don't make the changes permanent - if we look at
`/etc/network/intefaces` we'll see the default configuration is still present ... and if we reboot, our network
communications will come back up disabled.

To make them permament, we need to modify our configuration in `/etc/network/interfaces`:

    # enable eth0 interface, but don't assign it an address or enable dhcp
    auto eth0
    iface eth0 inet manual

    # enable ovsbr0 interface and have it get an address using dhcp
    auto ovsbr0 
    iface ovsbr0 inet dhcp

And now we can reboot safely and have everything come back up correctly.

    $ sudo apt-get install ifmetric
    $ sudo ifmetric ovsbr0 0

    ifmetric 
    iface eth0 inet dhcp
        up ifmetric ovsbr0 0


Notes:

- We haven't set a priority for the `ovsbr0` interface. This *may* matter in more advanced configurations.
- We haven't added the openvswitch kernel modules to `/etc/modules`, so it's not loaded during bootup. With more
    advanced configurations this does matter.

### Vlan Trunking (802.1q)
I played around with Open vSwitch in a VM for awhile, but then transitioned over to using it on a spare laptop when
I wanted to start setting up vlans & KVM. I performed the rest of the configuration on a laptop, rather than a VM.

There are a couple common vlan setup scenarios - for mine, I'm bridging the the host's vlan directly to the vlan's on
the physical network. My home vlan setup is very simple:

| Vlan Name     | VlanID    | Network           |
| ------------- | --------- | ----------------- |
| Management    | 16        | 172.16.16.0/24    |
| Home          | 17        | 172.16.17.0/24    |
| Work          | 18        | 172.16.18.0/24    |
| Lab           | 19        | 172.16.19.0/24    |
| Guest         | 20        | 172.16.20.0/24    |

Administration interfaces (firewall admin ui, nas admin ui, ESXi server admin interface, etc) sit on vlan 16. Where
everything else goes should be fairly obvious from the names. :) My intent with the new server is to extend the vlans
onto the host, allowing multiple servers to reside on the same VM and be able to talk to only their environment (except
where policy permits).

For this setup, I configured a switchport on my D-Link xStack DGS-3200-10 to *not* be members of all vlan 16, 17, 18,
and 19 (20 not necessary), and *not* to have an untagged (native) vlan.

In the previous example I configured a layer3 interface directly on the virtual switch - which the easiest way to
restore connectivity, but not very flexible.

    $ sudo ovs-ofctl dump-flows ovsbr0
    NXST_FLOW reply (xid=0x4):
    cookie=0x0, duration=12115.181s, table=0, n_packets=13317, n_bytes=8386825, idle_age=0, priority=0 actions=NORMAL

    $ sudo ovs-appctl fdb/show ovsbr0
    port  VLAN  MAC                Age
    LOCAL     0  b6:94:f3:38:bf:49   37
    LOCAL     0  00:0c:29:6a:26:3f    7
        1     0  00:3e:e1:c4:a3:16    2
        1     0  00:18:0a:46:33:5c    0
        1     0  e0:ef:25:00:08:ff    0

    $ sudo ovs-ofctl show ovsbr0
    OFPT_FEATURES_REPLY (xid=0x2): dpid:0000000c296a263f
    n_tables:254, n_buffers:256
    capabilities: FLOW_STATS TABLE_STATS PORT_STATS QUEUE_STATS ARP_MATCH_IP
    actions: OUTPUT SET_VLAN_VID SET_VLAN_PCP STRIP_VLAN SET_DL_SRC SET_DL_DST SET_NW_SRC SET_NW_DST SET_NW_TOS SET_TP_SRC SET_TP_DST ENQUEUE
    1(eth0): addr:00:0c:29:6a:26:3f
        config:     0
        state:      0
        current:    1GB-FD COPPER AUTO_NEG
        advertised: 10MB-HD 10MB-FD 100MB-HD 100MB-FD 1GB-FD COPPER AUTO_NEG
        supported:  10MB-HD 10MB-FD 100MB-HD 100MB-FD 1GB-FD COPPER AUTO_NEG
        speed: 1000 Mbps now, 1000 Mbps max
    LOCAL(ovsbr0): addr:00:0c:29:6a:26:3f
        config:     0
        state:      0
        speed: 0 Mbps now, 0 Mbps max
    OFPT_GET_CONFIG_REPLY (xid=0x4): frags=normal miss_send_len=0


To properly setup our management interface, we'll create a new interface & assign it to our management vlan:

    sudo ovs-vsctl add-port ovsbr0 mgmt tag=16 -- set interface mgmt type=internal
    sudo dhclient mgmt

    sudo ovs-vsctl del-port ovsbr0 



    sudo ovs-vsctl add-port ovsbr0 vlan17 tag=17 -- set interface vlan17 type=internal
    sudo ovs-vsctl add-port ovsbr0 vlan18 tag=18 -- set interface vlan18 type=internal
    sudo ovs-vsctl add-port ovsbr0 vlan19 tag=19 -- set interface vlan19 type=internal


- http://openvswitch.org/support/config-cookbooks/vlan-configuration-cookbook/
- http://blog.scottlowe.org/2012/10/19/vlans-with-open-vswitch-fake-bridges/
- http://website-humblec.rhcloud.com/configure-openvswitch-in-virt-environment/
 

### KVM with Open vSwitch
The basic walk through got things setup, but without a some virtualization it's not very helpful.

    # apt-get install kvm libvirt-bin virtinst virt-manager openvswitch-controller openvswitch-brcompat
    openvswitch-switch openvswitch-datapath-sourcei

## Notes


- uml-utilities?
    
sudo apt-get install vlan
sudo apt-get install openvswitch-switch openvswitch-common bridge-utils


- openvswitch database?
- bond defined in port
- interface contains interface definitions

- make kernel module as simple as possible
- packet processing decisions are made in userspace
- first packet of new gloes to to ovs-switchd
    - if it doesn't have an entry, packet sent to vs-vswitchd to make switching decision
    - if it already has a table entry, it's forwarded

- classifier has and processes openflow tables
- pushes 'fast-cache' entry back down into the kernel

- megaflows - support for wildcarding

- interfaces don't show up in if

- default installation has only 1 flow in flowtable
    - for any packet that arrives on any interface, do 'normal processing' (l2 learning)

### Bookmarks

- [An Introduction to Open vSwitch](http://horms.net/projects/openvswitch/2012-01/openvswitch.en.pdf)
- [Introduction to Open vSwitch](https://www.youtube.com/watch?v=rYW7kQRyUvA)
- [Developer Documentation](http://goo.gl/TqtRw3)
- [Open vSwitch FAQ](http://goo.gl/gbgjhi)
- [Open vSwitch Deep Dive The Virtual Switch for OpenStack](https://www.youtube.com/watch?v=x-F9bDRxjAM)

- http://www.jackwparks.com/2014/06/home-lab-openvswitch-vlans/
- http://blog.scottlowe.org/2012/10/04/some-insight-into-open-vswitch-configuration/
- http://blog.scottlowe.org/2012/10/19/vlans-with-open-vswitch-fake-bridges/
- http://www.jackwparks.com/2014/06/home-lab-openvswitch-vlans/
- http://www.microhowto.info/howto/configure_an_ethernet_interface_as_a_vlan_trunk.html
- http://ngineered.co.uk/howto-install-kvm-and-openvswitch-in-ubuntu-14-04/
- http://www.itsprite.com/kvmhow-install-configure-kvm-open-vswitch-ubuntu-debian/
- http://lost-and-found-narihiro.blogspot.com/2014/07/ubuntu-1404-install-open-vswitch-with.html
- https://stackoverflow.com/questions/18895700/openvswitch-one-nic-brdiges-and-vlans
- http://cloudbuilder.co.za/2013/08/20/openvswitch-and-kvm-with-libvirt/

- [VXLAN overlay networks with Open vSwitch](https://www.youtube.com/watch?v=tnSkHhsLqpM)
- [Introduction to Cloud Overlay Networks - VXLAN](https://www.youtube.com/watch?v=Jqm_4TMmQz8)
 
- [VLANs with Open vSwitch Fake Bridges](http://blog.scottlowe.org/2012/10/19/vlans-with-open-vswitch-fake-bridges/)
- [Running Host Management on Open vSwitch](http://blog.scottlowe.org/2012/10/30/running-host-management-on-open-vswitch/)
- [VLAN Trunking to Guest Domains with Open vSwitch](http://blog.scottlowe.org/2013/05/28/vlan-trunking-to-guest-domains-with-open-vswitch/)
- [Transparent VLAN Tagging with libvirt and Open vSwitch](https://www.netflask.net/transparent-vlan-tagging-libvirt-ovs/)

- https://fvtool.wordpress.com/2013/04/29/install-kvm-on-centos-6-4-configuring-openswitch-with-kvm-and-libvirtd/
- http://www.jedelman.com/home/open-vswitch-201-301
- http://blog.aaronorosen.com/open-vswitch-and-libvirt/
- http://keepingitclassless.net/2013/10/introduction-to-open-vswitch/
- http://linuxdrops.com/install-and-configure-open-vswitch-on-centos-rhel-fedora/
