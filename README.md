rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses


###installation

Requirements:
* [vagrant](https://www.vagrantup.com/)
* [virtualbox](https://www.virtualbox.org/wiki/Downloads)

Install these two programs and using your terminal, navigate to the download 
folder and use the command:
 
    vagrant up
    vagrant ssh
    
This will download the necessary OS and software, as well as share all folders 
with the Guest OS and make certain network ports accessible. vagrant ssh will
connect your terminal to the Guest OS, and allow you to interact with the database.

Find the shared tournament folder in /vagrant/tournament and run the following
commands to setup the postgresql database and run the tests:
   
    $ cd /vagrant/tournament
    $ psql
    => \i tournament.sql
    => \q
    $ python tournament_test.py

