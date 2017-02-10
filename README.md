# junos_pyez
Junos PyEZ is a Python library that enables you to remotely manage and automate devices running Junos OS.

Installing Junos PyEZ:
https://www.juniper.net/techpubs/en_US/junos-pyez1.0/topics/task/installation/junos-pyez-server-installing.html

Junos PyEZ Documentation:
https://junos-pyez.readthedocs.io/en/2.0.1/

### Junos XML API
CLI (Command Line Interface) output, which is the typical type of human-interface for network hardware, is a good way for humans to interact. However it is not a good interface for interacting with programs for automation as the data output is not in a structured format and data cannot be easily parsed for retrieval. For example consider retrieving the serial number of a Junos device - how would it be done?

seanw@vsrx1> show chassis hardware 
Hardware inventory:
Item             Version  Part number  Serial number     Description
Chassis                                BABF6658EFA5      VSRX
Midplane         REV 08   750-058562   564D00F7          VSRX
CB 0            
Routing Engine 0          BUILTIN      BUILTIN           SRX Routing Engine
FPC 0            REV 07   611-049549   RL3714040884      FPC
  PIC 0                   BUILTIN      BUILTIN           VSRX DPDK GE

Junos software operates over an XML (Extensible Markup Language) API (Application Program Interface). Junos recieves request in XML format and produces responses in XML format. Request are recieved via RPC (Remote Procedure Calls) and are enclosed in <rpc> tags:

seanw@vsrx1> show chassis hardware | display xml rpc 
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <rpc>
        <get-chassis-inventory>
        </get-chassis-inventory>
    </rpc>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>

The Junos device places its responses in <rpc-reply> tags:

seanw@vsrx1> show chassis hardware | display xml 
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
    <chassis-inventory xmlns="http://xml.juniper.net/junos/15.1X49/junos-chassis">
        <chassis junos:style="inventory">
            <name>Chassis</name>
            <serial-number>BABF6658EFA5</serial-number>
            <description>VSRX</description>
            <chassis-module>
                <name>Midplane</name>
                <version>REV 08</version>
                <part-number>750-058562</part-number>
                <serial-number>564D00F7</serial-number>
                <description>VSRX</description>
            </chassis-module>
            <chassis-module>
                <name>CB 0</name>
            </chassis-module>
            <chassis-module>
                <name>Routing Engine 0</name>
                <part-number>BUILTIN</part-number>
                <serial-number>BUILTIN</serial-number>
                <description>SRX Routing Engine</description>
            </chassis-module>
            <chassis-module>
                <name>FPC 0</name>
                <version>REV 07</version>
                <part-number>611-049549</part-number>
                <serial-number>RL3714040884</serial-number>
                <description>FPC</description>
                <chassis-sub-module>
                    <name>PIC 0</name>
                    <description>VSRX DPDK GE</description>
                    <version></version>
                    <part-number>BUILTIN</part-number>
                    <serial-number>BUILTIN</serial-number>
                </chassis-sub-module>
            </chassis-module>
        </chassis>
    </chassis-inventory>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
