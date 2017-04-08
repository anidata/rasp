Engines
=======

There are 4 types of engine supported by rasp, differing by how they are
accessing web pages. They all implement the same general functionality:

 * get_page_source(url): takes in a url, and returns a Webpage object,
 containing all we can find out about that webpage.  Notably it's source.

The 4 implemented engines are:

 * DefaultEngine: backed by python standard urllib
 * SeleniumEngine: backed by selenium and the firefox driver
 * TimedWaitEngine: also backed by selenium, but waits after issuing the
  request before storing the source
 * TorEngine: which is backed by Tor

.. autoclass:: rasp.engines.base.DefaultEngine
    :members:

.. autoclass:: rasp.engines.selenium_engine.SeleniumEngine
    :members:

.. autoclass:: rasp.engines.tor_engine.TorEngine
    :members:
