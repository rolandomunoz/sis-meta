Quickstart
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Hi!!! Welcome to this tutorial of ``sis_meta``. In the next sections
I will guide you through the basics of this package.

Installation
------------

Get the latest release of this package using the ``pip`` installer::

    pip install -U sis_meta

After that, you can import the package as in the following line.

.. code-block:: python

    import sis_meta

Reading a meta file
-------------------

You can use :func:`~sis_meta.read_from_file()` to load the content of a
`.meta` file. This will return a :class:`~sis_meta.Meta` object.

.. code-block:: python
    
    import sis_meta

    path = '/home/Documents/data/sound1.wav.meta'
    meta = sis_meta.read_from_file(path)

When a :class:`~meta_sis.Meta` object is obtained in this way, it contains
the `guide marks` and also the `groups` that were defined in the original
file.

Creating a Meta object
----------------------

You can also initialize a :class:`~sis_meta.Meta` object from scratch.

.. code-block:: python
    
    import sis_meta

    meta = sis_meta.Meta()

This object does not contain any `guide marks`. It only comes with a
set of default `groups`.

Navigating through marks
------------------------

You can iterate through the guide marks in a :class:`~sis_meta.Meta` object
using the ``for`` loop.

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


In this example, we read the content of a meta file as a :class:`~sis_meta.meta.Meta`
object. Then we used a ``for`` loop to visit each of its guide marks.
For each iteration, a :class:`~sis_meta.mark.GuideMark` object is returned.
Finally, the attributes of this object are printed.

.. code-block:: python

    position:  12.992729166666669
    length:  36.41172247942387
    text: "Hi"
    group_id:  6
    group_name:  "Speakers/M1"

    position:  51.48970447530865
    length:  5.854748328189302
    text:  "Where are you?"
    group_id:  7
    group_name:  "Speakers/M2"

    position:  70.49758603395063
    length:  2.325858924897119
    text: "Uhm..."
    group_id:  6
    group_name:  "Speakers/M1"

The attributes printed are ``position``, ``length``, ``text``, ``group_id``
and ``group_name``.

.. glossary::

    position
        The starting point of a guide mark in seconds.

    length
        The length of the guide mark in seconds. Marks can be
        intervals or points. When they are points, the length is always
        0.

    text
        The annotation associated with the guide mark.

    group_id
        The ID of the group the guide mark belong.

    group_name
        The name of the group the guide mark belongs.

Inserting guide marks 
---------------------

Once you have initialized a :class:`~sis_meta.Meta` object, you can insert
new guide marks. Use :meth:`sis_meta.Meta.insert_guide_mark` to do it.

.. code-block:: python

    import sis_meta

    # Initialize a Meta object
    meta = sis_meta.Meta()
    
    # Insert guide marks
    meta.insert_guide_mark('Speakers/M1', 10.424, 1.32, 'Hi')
    meta.insert_guide_mark('Speakers/M2', 11.93, 2.42, 'Where are you?')

Here, we inserted two guide marks. The first argument for both cases is
the group name; the second is the starting point of the mark; the third,
is the length of the guide mark; and the last argument is the text.
Note that the values in the starting point and lenght reprent the time
in seconds.
 
Every single guide mark belongs to a group. These are the groups that
come by default:

    - `Single` (id = 2)
    - `Sounds` (id = 3)
    - `Noises` (id = 4)
    - `Speakers/M1` (id = 6)
    - `Speakers/M2` (id = 7)
    - `Speakers/F1` (id = 8)
    - `Speakers/F2` (id = 9)
    - `VAD` (id = 10)
    - `For_AutoCmp` (id = 11)
    - `Edit_Tracker/ET_LM` (id = 13)

In the previous example, the group of the first mark is ``Speakers/M1``,
while ``Speakers/M2`` is the group of the second mark.

Manage groups
-------------

Use :meth:`~sis_meta.Meta.manage_groups` to handle the groups in your 
:class:`~sis_meta.Meta` instance. This returns a :class:`~sis_meta.groups.GroupsSegment`
object. You can use it to add, modify or delete any `group`.

.. code-block:: python

    meta = Meta()

    # Manage groups
    groups = meta.manage_groups()



Let's say we want to create a new group with the name of a my friend's cat
``Akuma``. We use :meth:`~sis_meta.groups.GroupsSegment.insert` to do it.

.. code-block:: python

    meta = Meta()

    # Manage groups
    groups = meta.manage_groups()
    groups.insert('Akuma')

Now, we can use ``Akuma`` as a group name for our new guide mark.

.. code-block:: python

    >>> meta.insert_guide_mark('Akuma', 10.424, 1.32, 'Meow')

We can also create nested groups. For this example, we create a parent
group called ``MyCats`` that contains two child groups: ``Akuma`` and
``Kirris``.

.. code-block:: python

    meta = Meta()

    # Manage groups
    groups = meta.manage_groups()

    groups.insert('MyCats') # Parent group
    groups.insert('Akuma', 'MyCats') # Child group
    groups.insert('Kirris', 'MyCats') # Child group

In the example, when creating the parent groups, we pass ``MyCats`` as
the first argument of :meth:`~sis_meta.groups.GroupsSegment.insert`.
To define a child group, we pass the name of the child group as the
first argument (``AKuma`` and ``Kirris``), but this time we provide a
second argument which is the name of the parent group (``MyCats``). 

To insert new marks, we provide ``MyCats/Akuma`` and ``MyCats/Kirris`` in
the first argument of :meth:`sis_meta.Meta.insert_guide_mark()`.

.. code-block:: python

    # Insert marks
    meta.insert_guide_mark('Praat/Akuma', 1.753, 2.242, 'Aló')
    meta.insert_guide_mark('Praat/Aaron', 3.2424, 2.853, 'hola')

Writing meta files
------------------
You can write new `meta` files using :meth:`sis_meta.Meta.write`.

.. code-block:: python

    import sis_meta

    meta = sis_meta.Meta()
    meta.insert_guide_mark('Speakers/M1', 10.424, 1.32, 'Hi')
    meta.insert_guide_mark('Speakers/M2', 11.93, 2.42, 'Where are you?')

    # Write a meta file
    meta.write()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
