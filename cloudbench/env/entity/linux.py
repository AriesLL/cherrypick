from .behavior import SecureShell, RsyncTransfer, SecureShell
from .behavior import LinuxInstaller, LinuxFileSystem, FileSystem

from cloudbench.package_manager import AptManager

class Linux(RsyncTransfer, SecureShell, LinuxInstaller, LinuxFileSystem):
    def __init__(self, *args, **kwargs):
        super(Linux, self).__init__(*args, **kwargs)

        self._memory = None;
        self._cpus = None;

    def intf_ip(self, intf='eth0'):
        extract = """grep -B1 "inet addr" |awk '{ if ( $1 == "inet" ) { print $2 }}' | awk -F: '{printf "%s", $2}'"""
        return self.script("ifconfig " + intf + " | " + extract)

    def memory(self):
        if not self._memory:
            self._memory = int(self.script("cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'"))
        return self._memory * 1024

    def cpus(self):
        if not self._cpus:
            self._cpus = int(self.script("nproc"))
        return self._cpus

class Ubuntu(Linux):
    def __init__(self, *args, **kwargs):
        super(Ubuntu, self).__init__(*args, **kwargs)

    @property
    def package_manager(self):
        if not hasattr(self, 'pkgmgr_'):
            self.pkgmgr_ = AptManager(self)

        return self.pkgmgr_