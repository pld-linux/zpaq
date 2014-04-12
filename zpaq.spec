%define pkg_version 650
Summary:	Data Compression Programs
Summary(pl.UTF-8):	Programy do kompresji danych
Name:		zpaq
Version:	6.50
Release:	1
License:	GPL v3
Group:		Applications/Archiving
#Source0Download: http://mattmahoney.net/dc/zpaq.html
Source0:	http://mattmahoney.net/dc/%{name}%{pkg_version}.zip
# Source0-md5:	7412265ebf52f0b3340677e7a1f2540c
# from debian git clone git://git.debian.org/git/collab-maint/zpaq.git zpaq
Source1:	%{name}-pod2man.mk
Source2:	unzpaq.1.pod
Source3:	zpaq.1.pod
URL:		http://mattmahoney.net/dc/zpaq.html
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
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

mkdir man
cp -p %{SOURCE1} man/pod2man.mk
cp -p %{SOURCE2} man/unzpaq.1.pod
cp -p %{SOURCE3} man/zpaq.1.pod

%{__sed} -e 's/gcc -O3/$(CC) $(CFLAGS)/' \
	-e 's/g++ -O3/$(CXX) $(CXXFLAGS)/' -i Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	CXX="%{__cxx}"
	CXXFLAGS="%{__cxx} %{rpmldflags} %{rpmcxxflags} %{rpmcppflags}"

%{__make} -C man -f pod2man.mk makeman \
	PACKAGE=zpaq
%{__make} -C man -f pod2man.mk makeman \
	PACKAGE=unzpaq

%install
rm -rf $RPM_BUILD_ROOT

install -D zpaq $RPM_BUILD_ROOT%{_bindir}/zpaq
ln -s zpaq $RPM_BUILD_ROOT%{_bindir}/unzpaq
install -Dp man/zpaq.1 $RPM_BUILD_ROOT%{_mandir}/man1/zpaq.1
install -Dp man/unzpaq.1 $RPM_BUILD_ROOT%{_mandir}/man1/unzpaq.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme.txt
%attr(755,root,root) %{_bindir}/unzpaq
%attr(755,root,root) %{_bindir}/zpaq
%{_mandir}/man1/unzpaq.1*
%{_mandir}/man1/zpaq.1*
