heat-rpms
=========

Repo for creating rpm packaging for the heat projects:

Step 1: Override Makefile variables

Create a file local.mk and set any variables which should override the make
variables at the beginning of the file Makefile

linux% touch local.mk  

Step 2: Create RPMs

linux% cd heat-rpms  
linux% make  
