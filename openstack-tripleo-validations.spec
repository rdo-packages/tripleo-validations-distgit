%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-validations
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:           openstack-tripleo-validations
Summary:        Ansible playbooks to detect potential issues with TripleO deployments
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://opendev.org/openstack/tripleo-validations
Source0:        https://tarballs.openstack.org/tripleo-validations/tripleo-validations-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/tripleo-validations/tripleo-validations-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:  git-core
BuildRequires:  python3-setuptools >= 50.3.0
BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 3.1.1
BuildRequires:  python3-heatclient >= 1.10.0
BuildRequires:  python3-glanceclient >= 2.9.1
BuildRequires:  python3-ironicclient >= 2.3.0
BuildRequires:  /usr/bin/pathfix.py

Requires:       (python3dist(ansible) >= 2 or ansible-core >= 2.11)
Requires:       ansible-collection-ansible-posix >= 1.2.0
Requires:       ansible-collection-community-general >= 2.5.1
Requires:       ansible-collection-containers-podman >= 1.4.1
Requires:       python3-pbr >= 3.1.1
Requires:       python3-heatclient >= 1.10.0
Requires:       python3-glanceclient >= 2.9.1
Requires:       python3-ironicclient >= 2.7.0
Requires:       python3-shade >= 1.24.0
Requires:       os-net-config >= 7.1.0
Requires:       python3-ironic-inspector-client >= 3.1.1
Requires:       python3-lxml
Requires:       validations-common
Requires:       python3-setuptools >= 50.3.0

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
BuildRequires:  (python3dist(ansible) >= 2 or ansible-core >= 2.11)
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
Requires:       python3-testtools >= 2.2.0
Requires:       python3-netaddr >= 0.7.18
Requires:       os-net-config >= 7.1.0
Requires:       python3-shade >= 1.24.0
Requires:       python3-ironic-inspector-client >= 3.1.1
Requires:       tripleo-ansible >= 3.3.1
Requires:       ansible-collections-openstack >= 1.8.0

Requires:       (python3dist(ansible) >= 2 or ansible-core >= 2.11)

%description -n openstack-tripleo-validations-tests
This package contains the tripleo-validations test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Tripleo Validations

BuildRequires:    python3-sphinx >= 2.0.0
BuildRequires:    python3-openstackdocstheme >= 2.2.2
BuildRequires:    python3-ruamel-yaml >= 0.15.5

%description      doc
This package contains the tripleo-validations Documentation files.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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

# Fix shebangs for Python 3-only distros
# TODO remove this when shebangs workaround will be fixed
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/library/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/lookup_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/callback_plugins/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/ansible/roles/

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python3_sitelib}/tripleo_validations
%{python3_sitelib}/tripleo_validations-*.egg-info
%{_datadir}/ansible
%{_bindir}/tripleo-ansible-inventory
%exclude %{python3_sitelib}/tripleo_validations/test*
%exclude %{buildroot}%{_datadir}/ansible/library/__init__.py

%files -n openstack-tripleo-validations-tests
%license LICENSE
%{python3_sitelib}/tripleo_validations/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

