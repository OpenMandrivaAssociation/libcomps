%bcond_without python2
%bcond_with docs

%define major 0
%define libname %mklibname comps %{major}
%define devname %mklibname comps -d

Name:		libcomps
Version:	0.1.12
Release:	1
Summary:	Comps XML file manipulation library
Group:		System/Libraries
License:	GPLv2+
URL:		https://github.com/rpm-software-management/libcomps
# Use the following commands to generate the tarball:
#  git clone https://github.com/rpm-software-management/libcomps.git libcomps-%%{commit}
#  git checkout %%{commit}
#  tar czvf libcomps-%%{version}.tar.gz libcomps-%%{commit}
Source0:	https://github.com/rpm-software-management/libcomps/archive/%{name}-%{version}.tar.gz
# Filters out rpmlint warnings
Source1:	libcomps.rpmlintrc
Patch1:		libcomps-0.1.8-compile.patch
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	cmake
%if %{with docs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif

# prevent provides from nonstandard paths:
%define __provides_exclude_from ^(%{python2_sitearch}/.*\\.so\\|%{python3_sitearch}/.*\\.so)$

%description
Libcomps is library for structure-like manipulation with content of
comps XML files. Supports read/write XML file, structure(s) modification.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
Libraries for %{name}.

%package -n %{devname}
Summary:	Development files for libcomps library
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%if %{with docs}
%package doc
Summary:	Documentation files for libcomps library
Group:		Documentation
Requires:	%{name}-devel = %{EVRD}
BuildArch:	noarch
BuildRequires:	doxygen

%description doc
Documentation files for libcomps library.

%package -n python-libcomps-doc
Summary:	Documentation files for python bindings libcomps library
Group:		Documentation
Requires:	python-%{name} = %{EVRD}
BuildArch:	noarch
BuildRequires:	python-sphinx

%description -n python-libcomps-doc
Documentation files for python bindings libcomps library.
%endif

%package -n python-libcomps
Summary:	Python 3 bindings for libcomps library
Group:		Development/Python
BuildRequires:	pkgconfig(python3)
Provides:	python3-%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n python-libcomps
Python3 bindings for libcomps library.

%if %{with python2}
%package -n python2-libcomps
Summary:	Python 2 bindings for libcomps library
Group:		Development/Python
BuildRequires:	pkgconfig(python2)
%if %{without python2}
Provides:	python-%{name} = %{EVRD}
%endif
Requires:	%{libname} = %{EVRD}

%description -n python2-libcomps
Python2 bindings for libcomps library.
%endif

%prep
%autosetup -n %{name}-%{version} -p1

%if %{with python2}
rm -rf py2
mkdir py2
%endif

%build
%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
%if %{without docs}
	-DENABLE_DOCS=OFF \
%endif
	-DENABLE_TESTS=OFF \
	-DPYTHON_DESIRED:STRING=3 ../libcomps/

%make_build
%if %{with docs}
make docs
make pydocs
%endif

%if %{with python2}
cd ../py2
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DENABLE_TESTS=OFF -DPYTHON_DESIRED:STRING=2 ../../libcomps/
%make_build
cd -
%endif

# (tpg) disable tests for now https://github.com/rpm-software-management/libcomps/issues/60
%if 0
%check
cd ./build
make test
cd -
%if %{with python2}
cd ./py2/build
make pytest
cd -
%endif
%endif

%install
cd ./build
%make_install
cd -
%if %{with python2}
cd ./py2/build
%make_install
cd -
%endif

%files -n %{libname}
%{_libdir}/libcomps.so.%{major}.*

%files -n %{devname}
%doc README.md COPYING
%{_libdir}/libcomps.so
%{_includedir}/*

%if %{with docs}
%files doc
%doc build/docs/libcomps-doc/html

%files -n python-libcomps-doc
%doc build/src/python/docs/html
%endif

%files -n python-libcomps
%{python3_sitearch}/libcomps

%if %{with python2}
%files -n python-libcomps
%{python2_sitearch}/libcomps
%endif
