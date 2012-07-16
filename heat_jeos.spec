Name:		heat_jeos
Version:	1
Release:	1
Summary:	This software provides the ability to create JEOS images for Heat

Group:		System Environment/Base
License:	ASL 2.0
URL:		http://heat-api.org
Source0:	https://github.com/downloads/heat-api/heat-jeos/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires:	python-devel
BuildRequires:	python-setuptools

Requires:	heat
Requires:	oz
Requires:	yum

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
%defattr(-, root, root, -)
%doc README.rst
%{_mandir}/man1/*.gz
%{_bindir}/heat-jeos
%{python_sitelib}/heat_jeos*



%changelog
* Wed Jul 11 2012 Jeff Peeler <jpeeler@redhat.com> 1-1
- initial package
