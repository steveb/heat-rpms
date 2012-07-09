Name: heat
Summary: This software provides AWS CloudFormation functionality for OpenStack Essex
Version: 5
Release: 1
License: ASL 2.0
Prefix: %{_prefix}
Group: System Environment/Base
URL: http://www.heat-api.org
Source0: http://heat-api.org/downloads/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1: heat.logrotate

BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-setuptools

Requires: python-crypto
Requires: python-eventlet
Requires: python-glance
Requires: python-greenlet
Requires: python-httplib2
Requires: python-iso8601
Requires: python-keystoneclient
Requires: python-kombu
Requires: python-lxml
Requires: python-memcached
Requires: python-migrate
Requires: python-novaclient
Requires: python-paste
Requires: python-qpid
Requires: python-routes
Requires: pysendfile
Requires: python-sqlalchemy
Requires: python-webob

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
sed -i -e '/^#!/,1 d' $RPM_BUILD_ROOT/%{python_sitelib}/heat/db/sqlalchemy/manage.py
sed -i -e '/^#!/,1 d' $RPM_BUILD_ROOT/%{python_sitelib}/heat/db/sqlalchemy/migrate_repo/manage.py
sed -i -e '/^#!/,1 d' $RPM_BUILD_ROOT/%{python_sitelib}/heat/testing/runner.py
mkdir -p $RPM_BUILD_ROOT/var/log/heat/
install -p -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/heat
mkdir -p $RPM_BUILD_ROOT/var/lib/heat/
mkdir -p $RPM_BUILD_ROOT/etc/heat/
cp -r etc/* $RPM_BUILD_ROOT/etc/heat/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
cp -v docs/man/man1/* $RPM_BUILD_ROOT/%{_mandir}/man1/
rm -rf $RPM_BUILD_ROOT/var/lib/heat/.dummy

%description
Heat provides AWS CloudFormation functionality for OpenStack.

%files
%defattr(-, root, root, -)
%doc README.rst
%{_mandir}/man1/*.gz
%{_bindir}/*
%{python_sitelib}/heat*
%dir %{_localstatedir}/log/heat
%dir %{_localstatedir}/lib/heat
%config(noreplace) %dir %{_sysconfdir}/heat/bash_completion.d/heat
%config(noreplace) %{_sysconfdir}/heat/heat-api-paste.ini
%config(noreplace) %{_sysconfdir}/heat/heat-api.conf
%config(noreplace) %{_sysconfdir}/heat/heat-engine-paste.ini
%config(noreplace) %{_sysconfdir}/heat/heat-engine.conf
%config(noreplace) %{_sysconfdir}/heat/heat-metadata-paste.ini
%config(noreplace) %{_sysconfdir}/heat/heat-metadata.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/heat

%changelog
* Mon Jul 9 2012 Jeff Peeler <jpeeler@redhat.com> - 5-1
- add necessary requires
- removed shebang line for scripts not requiring executable permissions
- add logrotate, removes all rpmlint warnings except for python-httplib2
- remove buildroot tag since everything since F10 has a default buildroot
- remove clean section as it is not required as of F13

* Fri Jun 8 2012 Steven Dake <sdake@redhat.com> - 4-1
- removed jeos from packaging since that comes from another repository
- compressed all separate packages into one package
- removed setup options which were producing incorrect results
- replaced python with {__python}
- added a br on python-devel
- added a --skip-build to the install step
- added percent-dir for directories
- fixed most rpmlint warnings/errors

* Mon Apr 16 2012 Chris Alfonso <calfonso@redhat.com> - 3-1
- initial openstack package log
