FI Widgets App
==============

The FI Widgets App is a multi-platform application that provides math widgets for Financial Independence enthusiasts. The app itself is just a wrapper for the `FI Widgets website <https://fi-widgets.com/>`_ where the core functionality resides. To use FI Widgets, you need only go to the website. The app is not essential, however, it offers greater convenience and a streamlined user experience with a native feel. If you want to launch the application quickly and always have it ready to go with a click or a press, the app is nice.

FI Widgets are generated from the `FI Python module <https://github.com/bbusenius/FI>`_ and added to the website using `FI API <https://github.com/bbusenius/FI-API>`_. As new functions are added to the FI Python module, new widgets are automatically added to the FI Website and thus this app.

**Android**:

.. image:: https://github.com/bbusenius/FI-Widgets-App/raw/master/docs/fi-widgets-android.jpeg
    :height: 889
    :width: 400

**Ubuntu**:

.. image:: https://github.com/bbusenius/FI-Widgets-App/raw/master/docs/fi-widgets-ubuntu.png


Distributions
-------------

Currently the app can be installed on Android and Ubuntu/Debian Linux, however, builds for more systems are possible. If you want to run this app on a different system, you can likely generate a distribution from this repo. See `BeeWare <https://github.com/beeware/beeware>`_ for information on generating packages or try the `BeeWare tutorial <https://docs.beeware.org/en/latest/>`_ to see how it works.

Development
===========

Setup
-----

1. ``git clone`` this repo.
2. ``cd /to/cloned/directory``
3. `Install development dependencies <https://docs.beeware.org/en/latest/tutorial/tutorial-0.html#install-dependencies>`_
4. ``python3 -m venv venv``
5. ``source venv/bin/activate``
6. ``python -m pip install briefcase``

Briefcase commands
------------------

These are the commands you need to run in dev mode, update static resources, build, run a build, and package for release on your native system.

- ``briefcase dev``
- ``briefcase update --update-resources``
- ``briefcase build -ru``
- ``briefcase run``
- ``briefcase package``

Generate an Android release
---------------------------

- ``briefcase update android --update-resources``
- ``briefcase build android -ru``
- ``briefcase package android``

Run unit tests
--------------
BeeWare uses ``pytest``.

``briefcase dev --test``
