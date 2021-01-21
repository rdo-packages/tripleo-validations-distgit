# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-validations
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:           openstack-tripleo-validations
Summary:        Ansible playbooks to detect potential issues with TripleO deployments
Version:        11.3.1
Release:        1%{?dist}
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
Requires:       validations-common

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
Requires:       python%{pyver}-oslo-utils >= 3.36.0
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

# Create __init__.py file if doesn't exit
%if %{pyver} == 2
touch library/__init__.py
%endif

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

# TODO remove this when https://review.opendev.org/#/c/740261/ merges
if [ ! -f "%{buildroot}%{_bindir}/tripleo-validation.py" ]; then
cat <<EOF >%{buildroot}%{_bindir}/tripleo-validation.py
#!/usr/bin/env python3
EOF
chmod 755 %{buildroot}%{_bindir}/tripleo-validation.py
fi

# Fix shebangs for Python 3-only distros
# TODO remove this when shebangs workaround will be fixed
if [ ! -d "%{buildroot}%{_datadir}/ansible" ]; then
mkdir -p %{buildroot}%{_datadir}/ansible/library
mkdir -p %{buildroot}%{_datadir}/ansible/lookup_plugins
mkdir -p %{buildroot}%{_datadir}/ansible/callback_plugins
mkdir -p %{buildroot}%{_datadir}/ansible/roles
fi
# TODO: to be removed
# Make compatible with old path openstack-tripleo-validation
if [ ! -d "%{buildroot}%{_datadir}/%{name}" ]; then
mkdir -p %{buildroot}%{_datadir}/%{name}/library
mkdir -p %{buildroot}%{_datadir}/%{name}/lookup_plugins
mkdir -p %{buildroot}%{_datadir}/%{name}/callback_plugins
mkdir -p %{buildroot}%{_datadir}/%{name}/roles
fi

%if %{pyver} == 3
# Fix shebangs for Python 3-only distros
# TODO remove this when shebangs workaround will be fixed
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/library/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/lookup_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/callback_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/roles/
# Fix shebangs for Python 3-only distros
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/library/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/lookup_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/callback_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/roles/
%endif

# Remove useless __init__.py file in library directory
# TODO:(gchamoul) Remove this once https://review.opendev.org/c/openstack/tripleo-validations/+/771797
# will be merged upstream.
rm -fr %{buildroot}%{_datadir}/ansible/library/__init__.py

%check
PYTHON=%{pyver_bin} %{pyver_bin} setup.py testr

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{pyver_sitelib}/tripleo_validations
%{pyver_sitelib}/tripleo_validations-*.egg-info
%{_datadir}/%{name}
%{_datadir}/ansible
%{_bindir}/tripleo-ansible-inventory
%{_bindir}/run-validations.sh
%{_bindir}/tripleo-validation.py
%exclude %{python3_sitelib}/tripleo_validations/test*
%exclude %{_datadir}/ansible/library/__init__.py

%files -n openstack-tripleo-validations-tests
%license LICENSE
%{pyver_sitelib}/tripleo_validations/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Mon Jan 06 2020 RDO <dev@lists.rdoproject.org> 11.3.1-1
- Update to 11.3.1

* Mon Oct 21 2019 RDO <dev@lists.rdoproject.org> 11.3.0-1
- Update to 11.3.0
