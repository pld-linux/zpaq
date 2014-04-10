%define pkg_version 110
Summary:	Data Compression Programs
Summary(pl.UTF-8):	Programy do kompresji danych
Name:		zpaq
Version:	1.10
Release:	0.1
License:	GPL
Group:		Applications/Archiving
Source0:	http://mattmahoney.net/dc/%{name}%{pkg_version}.zip
# from debian git clone git://git.debian.org/git/collab-maint/zpaq.git zpaq
Source1:	%{name}-pod2man.mk
Source2:	%{name}-unzpaq.1.pod
Source3:	%{name}-zpaq.1.pod
Source4:	%{name}make.in
Source5:	%{name}_c629f5bbb5181207e7e76ca99f5e0655d57086e5.cpp
URL:		http://mattmahoney.net/dc/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZPAQ is a configurable file compressor and archiver. Its goal is a
high compression ratio in an open format without loss of compatibility
between versions as new compression algorithms are discovered. ZPAQ
includes tools to help develop and test new algorithms.

%description -l pl.UTF-8
ZPAQ to konfigurowalny kompresor i archiwizer plików. Jego celem jest
duży współczynnik kompresji w otwartym formacie bez utraty zgodności
między wersjami w miarę wykrywania nowych algorytmów kompresji. ZPAQ
zawiera narzędzia pomagające tworzyć i testować nowe algorytmy.

%prep
%setup -q -c

%{__rm} *.exe *.bat

mkdir man
cp -pr %{SOURCE1} man/pod2man.mk
cp -pr %{SOURCE2} man/unzpaq.1.pod
cp -pr %{SOURCE3} man/zpaq.1.pod

sed -e 's:^pcomp :&%{_prefix}/libexec/zpaq/:' -i *.cfg

sed \
	-e "s:%CXX%:%{__cxx}:" \
	-e "s:%CXXFLAGS%:%{rpmcxxflags}:" \
	-e "s:%LIBDIR%:%{_libdir}:" \
	-e "s:%LDFLAGS%:%{rpmldflags}:" \
	%{SOURCE4} > zpaqmake

cp -pr zpaq.cpp unzpaq.cpp
cp -pr zpaq.h unzpaq.h

%build
printf '#define OPT\n#include "zpaq.cpp"\n' > zpaqstub.cpp
%{__make} zpaq unzpaq lzppre zpaqstub.o \
	CPPFLAGS+=-DNDEBUG

%{__make} -C man -f pod2man.mk makeman \
	PACKAGE=zpaq
%{__make} -C man -f pod2man.mk makeman \
	PACKAGE=unzpaq

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -p zpaqmake zpaq unzpaq $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/zpaq
install -pm 644 *.cfg $RPM_BUILD_ROOT%{_datadir}/zpaq
install -d $RPM_BUILD_ROOT%{_libexecdir}/zpaq
install -pm 755 lzppre $RPM_BUILD_ROOT%{_libexecdir}/zpaq

install -d $RPM_BUILD_ROOT%{_libdir}/zpaq
install -pm 644 zpaqstub.o $RPM_BUILD_ROOT%{_libdir}/zpaq
install -d $RPM_BUILD_ROOT%{_includedir}/zpaq
install -pm 644 zpaq.h $RPM_BUILD_ROOT%{_includedir}/zpaq

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -pm 644 man/*zpaq.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/zpaq oc %{_datadir}/zpaq/max.cfg out.zpaq files >/dev/null 2>&1 || :

%files
%defattr(644,root,root,755)
%doc LICENSE readme.txt
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
