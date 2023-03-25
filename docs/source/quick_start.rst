Quickstart
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

In this section, I will guide you through the basics of ``sis_meta``.

Installation
------------

You can get the latest release of this package using the ``pip`` installer::

    pip install -U sis-meta

After that, you can import the package as in the following line.

.. code-block:: python

    import sis_meta

Reading a meta file
-------------------

The first step is to load a meta file as an object. Use the ``Meta()`` class
to do this. In the following example, the path of the meta file is passed as 
an argument.

.. code-block:: python
    
    import sis_meta

    path = '/home/Documents/data/sound1.wav.meta'
    meta = sis_meta.Meta(path)

Navigating through marks
------------------------

You can walk through all the marks in a ``Meta`` object. Once you load
a meta file, use the loop ``for`` to visit each mark.

.. code-block:: python

    import sis_meta

    path = 'home/Documents/data/sound1.wav.meta'
    meta = sis_meta.Meta(path)

    for mark in meta:
        print(mark)

In the previous example, you will get the following result.

.. code-block:: python

    >>> {'position': 12.992729166666669, 'length': 36.41172247942387, 'text': '', 'group_id': 6, 'group_name': 'M1'}
    >>> {'position': 51.48970447530865, 'length': 5.854748328189302, 'text': '', 'group_id': 6, 'group_name': 'M1'}
    >>> {'position': 70.49758603395063, 'length': 2.325858924897119, 'text': '', 'group_id': 6, 'group_name': 'M1'}

Here, each printed ``dict`` contains the attributes of  a mark.
``position`` is the starting point in seconds; the ``length`` is also given in
seconds and it can be 0 if the mark is a point or greater if it is an interval;
``text`` is the content of the mark`. ``group_id`` and ``group_name`` show the
group a mark belongs to.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
