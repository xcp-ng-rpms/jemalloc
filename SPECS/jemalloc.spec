%global package_speccommit 13536b04ed41cbe31886788a8ff021f8efcd5f6b
%global usver 3.6.0
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
Name:           jemalloc
Version:        3.6.0

Release: %{?xsrel}%{?dist}
Summary:        General-purpose scalable concurrent malloc implementation

Group:          System Environment/Libraries
License:        BSD-2-Clause
URL:            http://www.canonware.com/jemalloc/
Source0: jemalloc-3.6.0.tar.bz2
Patch0: 0001-Do-not-package-pprof.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Remove pprof, as it already exists in google-perftools
# ARMv5tel has no atomic operations
# RHEL5/POWER has no atomic operations
BuildRequires:  /usr/bin/xsltproc

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
%defattr(-,root,root,-)
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh
%doc COPYING README VERSION
%doc doc/jemalloc.html
%ifarch ppc ppc64
%if 0%{?rhel} == 5
%doc COPYING.epel5-ppc
%endif
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Tue Mar 28 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 3.6.0-2
- First imported release

