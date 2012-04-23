heat-rpms
=========

Repo for creating rpm packaging for the heat projects:

Step 1: get the src for the heat project

Step 2: built a tarball file in that directory and copy it to the root directory of this repo.
        tar -zcvf heat-%{version}.tar.gz --exclude=.git .
