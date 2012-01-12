%define 	module	pysam
Summary:	Python module for reading and manipulating Samfiles
#Summary(pl.UTF-8):	-
Name:		python-%{module}
Version:	0.6
Release:	1
License:	MIT
Group:		Development/Languages/Python
Source0:	http://pysam.googlecode.com/files/%{module}-%{version}.tar.gz
# Source0-md5:	395f59d7b765d9f625f6d82fce905dc7
URL:		http://code.google.com/p/pysam/
# remove BR: python-devel for 'noarch' packages.
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-libs
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pysam is a python module for reading and manipulating Samfiles.
It's a lightweight wrapper of the samtools C-API. 

#%description -l pl.UTF-8

%prep
%setup -q -n %{module}-%{version}

# fix #!/usr/bin/env python -> #!/usr/bin/python:
%{__sed} -i -e '1s,^#!.*python,#!%{__python},' tests/*.py

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc THANKS
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-*.egg-info
%endif
