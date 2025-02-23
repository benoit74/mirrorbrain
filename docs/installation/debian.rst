
.. _installation_ubuntu_debian:

Installation on Debian/Ubuntu Linux
===================================

.. note:: 
   The following recipe for installing MirrorBrain was tested on Ubuntu 9.04 and 10.04.
   A similar procedure should work on other Ubuntu versions, and on Debian 5.0.


Install a standard Ubuntu LAMP server.


Add package repository
----------------------

To subscribe to the repository with packages for Ubuntu 10.04, add the following
to :file:`/etc/apt/sources.list`::

   sudo vim /etc/apt/sources.list
  [...]
  deb http://download.opensuse.org/repositories/Apache:/MirrorBrain/Ubuntu_10.04/ /


There are more repositories at
http://download.opensuse.org/repositories/Apache:/MirrorBrain/ for other Ubuntu
and Debian releases.

After adding the repository, update the local :program:`apt-get` package
cache::

  sudo apt-get update


That will produce a warning message saying that a GPG key isn't known for the
new package repository. Take note of the key ID and import the key with `apt-key`::

   # sudo apt-key adv --keyserver hkp://wwwkeys.de.pgp.net --recv-keys BD6D129A
  Executing: gpg --ignore-time-conflict --no-options --no-default-keyring \
    --secret-keyring /etc/apt/secring.gpg --trustdb-name /etc/apt/trustdb.gpg \
    --keyring /etc/apt/trusted.gpg --keyserver hkp://keys.gnupg.net --recv-keys \
    BD6D129A
  gpg: requesting key BD6D129A from hkp server hkp://wwwkeys.de.pgp.net
  gpg: key BD6D129A: public key "Apache OBS Project <Apache@build.opensuse.org>" imported
  gpg: no ultimately trusted keys found
  gpg: Total number processed: 1
  gpg:               imported: 1

If you now run :program:`apt-get` again, the warning should be gone::

  sudo apt-get update

.. note:: 
   The key's validity may need to be refreshed later. If apt-get stops working,
   see :ref:`refreshing_package_sign_keys`. 


Install the MirrorBrain packages
--------------------------------

The following commands will install all needed software via
:program:`apt-get`::

  sudo apt-get install mirrorbrain mirrorbrain-tools mirrorbrain-scanner \
  libapache2-mod-mirrorbrain libapache2-mod-autoindex-mb


Select and install an Apache MPM
--------------------------------

The MirrorBrain packages have dependencies on the Apache common packages, but
not on a MPM, since the choice of an MPM is one that the system admin must
make, and the MPMs cannot be installed in parallel. Thus, an MPM needs to be
installed (unless a LAMP package selection was installed initially). 

To install the worker MPM, run::

  sudo apt-get install apache2-mpm-worker

*If* the LAMP server has been installed, the prefork MPM was probably
preselected. It may make sense to switch to the worker MPM in such cases, which
is a good choice for busy download servers. If something like PHP is in use as
embedded interpreter (mod_php), though, then you need to stick to the prefork
MPM, because libraries that are used by PHP might not be threadsafe.


Loading Apache modules
~~~~~~~~~~~~~~~~~~~~~~

Don't forget to load the needed Apache modules::

  a2enmod form
  a2enmod mirrorbrain
  a2enmod geoip
  a2enmod dbd
  a2enmod autoindex_mb   # instead of Apache's own mod_autoindex
  a2enmod asn # only if you use that module as well


Configure mod_dbd
~~~~~~~~~~~~~~~~~

With Ubuntu 9.04, the DBD (Apache Portable Runtime DBD Framework) database
adapter for PostgreSQL is already installed, because the driver is statically
linked into the libaprutil1 shared object. libaprutil1-dbd-pgsql is a virtual
package which is just a pointer to the libaprutil1 package.

Running the following snippet will create a configuration for mod_dbd::

  sudo sh -c "cat > /etc/apache2/mods-available/dbd.conf << EOF
   <IfModule mod_dbd.c>
      DBDriver pgsql
      DBDParams 'host=localhost user=mirrorbrain password=12345 dbname=mirrorbrain connect_timeout=15'
   </IfModule>
  EOF
  "

.. note::
   Edit the password in the template here -- take note of it, you'll need it
   below, when you create a database user account.

.. note::
   Important: DBDParams strings must be unique; you cannot use the same string
   in another vhost. A possible workaround is to use differing connect_timeout
   values.


Install PostgreSQL
------------------

Install the PostgreSQL server (here, version 8.4 is the current version)::

  sudo apt-get install postgresql-8.4


Create the postgresql user account and database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Switch to user postgres::

  sudo su - postgres

Create user::

  createuser -P mirrorbrain
  Enter password for new role: 
  Enter it again: 
  Shall the new role be a superuser? (y/n) n
  Shall the new role be allowed to create databases? (y/n) n
  Shall the new role be allowed to create more new roles? (y/n) n

Create database::

  createdb -O mirrorbrain mirrorbrain
  createlang plpgsql mirrorbrain

Exit user postgres::

  exit


Edit host-based authentication 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add line ``host mirrorbrain mirrorbrain 127.0.0.1/32 md5`` to the end of
:file:`pg_hba.conf`, which is to be found here::

  sudo vim /etc/postgresql/8.4/main/pg_hba.conf

Start the PostgreSQL server::

  sudo /etc/init.d/postgresql-8.4 restart


Import initial mirrorbrain data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Import structure and data, running the commands as user mirrorbrain::

  sudo su - mirrorbrain
  gunzip -c /usr/share/doc/mirrorbrain/sql/schema-postgresql.sql.gz | psql -U mirrorbrain mirrorbrain
  gunzip -c /usr/share/doc/mirrorbrain/sql/initialdata-postgresql.sql.gz | psql -U mirrorbrain mirrorbrain
  exit


Next steps
----------

From here, follow on with :ref:`initial_configuration`.
