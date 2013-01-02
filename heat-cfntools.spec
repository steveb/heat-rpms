Name: heat-cfntools
Version: %{?_version}
Release: %{?_release}%{?dist}
Summary: Tools required to be installed on Heat provisioned cloud instances
Group: System Environment/Base
License: ASL 2.0
URL: http://heat-api.org
Source0: https://github.com/downloads/heat-api/heat-cfntools/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires: python-boto >= 2.4.0

%description
Tools required to be installed on Heat provisioned cloud instances

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

mkdir -p %{buildroot}/opt/aws/bin
mv %{buildroot}%{_bindir}/cfn-get-metadata %{buildroot}/opt/aws/bin
mv %{buildroot}%{_bindir}/cfn-hup %{buildroot}/opt/aws/bin
mv %{buildroot}%{_bindir}/cfn-init %{buildroot}/opt/aws/bin
mv %{buildroot}%{_bindir}/cfn-push-stats %{buildroot}/opt/aws/bin
mv %{buildroot}%{_bindir}/cfn-signal %{buildroot}/opt/aws/bin

%files
%doc README.rst LICENSE
/opt/aws/bin/cfn-*
%{python_sitelib}/heat_cfntools*

%changelog
* Thu Dec 24 2012 Steve Baker <sbaker@redhat.com> 1.0-1
- initial fork of heat-jeos
