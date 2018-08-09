# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pydefault 3
%else
%global pydefault 2
%endif

%global pydefault_bin python%{pydefault}
%global pydefault_sitelib %python%{pydefault}_sitelib
%global pydefault_install %py%{pydefault}_install
%global pydefault_build %py%{pydefault}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-validations
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:           openstack-tripleo-validations
Summary:        Ansible playbooks to detect potential issues with TripleO deployments
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            http://tripleo.org
Source0:        https://tarballs.openstack.org/tripleo-validations/tripleo-validations-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python%{pydefault}-setuptools
BuildRequires:  python%{pydefault}-devel
BuildRequires:  python%{pydefault}-pbr
BuildRequires:  python%{pydefault}-heatclient >= 1.10.0
BuildRequires:  python%{pydefault}-glanceclient >= 2.9.1
BuildRequires:  python%{pydefault}-ironicclient >= 2.3.0
%if %{pydefault} == 2
Requires:       ansible >= 2
%else
Requires:       ansible-python%{pydefault} >= 2
%endif
Requires:       python%{pydefault}-pbr
Requires:       python%{pydefault}-heatclient >= 1.10.0
Requires:       python%{pydefault}-glanceclient >= 2.9.1
Requires:       python%{pydefault}-ironicclient >= 2.3.0
Requires:       python%{pydefault}-shade >= 1.24.0

%description
A collection of Ansible playbooks to detect and report potential issues during
TripleO deployments.

%package -n openstack-tripleo-validations-tests
Summary:        Tests for TripleO validations
Requires:       %{name} = %{version}-%{release}

BuildRequires:  python%{pydefault}-heatclient
BuildRequires:  python%{pydefault}-swiftclient
BuildRequires:  python%{pydefault}-novaclient
BuildRequires:  python%{pydefault}-subunit
BuildRequires:  python%{pydefault}-oslotest
BuildRequires:  python%{pydefault}-testrepository
BuildRequires:  python%{pydefault}-testscenarios
BuildRequires:  python%{pydefault}-testtools
BuildRequires:  python%{pydefault}-netaddr
BuildRequires:  os-net-config
%if %{pydefault} == 2
BuildRequires:  ansible >= 2
%else
BuildRequires:  ansible-python%{pydefault} >= 2
%endif
BuildRequires:  openstack-macros

Requires:       python%{pydefault}-subunit
Requires:       python%{pydefault}-oslotest
Requires:       python%{pydefault}-oslo-config >= 2:5.1.0
Requires:       python%{pydefault}-heatclient >= 1.10.0
Requires:       python%{pydefault}-keystoneauth1 >= 3.3.0
Requires:       python%{pydefault}-mistralclient >= 3.1.0
Requires:       python%{pydefault}-novaclient >= 1:9.1.0
Requires:       python%{pydefault}-ironicclient >= 2.2.0
Requires:       python%{pydefault}-six >= 1.10.0
Requires:       openstack-tripleo-common >= 7.1.0
Requires:       python%{pydefault}-testrepository
Requires:       python%{pydefault}-testscenarios
Requires:       python%{pydefault}-testtools
Requires:       python%{pydefault}-netaddr
Requires:       os-net-config >= 7.1.0
Requires:       ansible >= 2
Requires:       python%{pydefault}-shade >= 1.24.0

%description -n openstack-tripleo-validations-tests
This package contains the tripleo-validations test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Tripleo Validations

BuildRequires:    python%{pydefault}-sphinx
BuildRequires:    python%{pydefault}-openstackdocstheme

%description      doc
This package contains the tripleo-validations Documentation files.
%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pydefault_build}

# docs generation
%if 0%{?with_doc}
%{pydefault_bin} setup.py build_sphinx -b html
%endif

%install
%{pydefault_install}

%check
PYTHON=${pydefault_bin} %{pydefault_bin} setup.py testr

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{pydefault_sitelib}/tripleo_validations
%{pydefault_sitelib}/tripleo_validations-*.egg-info
%{_datadir}/%{name}
%{_bindir}/tripleo-ansible-inventory
%exclude %{pydefault_sitelib}/tripleo_validations/test*

%files -n openstack-tripleo-validations-tests
%license LICENSE
%{pydefault_sitelib}/tripleo_validations/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
