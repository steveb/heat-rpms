Name: heat
Summary: This software provides cloud orchestration functionality for OpenStack Grizzly
Version: 2013.1
Release: 2%{?dist}
License: ASL 2.0
Group: System Environment/Base
URL: http://heat-api.org
Source0: https://github.com/downloads/heat-api/heat/heat-%{version}.tar.gz
Source1: heat.logrotate
Source2: heat-api.service
Source3: heat-api-cfn.service
Source4: heat-engine.service
Source5: heat-api-cloudwatch.service

# fedora specific patches commented out
#Patch0: switch-to-using-m2crypto.patch

BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-sphinx

Requires: heat-common = %{version}-%{release}
Requires: heat-engine = %{version}-%{release}
Requires: heat-api = %{version}-%{release}
Requires: heat-cfn-api = %{version}-%{release}
Requires: heat-cloudwatch-api = %{version}-%{release}
Requires: heat-clients = %{version}-%{release}

%prep
%setup -q
#%%patch0 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}
sed -i -e '/^#!/,1 d' %{buildroot}/%{python_sitelib}/heat/db/sqlalchemy/manage.py
sed -i -e '/^#!/,1 d' %{buildroot}/%{python_sitelib}/heat/db/sqlalchemy/migrate_repo/manage.py
sed -i -e '/^#!/,1 d' %{buildroot}/%{python_sitelib}/heat/testing/runner.py
mkdir -p %{buildroot}/var/log/heat/
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/heat

# install systemd unit files
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/heat-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/heat-api-cfn.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/heat-engine.service
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/heat-api-cloudwatch.service

mkdir -p %{buildroot}/var/lib/heat/
mkdir -p %{buildroot}/etc/heat/

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees source build/html
sphinx-build -b man -d build/doctrees source build/man

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd

rm -rf %{buildroot}/var/lib/heat/.dummy

install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/heat/heat-api.conf %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/heat/heat-api-paste.ini %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/heat/heat-api-cfn.conf %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/heat/heat-api-cfn-paste.ini %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/heat/heat-api-cloudwatch.conf %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/heat/heat-api-cloudwatch-paste.ini %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/heat/heat-engine.conf %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/boto.cfg %{buildroot}/%{_sysconfdir}/heat
install -p -D -m 644 %{_builddir}/%{name}-%{version}/etc/bash_completion.d/heat-cfn %{buildroot}/%{_sysconfdir}/bash_completion.d/heat-cfn

%description
Heat provides AWS CloudFormation and CloudWatch functionality for OpenStack.


%package common
Summary: Heat common
Group: System Environment/Base

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
#Requires: m2crypto

Requires(pre): shadow-utils

%description common
Components common to all OpenStack Heat services

%files common
%doc LICENSE
%{_bindir}/heat-db-setup
%{_bindir}/heat-keystone-setup
%{python_sitelib}/heat*
%dir %attr(0755,openstack-heat,root) %{_localstatedir}/log/heat
%dir %attr(0755,openstack-heat,root) %{_localstatedir}/lib/heat
%dir %{_sysconfdir}/heat
%config(noreplace) %{_sysconfdir}/logrotate.d/heat

%pre common
getent group openstack-heat >/dev/null || groupadd -r openstack-heat
getent passwd openstack-heat  >/dev/null || \
useradd -r -g openstack-heat -d %{_localstatedir}/lib/heat -s /sbin/nologin \
    -c "OpenStack Heat Daemon" openstack-heat
exit 0


%package engine
Summary: The Heat engine
Group: System Environment/Base

Requires: heat-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description engine
OpenStack API for starting CloudFormation templates on OpenStack

%files engine
%doc README.rst LICENSE doc/build/html/man/heat-engine.html
%{_bindir}/heat-engine
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/heat-engine.conf
%{_unitdir}/heat-engine.service
%{_mandir}/man1/heat-engine.1.gz

%post engine
%systemd_post heat-engine.service

%preun engine
%systemd_preun heat-engine.service

%postun engine
%systemd_postun_with_restart heat-engine-cfn.service


%package api
Summary: The Heat API
Group: System Environment/Base

Requires: heat-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description api
OpenStack-native ReST API to the Heat Engine

%files api
%doc README.rst LICENSE doc/build/man/heat-api.1
%{_bindir}/heat-api
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/heat-api.conf
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/heat-api-paste.ini
%{_unitdir}/heat-api.service
%{_mandir}/man1/heat-api.1.gz

%post api
%systemd_post heat-api.service

%preun
%systemd_preun heat-api.service

