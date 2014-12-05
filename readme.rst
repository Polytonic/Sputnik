`Sputnik`_
==========

|Build Status| |Coverage Status| |Dependency Status|

Summary
-------

Sputnik is a Python IRC bouncer written using `asyncio`_ and backed by `Redis`_. It is intended as a lightweight, zero-configuration bouncer capable of deployment on cloud providers such as `Heroku`_. Sputnik is written in pure Python, so adding custom functionality is relatively straightforward.

**Features**

- Automatic Network Reconnection
- Channel Saver
- Buffered Message History
- Multi-Client Connections

Getting Started
---------------

You can easily deploy a Sputnik instance on Heroku using the button below.

|Deploy|

Alternately, you can manually create and deploy your own Heroku app, or run Sputnik on your own computer or server. To do so requires a Python 3.4 interpreter and Redis (optional), if you want persistence between restarts or crashes.

Documentation
-------------

Sputnik documentation is built using `Sphinx`_ and publicly hosted at http://sputnik.readthedocs.org/. You can also build and serve the documentation locally.

.. code:: sh

    git submodule update --init --recursive
    cd docs && make dirhtml && cd _build/dirhtml
    python -m SimpleHTTPServer

Then visit http://localhost:8000 in a browser.

License
-------

    The MIT License (MIT)

    Copyright (c) 2014 Kevin Fung et al.

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. _Sputnik: https://github.com/Polytonic/Sputnik
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _Redis: https://github.com/antirez/redis
.. _Heroku: http://heroku.com
.. _Sphinx: http://sphinx-doc.org/faq.html

.. |Build Status| image:: http://img.shields.io/travis/Polytonic/Sputnik.svg?style=flat-square
   :target: https://travis-ci.org/Polytonic/Sputnik
.. |Coverage Status| image:: http://img.shields.io/coveralls/Polytonic/Sputnik.svg?style=flat-square
   :target: https://coveralls.io/r/Polytonic/Sputnik
.. |Dependency Status| image:: http://img.shields.io/gemnasium/Polytonic/Sputnik.svg?style=flat-square
   :target: https://gemnasium.com/Polytonic/Sputnik
.. |Deploy| image:: https://www.herokucdn.com/deploy/button.png
   :target: https://heroku.com/deploy?template=https://github.com/Polytonic/Sputnik/
