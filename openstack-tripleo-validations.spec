# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
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
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-heatclient >= 1.10.0
BuildRequires:  python%{pyver}-glanceclient >= 2.9.1
BuildRequires:  python%{pyver}-ironicclient >= 2.3.0
%if %{pyver} == 2
Requires:       ansible >= 2
%else
Requires:       python3dist(ansible) >= 2
BuildRequires:  /usr/bin/pathfix.py
%endif
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-heatclient >= 1.10.0
Requires:       python%{pyver}-glanceclient >= 2.9.1
Requires:       python%{pyver}-ironicclient >= 2.3.0
Requires:       python%{pyver}-shade >= 1.24.0
Requires:       os-net-config >= 7.1.0
Requires:       python%{pyver}-ironic-inspector-client >= 3.1.1

%description
A collection of Ansible playbooks to detect and report potential issues during
TripleO deployments.

%package -n openstack-tripleo-validations-tests
Summary:        Tests for TripleO validations
Requires:       %{name} = %{version}-%{release}

BuildRequires:  python%{pyver}-heatclient
BuildRequires:  python%{pyver}-netaddr
BuildRequires:  python%{pyver}-novaclient
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-swiftclient
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  os-net-config
%if %{pyver} == 2
BuildRequires:  ansible >= 2
%else
BuildRequires:  python3dist(ansible) >= 2
%endif
BuildRequires:  openstack-macros

Requires:       python%{pyver}-subunit
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-heatclient >= 1.10.0
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-mistralclient >= 3.1.0
Requires:       python%{pyver}-novaclient >= 1:9.1.0
Requires:       python%{pyver}-ironicclient >= 2.3.0
Requires:       python%{pyver}-six >= 1.10.0
Requires:       openstack-tripleo-common >= 7.1.0
Requires:       python%{pyver}-testrepository
Requires:       python%{pyver}-testscenarios
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-netaddr
Requires:       os-net-config >= 7.1.0
Requires:       python%{pyver}-shade >= 1.24.0
Requires:       python%{pyver}-ironic-inspector-client >= 3.1.1

%if %{pyver} == 2
Requires:       ansible >= 2
%else
Requires:       python3dist(ansible) >= 2
%endif

%description -n openstack-tripleo-validations-tests
This package contains the tripleo-validations test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Tripleo Validations

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme

%description      doc
This package contains the tripleo-validations Documentation files.
%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pyver_build}

# docs generation
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
%endif

%install
%{pyver_install}

%if %{pyver} == 3
# Fix shebangs for Python 3-only distros
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/validations/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/library/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/lookup_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/callback_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/roles/
%endif

#%check
#PYTHON=%{pyver_bin} %{pyver_bin} setup.py testr

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{pyver_sitelib}/tripleo_validations
%{pyver_sitelib}/tripleo_validations-*.egg-info
%{_datadir}/%{name}
%{_bindir}/tripleo-ansible-inventory
%{_bindir}/run-validations.sh
%exclude %{pyver_sitelib}/tripleo_validations/test*

%files -n openstack-tripleo-validations-tests
%license LICENSE
%{pyver_sitelib}/tripleo_validations/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/tripleo-validations/commit/?id=42b2a2068cb4c2c0369a47b5c7fc3d376e97c7ef
