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

Once you have started a Meta object, you are ready to iterate through 
all of its marks. Use the `for` loop as in the next example. 

.. code-block:: python

    import sis_meta

    path = 'home/Documents/data/sound1.wav.meta'
    meta = sis_meta.Meta(path)

    for mark in meta:
        print(mark)

You will get something like this:

.. code-block:: python

    >>> (71.45500032620042, 8.862635699373698, '', 6, 'M1')
    >>> (81.63590345544776, 8.432847498362264, '', 6, 'M1')
    >>> (81.93615262049745, 3.8635357077476726, '', 7, 'M2')
    >>> (86.45225645464342, 3.0033196833159366, '', 7, 'M2')
    >>> (95.81131219694839, 0.9396610807995955, '', 8, 'F1')
    >>> (95.81848391909412, 0.8725424321710591, '', 7, 'M2')
    >>> (97.64269246667006, 0.9492494591750926, '', 7, 'M2')

Here, a mark is represented by a tuple. Each tuple has 5 elements. The value 
in the first element is the ``starting position`` of the mark; the second element
is the ``length`` mark. Both elements are given in seconds. The third element is
the ``text`` that is linked to the mark; the ``group_id`` and ``group_name`` are
given in the fourth and fith element respectively.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
