Crawlers
========

A bounded crawler takes in a collection of urls to crawl, as well as an engine to use, and then executes the crawling of each
 of the urls in that collection.  The user can pass in a callback which is used by the crawler to handle the Webpage
 objects returned by the engines (generally to persist the data somewhere).

Currently we have one crawler implemented, the DefaultBoundedCrawler, which is a simple single-threaded iterator. In the
examples directory, there is a usage example.

.. autoclass:: rasp.crawlers.base.DefaultBoundedCrawler
    :members:
