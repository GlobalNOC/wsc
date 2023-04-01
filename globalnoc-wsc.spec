%{?scl:%scl_package globalnoc-wsc}

################################################################################
# NOTE: YOU PROBABLY DO NOT NEED TO CHANGE THESE

%global py_pkg %(echo '%{py_name}' | sed -e 's/-/_/g')
%global python3_wheelname %{py_pkg}-%{py_version}-py3-none-any.whl

# space separated list of python scripts to copy to %{_bindir}
# pull from pyproject.toml -- keys from tool.poetry.scripts
%global py_scripts %(toml get pyproject.toml tool.poetry.scripts | jq -r 'keys | @csv' | sed -e 's/"//g' -e 's/,/ /g')

# summary/description text
# pull this from pyproject.toml
%global pkg_summary %(toml get --raw pyproject.toml tool.poetry.description)

# package release number (use 1 if unsure)
%global pkg_release 1

################################################################################
# NOTE: DO NOT CHANGE THESE UNLESS YOU KNOW WHAT YOU'RE DOING

# use bash for the build shell
%global _buildshell /bin/bash

# skip RPM bytecompilation -- it doesn't work with python3.8
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-scl-python-bytecompile[[:space:]].*$!!g')

################################################################################
# NOTE: Unless you need to set BuildArch, these are probably fine as they are

Name:           %{scl_prefix}%{py_name}
Version:        %{py_version}
Release:        %{pkg_release}%{?dist}
Summary:        %{pkg_summary}

License:        Apache-2.0

# the location isn't used, but rpmlint complains if this isn't a URL
Source0:        https://github.grnoc.iu.edu/%{name}-%{version}.tar.gz

BuildArch:      noarch
AutoReqProv:    no

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-rpm-macros
BuildRequires:  %{?scl_prefix}virtualenv-tools3
BuildRequires:  jq
BuildRequires:  toml

Requires:       %{?scl_prefix}python(abi) = 3.8
Requires:       %{?scl_prefix}python-lxml
Requires:       %{?scl_prefix}python-requests
%{?scl:Requires: %scl_runtime}

################################################################################
# NOTE: This should work as is as long as you are using poetry

%description
%{pkg_summary}

%prep
%autosetup -n %{py_name}-%{py_version}

%build

################################################################################
# NOTE: Check the install and files section carefully

%install
rm -rf %{buildroot}

# create directories
%{__install} -d %{buildroot}
%{__install} -d %{buildroot}/%{_bindir}

# install python scripts
for s in %{py_scripts}; do
    %{__install} venv/bin/$s %{buildroot}/%{_bindir}
done

# install python wheel package
%python38py3_install_wheel ../%{python3_wheelname}

%files
%{_bindir}/*
/opt/rh/rh-python38/root/usr/lib/python3.8/site-packages
