Quickstart
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

In this section, I will guide you through the basics of ``sis_meta``.

Installation
------------

Get the latest release of this package using the ``pip`` installer::

    pip install -U sis-meta

After that, you can import the package as in the following line.

.. code-block:: python

    import sis_meta

Reading a meta file
-------------------

You can read the content of an existing meta file. Use ``read_from_file()``
as in the following example.

.. code-block:: python
    
    import sis_meta

    path = '/home/Documents/data/sound1.wav.meta'
    meta = sis_meta.read_from_file(path)

In the example, ``read_from_file()`` is the function that takes the path
of the meta file as an argument. Then, the function returns a ``Meta``
object which assigned to ``meta``.

Navigating through marks
------------------------

A ``Meta`` is a type of object that contains guide marks. You can loop through
these marks using a ``for`` loop. Take a look to the following example:

.. code-block:: python

    import sis_meta

    path = 'home/Documents/data/sound1.wav.meta'
    meta = sis_meta.read_from_file(path)

    for guide_mark in meta:
        print('')
        print('position: ', guide_mark.position)
        print('length: ', guide_mark.length)
        print('text: ', guide_mark.text)
        print('group_id: ', guide_mark.group_id)
        print('group_name: ', guide_mark.group_name)

In this example, we created a ``Meta`` object and assigned to ``meta``.
Then we used a ``for`` loop to visit the guide marks it contains.
Note that a guide mark is also an object of type ``GuideMark``. For each guide
mark, we print the following  attributes: ``position``, ``length``, ``text``,
``group_id`` and ``group_name``.

The result is as in the following lines:

.. code-block:: python

    >>> position:  12.992729166666669
    >>> length:  36.41172247942387
    >>> text: "Hi"
    >>> group_id:  6
    >>> group_name:  M1

    >>> position:  51.48970447530865
    >>> length:  5.854748328189302
    >>> text:  "Where are you?"
    >>> group_id:  7
    >>> group_name:  M2

    >>> position:  70.49758603395063
    >>> length:  2.325858924897119
    >>> text: "Uhm..."
    >>> group_id:  6
    >>> group_name:  M1

Note that ``position`` and ``length`` are given in seconds. The first one is the
starting time of the mark, while ``length`` is the duration of the mark. In SIS
marks can be intervals or points. When they are points, the length is always ``0``.
``text`` contains the annotation associated with the mark. Finally, any mark
belongs to a group which is given in ``group_id`` and ``group_name``.

Writing meta files
------------------
Writing a meta file is a process that is still under development. However, this piece of
code can do the job!

.. code-block:: python

    >>> import sis_meta

    >>> meta_path = '/home/rolando/Documents/data/mysound.wav.meta'

    >>> # lists
    >>> positions = [1.64505565987125, 3.1312, 20.2901113197425, 31.3131, 40.3121434114]
    >>> lengths = [15.313, 10.322, 2.32322, 20.1221, 2]
    >>> ids = [6, 7, 8, 9, 8]
    >>> texts = ['Hola, me llamo Akuma', 'Yo me llamo Lala', 'miau', 'raul', 'abuela']

    >>> data = {
        'positions': positions,
        'lengths': lengths,
        'ids': ids,
        'texts': texts,
        }
    >>> meta = sis_meta.write_meta_file(data, meta_path)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
