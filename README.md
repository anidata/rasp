Rasp
====

[![Build Status](https://travis-ci.org/anidata/rasp.svg?branch=master)](https://travis-ci.org/anidata/rasp)

Overview
--------

Rasp is a python library of 'engines' for getting rendered web data.
 
It is an open source project maintained by Anidata, a non-profit 
corporation consisting of established and aspiring data scientists who 
have come together with the purpose of applying data science to make a 
difference in the community.

Rasp is freely licensed under the BSD-3-Clause license.

Installation
------------

Currently this repo is still in development and is not on pypi or conda
yet, so install with:

    $ pip install git+https://github.com/anidata/rasp.git

Usage
-----

There are 4 types of engine supported by rasp, differing by how they are
accessing web pages. They all implement the same general functionality:
 
 * get_page_source(url): takes in a url, and returns a Webpage object, 
 containing all we can find out about that webpage.  Notably its source.
 
The 4 implemented engines are:

 * DefaultEngine: backed by [requests](http://docs.python-requests.org/en/master/)
 * SeleniumEngine: backed by selenium and the firefox driver
 * TorEngine: which is backed by Tor
 
Engines can be used directly, or passed to a crawler, along with a collection
of URLs and a callback to handle resultant Webpage objects. The crawler
will handle the execution.

Currently there is only one crawler implimented:

 * DefaultBoundedCrawler: a single-threaded python iteration.

Testing
-------
To run the tests install the dev dependencies listed in requirements-dev.txt
and run `pytest`
