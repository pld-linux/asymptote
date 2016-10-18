Summary:	Asymptote is a powerful descriptive vector graphics language for technical drawing
Summary(hu.UTF-8):	Asymptote egy leíró vektorgrafikus nyelv technikai rajzokhoz
Summary(pl.UTF-8):	Język opisu grafiki wektorowej do rysunków technicznych
Name:		asymptote
Version:	2.35
Release:	5
License:	GPL v3
Group:		Applications/Science
Source0:	http://downloads.sourceforge.net/asymptote/%{name}-%{version}.src.tgz
# Source0-md5:	199e971792072527bd0cb1583d8ef3fb
Patch0:		%{name}-memrchr.patch
Patch1:		gsl2.patch
URL:		http://asymptote.sourceforge.net/
#BuildRequires:	Mesa-libglapi-devel
BuildRequires:	autoconf
BuildRequires:	fftw3-devel
BuildRequires:	gc-devel >= 7.0
BuildRequires:	gc-c++-devel >= 7.0
BuildRequires:	ghostscript
BuildRequires:	gsl-devel >= 1.7
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	texinfo-texi2dvi
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-ams
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-ams
#BuildRequires:	texlive-tex-babel
BuildRequires:	zlib-devel
Suggests:	ImageMagick-coder-dot
Suggests:	ImageMagick-coder-jpeg
Suggests:	ImageMagick-coder-png
# e.g. "label" command needs latex
Suggests:	texlive-latex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define texmfdist %{_datadir}/texmf-dist

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
Requires:	python-tkinter

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
Requires(post,postun):	%{_bindir}/texhash
Requires:	texlive-context

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
%patch1 -p1

%build
%{__autoheader}
%{__autoconf}
%configure \
	--enable-gc \
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
%{__mv} $RPM_BUILD_ROOT%{texmfdist}/tex/context/{third,}/asymptote
%{__rm} -r $RPM_BUILD_ROOT%{texmfdist}/tex/context/third

%ifnarch ppc
%{__mv} $RPM_BUILD_ROOT%{_infodir}/{asymptote/*,}
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}/asymptote
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post latex
[ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash 1>&2

%postun latex
[ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash 1>&2

%files
%defattr(644,root,root,755)
%doc README TODO BUGS
%ifnarch ppc
%{_infodir}/*.info*
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
%{_datadir}/%{name}/GUI/xasy2asy.py
%{_datadir}/%{name}/GUI/xasyActions.py
%{_datadir}/%{name}/GUI/xasyBezierEditor.py
%{_datadir}/%{name}/GUI/xasyCodeEditor.py
%{_datadir}/%{name}/GUI/xasyColorPicker.py
%{_datadir}/%{name}/GUI/xasyFile.py
%{_datadir}/%{name}/GUI/xasyGUIIcons.py
%{_datadir}/%{name}/GUI/xasyMainWin.py
%{_datadir}/%{name}/GUI/xasyOptions.py
%{_datadir}/%{name}/GUI/xasyOptionsDialog.py
%{_datadir}/%{name}/GUI/xasyVersion.py
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
%{texmfdist}/tex/latex/asymptote

%files context
%defattr(644,root,root,755)
# should be in texlive.spec
%dir %{texmfdist}/tex/context
%{texmfdist}/tex/context/asymptote

%files -n vim-syntax-asymptote
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/syntax
