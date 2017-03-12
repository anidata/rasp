Contributing to Rasp
====================

Be Nice and Have Fun
--------------------

Software is written by people, be nice to those people, and help each
other out along the way.

How to Contribute
-----------------

The preferred workflow to contribute to rasp is:

 * Fork this repository into your own github account.
 * Clone the fork on your account onto your local disk:

    $ git clone git@github.com:YourLogin/rasp.git 
    $ cd rasp

 * Create a branch for your new awesome feature, do not work in the master branch:

    $ git checkout -b new-awesome-feature

 * Write some code, or docs, or tests.
 * When you are done, submit a pull request.

Guidelines
----------

Rasp is a project maintained by Anidata, and has some guiding 
principles:

 * We are targeting modern pythons, in particularly 3.4+, but want to maintain
 support for 2.7 where possible.
 * Engines should be interchangeable and 'just work', so robust testing 
 and documentation are important.
 * The core object of interest is the Webpage, which should be intuitive,
 rich, and performant.

Testing
-------

Test coverage is admittedly pretty bad right now, so help out by writing
 tests for new code. To run the tests, make sure that you've installed
  the dev requirements, and use the command found in the bin directory
  of your virtualenv:

    $ nose2

We are working on getting travis or a similar CI service running.

Documentation
-------------

We use sphinx to build docs, they are in the docs directory.  To add new
documentation, look in docs/source, at the *.rst files. To build the docs:

    >>>cd docs
    >>>make clean
    >>>make html
    
Will build new html in the docs/build directory.

Easy Issues / Getting Started
-----------------------------

There are a number of issues on the near term horizon that would be 
great to have help with. The first place to go is the issues tab above
and make a comment on an issue that is interesting, or open up an issue
stating you'd like to contribute and we can work on that together.