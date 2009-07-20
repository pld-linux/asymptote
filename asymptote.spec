Summary:	Asymptote is a powerful descriptive vector graphics language for technical drawing
Summary(hu.UTF-8):	Asymptote egy leíró vektorgrafikus nyelv technikai rajzokhoz
Summary(pl.UTF-8):	Język opisu grafiki wektorowej do rysunków technicznych
Name:		asymptote
Version:	1.82
Release:	1
License:	GPL v3
Group:		Applications/Science
Source0:	http://dl.sourceforge.net/asymptote/%{name}-%{version}.src.tgz
# Source0-md5:	0960360e00e8a1a6b84acb70f623ca72
Patch0:		%{name}-memrchr.patch
URL:		http://asymptote.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	gc-devel >= 7.0
BuildRequires:	gsl-devel >= 1.7
BuildRequires:	ncurses-devel
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	texinfo-texi2dvi
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-ams
BuildRequires:	texlive-latex
BuildRequires:	texlive-tex-babel
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

%package gui
Summary:	GUI for asymptote
Summary(hu.UTF-8):	GUI asymptote-hoz
Summary(pl.UTF-8):	Graficzny interfejs do asymptote
Group:		Applications/Science
Requires:	%{name} = %{version}-%{release}

%description gui
GUI for asymptote.

%description gui -l hu.UTF-8
GUI asymptote-hoz.

%description gui -l hu.UTF-8 -l pl.UTF-8
Graficzny interfejs do asymptote.

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

%package latex
Summary:	LaTeX styles
Summary(hu.UTF-8):	LaTeX stílusok
Summary(pl.UTF-8):	Style LaTeXa
Group:		Applications/Publishing/TeX
Requires(post,postun):	%{_bindir}/texhash

%description latex
LaTeX styles.

%description latex -l hu.UTF-8
LaTeX stílusok.

%description latex -l pl.UTF-8
Style LaTeXa.

%package context
Summary:	ConTeXt color macros
Group:		Applications/Publishing/TeX

%description context
ConTeXt color macros.

%package -n vim-syntax-asymptote
Summary:	Vim syntax file to asy-files
Summary(hu.UTF-8):	Vim syntax fájl asy fájlokhoz
Group:		Applications/Editors/Vim

%description -n vim-syntax-asymptote
Vim syntax file to asy files.

%description -n vim-syntax-asymptote -l hu.UTF-8
Vim syntax fájl asy fájlokhoz.

%prep
%setup -q
%patch0 -p1

%build
%{__autoheader}
%{__autoconf}
%configure \
	CPPFLAGS=-I/usr/include/gc \
	--disable-static \
	--enable-gc=%{_includedir}/gc \
	--with-docdir=%{_docdir}/%{name}-doc

%ifarch ppc
%{__make} asy
%{__make} faq
%else
%{__make} all
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ifarch ppc
%{__make} install-asy \
%else
%{__make} install \
%endif
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-doc/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/syntax
%{__mv} $RPM_BUILD_ROOT%{_datadir}/{asymptote/asy.vim,vim/vimfiles/syntax}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/texmf{,-dist}

%ifnarch ppc
%{__mv} $RPM_BUILD_ROOT%{_infodir}/{asymptote/*,}
%{__rm} -rf $RPM_BUILD_ROOT%{_infodir}/asymptote
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post latex
[ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash 1>&2

%postun latex
[ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash 1>&2

%files
%defattr(644,root,root,755)
%doc README TODO BUGS
%ifnarch ppc
%{_infodir}/*.info.gz
%endif
%attr(755,root,root) %{_bindir}/asy
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/GUI
%ifnarch ppc
%{_mandir}/man1/asy.1*
%endif

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xasy
%dir %{_datadir}/%{name}/GUI
%attr(755,root,root) %{_datadir}/%{name}/GUI/xasy.py
%{_datadir}/%{name}/GUI/[!x]*.py
%ifnarch ppc
%{_mandir}/man1/xasy.1*
%endif

%ifarch ppc
# What should we do?
%else
%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files latex
%defattr(644,root,root,755)
%{_datadir}/texmf-dist/tex/latex/asymptote

%files context
%defattr(644,root,root,755)
%{_datadir}/texmf-dist/tex/context/third/asymptote/colo-asy.tex

%files -n vim-syntax-asymptote
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/syntax
