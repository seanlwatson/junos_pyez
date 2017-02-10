import argparse
import logging
import os
import sys

from jnpr.junos import Device
from jnpr.junos.exception import *
from jnpr.junos.utils.sw import SW


# Define the logging methods used within the program and by the install() method.
def do_log(msg, level='info'):
    getattr(logging, level)(msg)


def update_progress(report):
    # Log the progress of the installing process
    do_log(report)


def main():
    parser = argparse.ArgumentParser(description='Upgrade Junos software on target device')
    parser.add_argument('-d', '--device', dest='device', help='Junos target device', required=True)
    parser.add_argument('-s', '--software', dest='software', help='Path to Junos software package', required=True)
    args = parser.parse_args()
    host = args.device
    package = args.software
    logfile = '/Users/seanw/PycharmProjects/junos_pyez/software_upgrade/log/install.log'

    # Remove log file if it already exist
    try:
        os.remove(logfile)
    except OSError:
        pass

    # Initialize logging
    logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s:%(name)s: %(message)s')
    logging.getLogger().name = host
    sys.stdout.write("Information logged in {0}\n".format(logfile))

    # Verify Junos software package exists
    if os.path.isfile(package):
        pass
    else:
        msg = "Software package does not exist: {0}.".format(package)
        sys.exit(msg + '\nExiting program')

    # Create an instance of the Device class, and supply the hostname and any parameters required
    dev = Device(host=host)

    # Open a NETCONF session with Junos device
    try:
        dev.open()
    except ConnectError as err:
        sys.stderr.write("Cannot connect to device: {0}\n".format(err))
        return

    # Increase the default RPC timeout to accommodate install operations
    dev.timeout = 300

    # Create an instance of SW utility
    sw = SW(dev)

    # Include code to install the software package and to reboot the device if the installation succeeds
    try:
        do_log("Starting the software upgrade process: {0}".format(package))
        ok = sw.install(package=package, remote_path='/var/tmp', progress=update_progress, validate=True)
    except Exception as err:
        msg = "Unable to install software, {0}".format(err)
        do_log(msg, level='error')
        ok = False

    if ok is True:
        do_log('Software installation complete. Rebooting')
        rsp = sw.reboot()
        do_log('Upgrade pending reboot cycle, please be patient.')
        do_log(rsp)
    else:
        msg = 'Unable to install software, {0}'.format(ok)
        logging.error(msg)

    # End the NETCONF session with Junos device
    dev.close()

if __name__ == "__main__":
    main()
