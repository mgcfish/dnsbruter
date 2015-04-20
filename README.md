DNS Bruter
=========

DNS Bruter is an open source multi-threaded penetration testing tool that automates the process of detecting subdomains of a domain.<br>

It is based on the [dnsbruter](https://github.com/marpie/dnsbruter) of [Markus Pieton](https://github.com/marpie).

Features
----

* ZoneTransfers for nameservers
* Bruteforcing from wordlist
* Wildcard domains are supported!

Installation
----

You can download the latest tarball by clicking [here](https://github.com/whoot/dnsbruter/tarball/master) or latest zipball by clicking  [here](https://github.com/whoot/dnsbruter/zipball/master).

Preferably, you can download dnsbruter by cloning the [Git](https://github.com/whoot/dnsbruter) repository:

    git clone https://github.com/whoot/dnsbruter.git

DNSBruter works with [Python](http://www.python.org/download/) version **3.x** on Debian/Ubuntu and RedHat (and Windows) platforms.

WARNING: I really, really don´t recommend to use it Windows, because Windows has some fucked up timeout ratings!
	 Use it on Linux, comment out the "search xxx" in /etc/resolv.conf and be happy :) 

On every platform you need following packages:

* [dnspython](http://www.dnspython.org/)
* [Colorama](https://pypi.python.org/pypi/colorama)

On Redhat you can also need argparse. You can install it with easy_install:

	easy_install argparse

Usage
----

To get a list of all options use:

    python dnsbruter.py -h

You can use DNSBruter with domains:

	python dnsbruter.py -d DOMAIN [DOMAIN ...]

Or with a file with a list of domains:

	python dnsbruter.py -f FILE

Example:<br>
Find all subdomains of example.com (with default subdomainlist):

	python dnsbruter.py -d example.com

Bug Reporting
----
Bug reports are welcome! Please report all bugs on the [issue tracker](https://github.com/whoot/Typo-Enumerator/issues).

Links
----

* Download: [.tar.gz](https://github.com/whoot/dnsbruter/tarball/master) or [.zip](https://github.com/whoot/dnsbruter/archive/master)
* Changelog: [Here](https://github.com/whoot/dnsbruter/blob/master/doc/ChangeLog.md)
* TODO: [Here](https://github.com/whoot/dnsbruter/blob/master/doc/TODO.md)
* Issue tracker: https://github.com/whoot/dnsbruter/issues
