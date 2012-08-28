heat-rpms
=========

Repo for creating rpm packaging for the heat projects:

Step 1: Create a heat tar.gz file

linux% git clone git://github.com/heat-api/heat.git  
linux% cd heat  
linux% ./setup.py sdist  

This will create a source distribution of heat in dist/heat-$VER.tar.gz

Step 2: Create a heat-jeos tar.gz file

linux% git clone git://github.com/heat-api/heat-jeos.git  
linux% cd heat-jeos  
linux% ./setup.py sdist  

This will create a source distribution of heat-jeos in dist/heat-jeos-$VER.tar.gz

Step 3: Copy source distribution files created above to heat-rpms directory after cloning

linux% git clone git://github.com/heat-api/heat-rpms.git  

Step 4: Create the RPM

linux% cd heat-rpms  
linux% make  
