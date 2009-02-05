Summary:	Asymptote is a powerful descriptive vector graphics language for technical drawing
Summary(hu.UTF-8):	Asymptote egy leíró vektorgrafikus nyelv technikai rajzokhoz
Summary(pl.UTF-8):	Język opisu grafiki wektorowej do rysunków technicznych
Name:		asymptote
Version:	1.61
Release:	1
License:	GPL v3
Group:		Applications/Science
Source0:	http://dl.sourceforge.net/asymptote/%{name}-%{version}.src.tgz
# Source0-md5:	93ce4d40318752ca60f15eef096e4e1a
URL:		http://asymptote.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	gc-devel >= 7.0
BuildRequires:	gsl-devel >= 1.7
BuildRequires:	ncurses-devel
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-tex-babel
BuildRequires:	texinfo-texi2dvi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Asymptote is a powerful descriptive vector graphics language for
technical drawing, inspired by MetaPost but with an improved C++-like
syntax. Asymptote provides for figures the same high-quality level of
typesetting that LaTeX does for scientific text.

%description -l hu.UTF-8
Asymptote egy leíró vektorgrafikus nyelv technikai rajzokhoz, hasonló
a MetaPost-hoz, de kibővítve C++-szerű szintaxissal. Asymptote még
képes olyan szintű szövegszedésre is, amelyre a LaTeX képes a
tudományos szöveggel.

%description -l pl.UTF-8
Asymptote jest językiem opisu grafiki wektorowej dla rysunków
technicznych. Język ten jest inspirowany językiem MetaPost, ale
posiada bogatszą składnię w stylu C++.

%package doc
Summary:	Asymptote documentation
Summary(hu.UTF-8):	Asymptote dokumentáció
Summary(pl.UTF-8):	Dokumentacja do Asymptote
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description doc
Asymptote documentation.

%description doc -l hu.UTF-8
Asymptote dokumentációja.

%description doc -l pl.UTF-8
Dokumentacja do Asymptote.

%package examples
Summary:	Asymptote examples
Summary(hu.UTF-8):	Asymptote példák
Summary(pl.UTF-8):	Przykłady do Asymptote
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Asymptote examples.

%description examples -l hu.UTF-8
Asymptote példák.

%description examples -l pl.UTF-8
Przykładowe pliki dla asymptote.

%prep
%setup -q

%build
%{__autoheader}
%{__autoconf}
%configure \
	CPPFLAGS=-I/usr/include/gc \
	--disable-static \
	--enable-gc=%{_includedir}/gc \
	--with-docdir=%{_docdir}/%{name}-doc
cd doc && for i in %{_datadir}/texmf/tex/texinfo/*; do ln -s $i; done && cd ..

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

# I don't know why need it - maybe the bad tetex configuration?
# And the solution suggested by asympote's doc doesn't work too :(
# cp %{_datadir}/texmf/tex/{plain/pdfcolor/pdfcolor.tex,generic/epsf/epsf.tex,texinfo/texinfo.tex} doc
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-doc/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO BUGS
%attr(755,root,root) %{_bindir}/asy
%attr(755,root,root) %{_bindir}/xasy
%{_datadir}/%{name}
%{_datadir}/texmf*/tex/latex/asymptote
%{_mandir}/man1/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc
