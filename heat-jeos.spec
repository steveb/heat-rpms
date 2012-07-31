Name:		heat-jeos
Version:	5
Release:	1%{?dist}
Summary:	This software provides the ability to create JEOS images for Heat

Group:		System Environment/Base
License:	ASL 2.0
URL:		http://heat-api.org
Source0:	https://github.com/downloads/heat-api/heat-jeos/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires:	python2-devel
BuildRequires:	python-setuptools

Requires:	oz
Requires:	python-glance
Requires:	python-lxml
Requires:	python-prettytable
Requires:	python-psutil


%description
This is a project for creating Just Enough Operating System images
for heat.

This project supports the following features:
- Creates TDL files for use with oz
- Creates compressed qcow2 files for use with libvirt/glance
- Registers image files with glance

%prep
%setup -q


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
cp -v docs/man/man1/* $RPM_BUILD_ROOT/%{_mandir}/man1


%files
%doc README.rst LICENSE
%{_mandir}/man1/*.gz
%{_bindir}/heat-jeos
%{python_sitelib}/heat_jeos*



%changelog
* Tue Jul 31 2012 Jeff Peeler <jpeeler@redhat.com> 5-1
- skip version numbers to match heat
- add dist tag

* Mon Jul 30 2012 Jeff Peeler <jpeeler@redhat.com> 1-5
- renamed package from heat_jeos to heat-jeos

* Fri Jul 27 2012 Jeff Peeler <jpeeler@redhat.com> 1-4
- removed unnecessary defattr
- added license file to docs
- removed yum requires

* Thu Jul 26 2012 Jeff Peeler <jpeeler@redhat.com> 1-3
- removed heat requires

* Fri Jul 20 2012 Jeff Peeler <jpeeler@redhat.com> 1-2
- change python-devel to python2-devel

* Wed Jul 11 2012 Jeff Peeler <jpeeler@redhat.com> 1-1
- initial package
