Name: heat
Summary: This software provides AWS CloudFormation functionality for OpenStack Essex
Version: 4
Release: 1
License: ASL 2.0
Prefix: %{_prefix}
Group: System Environment/Base
URL: http://www.heat-api.org
Source0: http://heat-api.org/downloads/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: python-glance
BuildRequires: python-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/log/heat/
mkdir -p $RPM_BUILD_ROOT/var/lib/heat/
mkdir -p $RPM_BUILD_ROOT/etc/heat/
cp -r etc/* $RPM_BUILD_ROOT/etc/heat/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/ 
cp -v docs/man/man1/* $RPM_BUILD_ROOT/%{_mandir}/man1/
rm -rf $RPM_BUILD_ROOT/var/lib/heat/.dummy

%clean
rm -rf $RPM_BUILD_ROOT

%description
Heat provides AWS CloudFormation functionality for OpenStack.

%files
%doc README.rst
%defattr(-,root,root,-)
%{_mandir}/man1/*.gz
%{_bindir}/heat
%{_bindir}/heat-api
%{_bindir}/heat-engine
%{_bindir}/heat-metadata
%{_bindir}/heat-db-setup
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

%changelog
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
