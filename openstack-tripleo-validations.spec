%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name tripleo-validations
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:           openstack-tripleo-validations
Summary:        Ansible playbooks to detect potential issues with TripleO deployments
Version:        9.3.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            http://tripleo.org
Source0:        https://tarballs.openstack.org/tripleo-validations/tripleo-validations-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python-heatclient >= 1.10.0
BuildRequires:  python-glanceclient >= 2.9.1
BuildRequires:  python-ironicclient >= 2.3.0
Requires:       ansible >= 2
Requires:       python2-pbr
Requires:       python-heatclient >= 1.10.0
Requires:       python-glanceclient >= 2.9.1
Requires:       python-ironicclient >= 2.3.0
Requires:       python2-shade >= 1.24.0

%description
A collection of Ansible playbooks to detect and report potential issues during
TripleO deployments.

%package -n openstack-tripleo-validations-tests
Summary:        Tests for TripleO validations
Requires:       %{name} = %{version}-%{release}

BuildRequires:  python2-heatclient
BuildRequires:  python2-swiftclient
BuildRequires:  python2-novaclient
BuildRequires:  python2-subunit
BuildRequires:  python2-oslotest
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
BuildRequires:  python2-netaddr
BuildRequires:  os-net-config
BuildRequires:  ansible >= 2
BuildRequires:  openstack-macros

Requires:       python2-subunit
Requires:       python2-oslotest
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-heatclient >= 1.10.0
Requires:       python2-keystoneauth1 >= 3.4.0
Requires:       python2-mistralclient >= 3.1.0
Requires:       python2-novaclient >= 1:9.1.0
Requires:       python2-ironicclient >= 2.3.0
Requires:       python2-six >= 1.10.0
Requires:       openstack-tripleo-common >= 7.1.0
Requires:       python2-testrepository
Requires:       python2-testscenarios
Requires:       python2-testtools
Requires:       python2-netaddr
Requires:       os-net-config >= 7.1.0
Requires:       ansible >= 2
Requires:       python2-shade >= 1.24.0

%description -n openstack-tripleo-validations-tests
This package contains the tripleo-validations test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Tripleo Validations

BuildRequires:    python2-sphinx
BuildRequires:    python2-openstackdocstheme

%description      doc
This package contains the tripleo-validations Documentation files.
%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{__python2} setup.py build

# docs generation
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%{__python2} setup.py testr

%files
%license LICENSE
%doc README.rst AUTHORS ChangeLog
%{python2_sitelib}/tripleo_validations
%{python2_sitelib}/tripleo_validations-*.egg-info
%{_datadir}/%{name}
%{_bindir}/tripleo-ansible-inventory
%exclude %{python2_sitelib}/tripleo_validations/test*

%files -n openstack-tripleo-validations-tests
%license LICENSE
%{python2_sitelib}/tripleo_validations/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Mon Aug 27 2018 RDO <dev@lists.rdoproject.org> 9.3.0-1
- Update to 9.3.0

