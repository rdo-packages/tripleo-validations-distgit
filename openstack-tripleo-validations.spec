
%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-validations
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:           openstack-tripleo-validations
Summary:        Ansible playbooks to detect potential issues with TripleO deployments
Version:        12.3.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            http://tripleo.org
Source0:        https://tarballs.openstack.org/tripleo-validations/tripleo-validations-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-heatclient >= 1.10.0
BuildRequires:  python3-glanceclient >= 2.9.1
BuildRequires:  python3-ironicclient >= 2.3.0
Requires:       python3dist(ansible) >= 2
BuildRequires:  /usr/bin/pathfix.py
Requires:       python3-pbr
Requires:       python3-heatclient >= 1.10.0
Requires:       python3-glanceclient >= 2.9.1
Requires:       python3-ironicclient >= 2.7.0
Requires:       python3-shade >= 1.24.0
Requires:       os-net-config >= 7.1.0
Requires:       python3-ironic-inspector-client >= 3.1.1
Requires:       validations-common

%description
A collection of Ansible playbooks to detect and report potential issues during
TripleO deployments.

%package -n openstack-tripleo-validations-tests
Summary:        Tests for TripleO validations
Requires:       %{name} = %{version}-%{release}

BuildRequires:  python3-heatclient
BuildRequires:  python3-netaddr
BuildRequires:  python3-novaclient
BuildRequires:  python3-oslotest
BuildRequires:  python3-subunit
BuildRequires:  python3-swiftclient
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  os-net-config
BuildRequires:  python3dist(ansible) >= 2
BuildRequires:  openstack-macros

Requires:       python3-subunit
Requires:       python3-oslotest
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-utils >= 3.40.2
Requires:       python3-heatclient >= 1.10.0
Requires:       python3-keystoneauth1 >= 3.16.0
Requires:       python3-mistralclient >= 3.1.0
Requires:       python3-novaclient >= 1:15.1.0
Requires:       python3-ironicclient >= 2.7.0
Requires:       python3-six >= 1.11.0
Requires:       openstack-tripleo-common >= 7.1.0
Requires:       python3-testrepository
Requires:       python3-testscenarios
Requires:       python3-testtools
Requires:       python3-netaddr
Requires:       os-net-config >= 7.1.0
Requires:       python3-shade >= 1.24.0
Requires:       python3-ironic-inspector-client >= 3.1.1
Requires:       validations-common

Requires:       python3dist(ansible) >= 2

%description -n openstack-tripleo-validations-tests
This package contains the tripleo-validations test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Tripleo Validations

BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme

%description      doc
This package contains the tripleo-validations Documentation files.
%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

# docs generation
%if 0%{?with_doc}
sphinx-build -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_bindir}/tripleo-validation.py

# Fix shebangs for Python 3-only distros
# TODO remove this when shebangs workaround will be fixed
if [ ! -d "%{buildroot}%{_datadir}/ansible" ]; then
mkdir -p %{buildroot}%{_datadir}/ansible/library
mkdir -p %{buildroot}%{_datadir}/ansible/lookup_plugins
mkdir -p %{buildroot}%{_datadir}/ansible/callback_plugins
mkdir -p %{buildroot}%{_datadir}/ansible/roles
fi
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/library/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/lookup_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/callback_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/roles/

# TODO: to be removed
# Make compatible with old path openstack-tripleo-validation
if [ ! -d "%{buildroot}%{_datadir}/%{name}" ]; then
mkdir -p %{buildroot}%{_datadir}/%{name}/library
mkdir -p %{buildroot}%{_datadir}/%{name}/lookup_plugins
mkdir -p %{buildroot}%{_datadir}/%{name}/callback_plugins
mkdir -p %{buildroot}%{_datadir}/%{name}/roles
fi
# Fix shebangs for Python 3-only distros
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/library/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/lookup_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/callback_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/roles/

%check
PYTHON=%{__python3} %{__python3} setup.py testr

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python3_sitelib}/tripleo_validations
%{python3_sitelib}/tripleo_validations-*.egg-info
# TODO to be removed:
# Make old path compatible
%{_datadir}/%{name}
%{_datadir}/ansible
%{_bindir}/tripleo-ansible-inventory
%{_bindir}/run-validations.sh
%{_bindir}/tripleo-validation.py
%exclude %{python3_sitelib}/tripleo_validations/test*

%files -n openstack-tripleo-validations-tests
%license LICENSE
%{python3_sitelib}/tripleo_validations/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Mon Oct 05 2020 RDO <dev@lists.rdoproject.org> 12.3.2-1
- Update to 12.3.2

* Tue Jul 28 2020 RDO <dev@lists.rdoproject.org> 12.3.1-1
- Update to 12.3.1

* Tue May 26 2020 RDO <dev@lists.rdoproject.org> 12.3.0-1
- Update to 12.3.0