%postun
%systemd_postun_with_restart heat-api.service


%package cfn-api
Summary: Heat CloudFormation API
Group: System Environment/Base

Requires: heat-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description cfn-api
AWS CloudFormation-compatible API to the Heat Engine

%files cfn-api
%doc README.rst LICENSE doc/build/html/man/heat-api-cfn.html
%{_bindir}/heat-api-cfn
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/heat-api-cfn.conf
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/heat-api-cfn-paste.ini
%{_unitdir}/heat-api-cfn.service
%{_mandir}/man1/heat-api-cfn.1.gz

%post cfn-api
%systemd_post heat-api-cloudwatch.service

%preun cfn-api
%systemd_preun heat-api-cloudwatch.service

%postun cfn-api
%systemd_postun_with_restart heat-api-cloudwatch.service


%package cloudwatch-api
Summary: Heat CloudWatch API
Group: System Environment/Base

Requires: heat-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description cloudwatch-api
AWS CloudWatch-compatible API to the Heat Engine

%files cloudwatch-api
%doc README.rst LICENSE doc/build/html/man/heat-api-cloudwatch.html
%{_bindir}/heat-api-cloudwatch
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/heat-api-cloudwatch.conf
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/heat-api-cloudwatch-paste.ini
%{_unitdir}/heat-api-cloudwatch.service
%{_mandir}/man1/heat-api-cloudwatch.1.gz

%post cloudwatch-api
%systemd_post heat-api-cfn.service

%preun cloudwatch-api
%systemd_preun heat-api-cfn.service

%postun cloudwatch-api
%systemd_postun_with_restart heat-api-cfn.service


%package clients
Summary: Heat clients
Group: System Environment/Base

Requires: heat-common = %{version}-%{release}

%description clients
Heat client tools accessible from the CLI

%files clients
%doc README.rst LICENSE doc/build/html/man/heat-cfn.html
%{_bindir}/heat-boto
%{_bindir}/heat-cfn
%{_bindir}/heat-watch
%config(noreplace) %{_sysconfdir}/bash_completion.d/heat-cfn
%config(noreplace) %attr(-,root,openstack-heat) %{_sysconfdir}/heat/boto.cfg
%{_mandir}/man1/heat-cfn.1.gz
#%{_mandir}/man1/heat-boto.1.gz

%changelog
* Thu Dec 20 2012 Jeff Peeler <jpeeler@redhat.com> 2013.1-2
- split into subpackages

* Fri Dec 14 2012 Steve Baker <sbaker@redhat.com> 2013.1-1
- rebase to 2013.1
- expunge heat-metadata
- generate man pages and html developer docs with sphinx

* Tue Oct 23 2012 Zane Bitter <zbitter@redhat.com> 7-1
- rebase to v7
- add heat-api daemon (OpenStack-native API)

* Fri Sep 21 2012 Jeff Peeler <jpeeler@redhat.com> 6-5
- update m2crypto patch (Fedora)
- fix user/group install permissions

* Tue Sep 18 2012 Steven Dake <sdake@redhat.com> 6-4
- update to new v6 binary names in heat

* Tue Aug 21 2012 Jeff Peeler <jpeeler@redhat.com> 6-3
- updated systemd scriptlets

* Tue Aug  7 2012 Jeff Peeler <jpeeler@redhat.com> 6-2
- change user/group ids to openstack-heat

* Wed Aug 1 2012 Jeff Peeler <jpeeler@redhat.com> 6-1
- create heat user and change file permissions
- set systemd scripts to run as heat user

* Fri Jul 27 2012 Ian Main <imain@redhat.com> - 5-1
- added m2crypto patch.
- bumped version for new release.
- added boto.cfg to sysconfigdir

* Tue Jul 24 2012 Jeff Peeler <jpeeler@redhat.com> - 4-5
- added LICENSE to docs
- added dist tag
- added heat directory to files section
- removed unnecessary defattr 

* Tue Jul 24 2012 Jeff Peeler <jpeeler@redhat.com> - 4-4
- remove pycrypto requires

* Fri Jul 20 2012 Jeff Peeler <jpeeler@redhat.com> - 4-3
- change python-devel to python2-devel

* Wed Jul 11 2012 Jeff Peeler <jpeeler@redhat.com> - 4-2
- add necessary requires
- removed shebang line for scripts not requiring executable permissions
- add logrotate, removes all rpmlint warnings except for python-httplib2
- remove buildroot tag since everything since F10 has a default buildroot
- remove clean section as it is not required as of F13
- add systemd unit files
- change source URL to download location which doesn't require a SHA

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
