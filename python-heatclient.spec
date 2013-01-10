Name: python-heatclient
Version: %{?_version}
Release: %{?_release}%{?dist}
Summary: Python API and CLI for OpenStack Heat

Group: Development/Languages
License: ASL 2.0
URL: http://github.com/openstack/python-heatclient
Source0: http://pypi.python.org/packages/source/p/python-heatclient/python-heatclient-%{?_version}.tar.gz

BuildArch: noarch
BuildRequires: python-setuptools

Requires: python-httplib2
Requires: python-keystoneclient
Requires: python-prettytable
Requires: python-setuptools
Requires: python-warlock

%description
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements
100% of the OpenStack Heat API.

%prep
%setup -q

sed -e 's|^prettytable.*|prettytable|' -i tools/pip-requires

# Remove bundled egg-info
rm -rf python_heatclient.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}/usr/heatclient/versioninfo %{buildroot}%{python_sitelib}/heatclient/versioninfo

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

%files
%doc README.md
%doc LICENSE
%{_bindir}/heat
%{python_sitelib}/heatclient
%{python_sitelib}/*.egg-info

%changelog
* Wed Jan 04 2012 Steve Baker <sbaker@redhat.com> 0.1.0
- Initial release
