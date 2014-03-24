%define pkg_version 110
Summary:	Data Compression Programs
Name:		zpaq
Version:	1.10
Release:	0.1
Group:		Applications/Archiving
URL:		http://mattmahoney.net/dc/
Source0:	http://mattmahoney.net/dc/%{name}%{pkg_version}.zip
# from debian git clone git://git.debian.org/git/collab-maint/zpaq.git zpaq
Source1:	%{name}-pod2man.mk
Source2:	%{name}-unzpaq.1.pod
Source3:	%{name}-zpaq.1.pod
Source4:	%{name}make.in
Source5:	%{name}_c629f5bbb5181207e7e76ca99f5e0655d57086e5.cpp
License:	GPL
BuildRequires:	libgcc
BuildRequires:	libstdc++6-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZPAQ is a configurable file compressor and archiver. Its goal is a
high compression ratio in an open format without loss of compatibility
between versions as new compression algorithms are discovered. ZPAQ
includes tools to help develop and test new algorithms.

%prep

%setup -q -c
rm -rf *.exe *.bat

mkdir man
cp -pr %{SOURCE1} man/pod2man.mk
cp -pr %{SOURCE2} man/unzpaq.1.pod
cp -pr %{SOURCE3} man/zpaq.1.pod

sed -e 's:^pcomp :&%{_prefix}/libexec/zpaq/:' -i *.cfg

stripflag=' -Wl,--strip-all'
echo 'int main(void) {return 0;}' > striptest.cpp
%{__make} LDFLAGS+="${stripflag}" striptest
sed \
	-e "s:%CXX%:${CXX}:" \
	-e "s:%CXXFLAGS%:${CXXFLAGS}:" \
	-e "s:%LIBDIR%:%{_libdir}:" \
	-e "s:%LDFLAGS%:${LDFLAGS}${stripflag}:" \
	%{SOURCE4} > zpaqmake

cp -pr zpaq.cpp unzpaq.cpp
cp -pr zpaq.h unzpaq.h

%build

printf '#define OPT\n#include "zpaq.cpp"\n' > zpaqstub.cpp
%{__make} CPPFLAGS+=-DNDEBUG zpaq unzpaq lzppre zpaqstub.o

%{__make} -C man -f pod2man.mk PACKAGE=zpaq makeman
%{__make} -C man -f pod2man.mk PACKAGE=unzpaq makeman

%install
rm -rf $RPM_BUILD_ROOT
[ "$RPM_BUILD_ROOT" != / ] && rm -rf "$RPM_BUILD_ROOT"

install -d $RPM_BUILD_ROOT%{_bindir}
install -pm 755 zpaqmake zpaq unzpaq $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT%{_datadir}/zpaq
install -pm 644 *.cfg $RPM_BUILD_ROOT%{_datadir}/zpaq
install -d $RPM_BUILD_ROOT%{_libexecdir}/zpaq
install -pm 755 lzppre $RPM_BUILD_ROOT%{_libexecdir}/zpaq

install -d $RPM_BUILD_ROOT%{_libdir}/zpaq
install -pm 755 zpaqstub.o $RPM_BUILD_ROOT%{_libdir}/zpaq
install -d $RPM_BUILD_ROOT%{_includedir}/zpaq
install -pm 644 zpaq.h $RPM_BUILD_ROOT%{_includedir}/zpaq

install -d $RPM_BUILD_ROOT%{_mandir}/man1/
install -pm 644 man/*zpaq.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
[ "$RPM_BUILD_ROOT" != / ] && rm -rf "%{buildroot}"

%post
%{_bindir}/zpaq oc %{_datadir}/zpaq/max.cfg out.zpaq files &>/dev/null || :

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/unzpaq
%attr(755,root,root) %{_bindir}/zpaq
%attr(755,root,root) %{_bindir}/zpaqmake
%{_includedir}/zpaq/zpaq.h
%{_libdir}/zpaq/zpaqstub.o
%{_libexecdir}/zpaq/lzppre
%{_mandir}/man1/unzpaq.1*
%{_mandir}/man1/zpaq.1*
%{_datadir}/zpaq/max.cfg
%{_datadir}/zpaq/mid.cfg
%{_datadir}/zpaq/min.cfg
%doc LICENSE readme.txt

%changelog
* Thu Sep 23 2010 gil <puntogil@libero.it> 1.10-1mamba
- package created by autospec
