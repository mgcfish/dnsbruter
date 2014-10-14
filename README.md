DNSBruter
=========

DNSBruter is an open source multi-threaded penetration testing tool that automates the process of detecting all subdomains of a domain.<br>

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

DNSBruter works with [Python](http://www.python.org/download/) version **2.6.x** and **2.7.x** on Debian/Ubuntu, RedHat and Windows platforms.

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
* Changelog: [Here](https://github.com/whoot/dnsbruter/blob/master/doc/CHANGELOG.md)
* TODO: [Here](https://github.com/whoot/dnsbruter/blob/master/doc/TODO.md)
* Issue tracker: https://github.com/whoot/dnsbruter/issues
