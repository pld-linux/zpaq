Summary:	Data Compression Programs
Summary(pl.UTF-8):	Programy do kompresji danych
Name:		zpaq
Version:	7.15
%define	pkg_ver	%(echo %{version} | tr -d .)
Release:	1
License:	Public Domain
Group:		Applications/Archiving
#Source0Download: http://mattmahoney.net/dc/zpaq.html
Source0:	http://mattmahoney.net/dc/%{name}%{pkg_ver}.zip
# Source0-md5:	1779c19decc885b44636c497b61d937a
URL:		http://mattmahoney.net/dc/zpaq.html
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

%{__rm} *.exe

%build
%{__make} \
	CXX="%{__cxx}" \
	CPPFLAGS="%{rpmcppflags} -Dunix" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags} %{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING readme.txt
%attr(755,root,root) %{_bindir}/zpaq
%{_mandir}/man1/zpaq.1*
