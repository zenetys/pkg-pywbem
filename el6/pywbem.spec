%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define setuptools_version 12.4

Name:           pywbem
Version:        0.11.0
Release:        1%{dist}.zenetys
Summary:        Python WBEM Client and Provider Interface
Group:          Development/Libraries
License:        LGPLv2
URL:            http://pywbem.sourceforge.net

Source0:        https://files.pythonhosted.org/packages/source/p/pywbem/pywbem-%{version}.tar.gz
Source1:        https://files.pythonhosted.org/packages/source/s/setuptools/setuptools-%{setuptools_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-setuptools

Requires:       PyYAML
Requires:       m2crypto
Requires:       python-ply
Requires:       python-six

%description
A Python library for making CIM (Common Information Model) operations over HTTP
using the WBEM CIM-XML protocol. It is based on the idea that a good WBEM
client should be easy to use and not necessarily require a large amount of
programming knowledge. It is suitable for a large range of tasks from simply
poking around to writing web and GUI applications.

WBEM, or Web Based Enterprise Management is a manageability protocol, like
SNMP, standardised by the Distributed Management Task Force (DMTF) available
at http://www.dmtf.org/standards/wbem.

It also provides a Python provider interface, and is the fastest and
easiest way to write providers on the planet.

%prep
%setup -q
%setup -q -T -D -b 1

%build
pushd .
cd ../setuptools-%{setuptools_version}
%{__python} setup.py build
popd

PYTHONPATH=../setuptools-%{setuptools_version}/build/lib \
CFLAGS="%{optflags}" \
    %{__python} setup.py build

%install
rm -rf %{buildroot}

PYTHONPATH=../setuptools-%{setuptools_version}/build/lib \
    %{__python} setup.py install -O1 --skip-build --root %{buildroot}

rm -f %{buildroot}/%{_bindir}/*.bat

# preserve compatibility with pywbem 0.7.0 standard package
# and avoid conflict with sblim-wbemcli
mv %{buildroot}/%{_bindir}/{mof_compiler,mofcomp}
mv %{buildroot}/%{_bindir}/{,py}wbemcli
mv %{buildroot}/%{_bindir}/{,py}wbemcli.py
sed -i -e 's,wbemcli,pywbemcli,' %{buildroot}/%{_bindir}/pywbemcli

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%attr(755,root,root) %{_bindir}/mofcomp
%attr(755,root,root) %{_bindir}/pywbemcli
%attr(755,root,root) %{_bindir}/pywbemcli.py
%doc README.rst

%changelog
* Fri Jan 05 2018 Julien Thomas <julthomas@free.fr> - 0.11.0-1
- Update to pywbem version 0.11.0

* Thu May 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.0-4
- rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 28 2009 David Nalley <david@gnsa.us> 0.7.0-2
- Added some verbiage regarding what WBEM is and expanding WBEM and CIM acronyms
- Added python-twisted as a dependency

* Thu Jun 25 2009 David Nalley <david@gnsa.us> 0.7.0-1
- Initial packaging
