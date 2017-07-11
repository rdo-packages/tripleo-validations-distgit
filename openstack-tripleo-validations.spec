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
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
Requires:       ansible >= 2
Requires:       python-pbr
Requires:       python-setuptools

%description
A collection of Ansible playbooks to detect and report potential issues during
TripleO deployments.

%package -n openstack-tripleo-validations-tests
Summary:        Tests for TripleO validations
Requires:       %{name} = %{version}-%{release}

BuildRequires:  python-coverage
BuildRequires:  python-heatclient
BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-netaddr
BuildRequires:  ansible >= 2

Requires:       python-coverage
Requires:       python-subunit
Requires:       python-oslotest
Requires:       python-oslo-config >= 2:3.14.0
Requires:       python-heatclient >= 1.6.1
Requires:       python-keystoneauth1 >= 2.18.0
Requires:       python-mistralclient >= 2.0.0
Requires:       python-novaclient >= 1:7.1.0
Requires:       python-testrepository
Requires:       python-testscenarios
Requires:       python-testtools
Requires:       python-netaddr
Requires:       ansible >= 2

%description -n openstack-tripleo-validations-tests
This package contains the tripleo-validations test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Tripleo Validations

BuildRequires:    python-sphinx
BuildRequires:    python-openstackdocstheme

%description      doc
This package contains the tripleo-validations Documentation files.
%endif

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

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