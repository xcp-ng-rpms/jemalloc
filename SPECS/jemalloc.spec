%global package_speccommit 94e340a21a60558f75ffba6d1847c8e89280747f
%global usver 5.3.0
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
Name:           jemalloc
Version:        5.3.0

Release: %{?xsrel}%{?dist}
Summary:        General-purpose scalable concurrent malloc implementation

Group:          System Environment/Libraries
License:        BSD-2-Clause
URL:            http://www.canonware.com/jemalloc/
Source0: jemalloc-5.3.0.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Remove pprof, as it already exists in google-perftools
# ARMv5tel has no atomic operations
# RHEL5/POWER has no atomic operations
BuildRequires:  /usr/bin/xsltproc

BuildRequires: gcc

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build

%configure
%{__make} %{?_smp_mflags}


%check
make check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Install this with doc macro instead
rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'


%files
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh
%doc COPYING README VERSION
%doc doc/jemalloc.html

%files devel
%{_includedir}/jemalloc
%{_bindir}/jemalloc-config
%{_libdir}/pkgconfig/jemalloc.pc
%{_bindir}/jeprof
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%ldconfig_scriptlets

%changelog
* Thu Aug 01 2024 Stephen Cheng <stephen.cheng@cloud.com> - 5.3.0-1
- Updated to 5.3.0

* Tue Mar 28 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 3.6.0-2
- First imported release

