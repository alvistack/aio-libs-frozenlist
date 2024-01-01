# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: python-frozenlist
Epoch: 100
Version: 1.5.0
Release: 1%{?dist}
Summary: List-like structure implements collections.abc.MutableSequence
License: Apache-2.0
URL: https://github.com/aio-libs/frozenlist/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: fdupes
BuildRequires: python-rpm-macros
BuildRequires: python3-Cython3
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
The list is mutable until FrozenList.freeze() is called, after which
list modifications raise RuntimeError. A FrozenList instance is
hashable, but only when frozen. Attempts to hash a non-frozen instance
will result in a RuntimeError exception.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
python3 -m cython -3 frozenlist/*.pyx -I frozenlist
%py3_build

%install
%py3_install
find %{buildroot}%{python3_sitearch} -type f -name '*.pyc' -exec rm -rf {} \;
fdupes -qnrps %{buildroot}%{python3_sitearch}

%check

%if 0%{?suse_version} > 1500
%package -n python%{python3_version_nodots}-frozenlist
Summary: List-like structure implements collections.abc.MutableSequence
Requires: python3
Provides: python3-frozenlist = %{epoch}:%{version}-%{release}
Provides: python3dist(frozenlist) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-frozenlist = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(frozenlist) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-frozenlist = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(frozenlist) = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-frozenlist
The list is mutable until FrozenList.freeze() is called, after which
list modifications raise RuntimeError. A FrozenList instance is
hashable, but only when frozen. Attempts to hash a non-frozen instance
will result in a RuntimeError exception.

%files -n python%{python3_version_nodots}-frozenlist
%license LICENSE
%{python3_sitearch}/*
%endif

%if !(0%{?suse_version} > 1500)
%package -n python3-frozenlist
Summary: List-like structure implements collections.abc.MutableSequence
Requires: python3
Provides: python3-frozenlist = %{epoch}:%{version}-%{release}
Provides: python3dist(frozenlist) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-frozenlist = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(frozenlist) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-frozenlist = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(frozenlist) = %{epoch}:%{version}-%{release}

%description -n python3-frozenlist
The list is mutable until FrozenList.freeze() is called, after which
list modifications raise RuntimeError. A FrozenList instance is
hashable, but only when frozen. Attempts to hash a non-frozen instance
will result in a RuntimeError exception.

%files -n python3-frozenlist
%license LICENSE
%{python3_sitearch}/*
%endif

%changelog
