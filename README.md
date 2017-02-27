Rasp
====

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

TODO

Usage
-----

There are 4 types of engine supported by rasp, differing by how they are
accessing web pages. They all implement the same general functionality:
 
 * get_page_source(url): takes in a url, and returns a Webpage object, 
 containing all we can find out about that webpage.  Notably it's source.
 
The 4 implimented engines are:

 * DefaultEngine: backed by python standard urllib
 * SeleniumEngine: backed by selenium and the firefox driver
 * TimedWaitEngine: also backed by selenium, but waits after issuing the
  request before storing the source
 * TorEngine: which is backed by the Tor browser

