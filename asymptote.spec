#
# Conditional build:
%bcond_without	doc		# do not build and package API docs
#
%ifarch ppc %{ix86}
%undefine	with_doc
%endif
# TODO: OpenImageIO? (--enable-openimageio)
Summary:	Asymptote is a powerful descriptive vector graphics language for technical drawing
Summary(hu.UTF-8):	Asymptote egy leíró vektorgrafikus nyelv technikai rajzokhoz
Summary(pl.UTF-8):	Język opisu grafiki wektorowej do rysunków technicznych
Name:		asymptote
Version:	2.59
Release:	3
# uses GPL libraries (gsl, readline), so final license is GPL
License:	GPL v3+ (LGPL v3+ code)
Group:		Applications/Science
Source0:	http://downloads.sourceforge.net/asymptote/%{name}-%{version}.src.tgz
# Source0-md5:	d43d86b6e80faa7364ab57a6161ac1d0
Patch0:		%{name}-memrchr.patch
Patch1:		%{name}-info.patch
URL:		http://asymptote.sourceforge.net/
BuildRequires:	GLM
BuildRequires:	Mesa-libOSMesa-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	bison
BuildRequires:	fftw3-devel >= 3
BuildRequires:	flex
BuildRequires:	gc-c++-devel >= 8.0.4
BuildRequires:	gc-devel >= 8.0.4
BuildRequires:	ghostscript
BuildRequires:	gsl-devel >= 1.7
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	ncurses-devel
BuildRequires:	python >= 2
BuildRequires:	readline-devel >= 4.3
BuildRequires:	rpm-pythonprov
BuildRequires:	texinfo
BuildRequires:	texinfo-texi2dvi >= 6.7
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
Summary(pl.UTF-8):	Makra kolorów ConTeXta
Group:		Applications/Publishing/TeX
Requires(post,postun):	%{_bindir}/texhash
Requires:	texlive-context

%description context
ConTeXt color macros.

%description context -l pl.UTF-8
Makra kolorów ConTeXta.

%package -n vim-syntax-asymptote
Summary:	Vim syntax file to asy-files
Summary(hu.UTF-8):	Vim syntax fájl asy fájlokhoz
Summary(pl.UTF-8):	Plik składni Vima dla plików asy
Group:		Applications/Editors/Vim

%description -n vim-syntax-asymptote
Vim syntax file to asy files.

%description -n vim-syntax-asymptote -l hu.UTF-8
Vim syntax fájl asy fájlokhoz.

%description -n vim-syntax-asymptote -l pl.UTF-8
Plik składni Vima dla plików asy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%{__autoheader}
%configure \
	--enable-gc=system \
	--enable-offscreen \
	--with-docdir=%{_docdir}/%{name}-doc

%if %{with doc}
%{__make} all
%else
%{__make} asy
%{__make} faq
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with doc}
%{__make} install \
%else
%{__make} install-asy \
%endif
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-doc/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/syntax
%{__mv} $RPM_BUILD_ROOT%{_datadir}/asymptote/*.vim $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/syntax
%{__mv} $RPM_BUILD_ROOT%{_datadir}/texmf{,-dist}
%{__mv} $RPM_BUILD_ROOT%{texmfdist}/tex/context/{third,}/asymptote
%{__rm} -r $RPM_BUILD_ROOT%{texmfdist}/tex/context/third

%if %{with doc}
%{__mv} $RPM_BUILD_ROOT%{_infodir}/{asymptote/*.info,}
rmdir $RPM_BUILD_ROOT%{_infodir}/asymptote
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
%doc BUGS ChangeLog README ReleaseNotes TODO
%attr(755,root,root) %{_bindir}/asy
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.asy
%{_datadir}/%{name}/asymptote.py
%{_datadir}/%{name}/nopapersize.ps
%{_datadir}/%{name}/reload.js
# to emacs package?
%{_datadir}/%{name}/asy*.el
# kate package?
%{_datadir}/%{name}/asy-kate.sh
%{_datadir}/asymptote/shaders
%{_datadir}/asymptote/webgl
%if %{with doc}
%{_mandir}/man1/asy.1*
%{_infodir}/asy-faq.info*
%{_infodir}/asymptote.info*
%endif

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xasy
%dir %{_datadir}/%{name}/GUI
%attr(755,root,root) %{_datadir}/%{name}/GUI/xasy.py
%{_datadir}/%{name}/GUI/[!x]*.py
%{_datadir}/asymptote/GUI/xasy2asy.py
%{_datadir}/asymptote/GUI/xasyArgs.py
%{_datadir}/asymptote/GUI/xasyBezierInterface.py
%{_datadir}/asymptote/GUI/xasyFile.py
%{_datadir}/asymptote/GUI/xasyOptions.py
%{_datadir}/asymptote/GUI/xasyStrings.py
%{_datadir}/asymptote/GUI/xasySvg.py
%{_datadir}/asymptote/GUI/xasyTransform.py
%{_datadir}/asymptote/GUI/xasyUtils.py
%{_datadir}/asymptote/GUI/xasyValidator.py
%{_datadir}/asymptote/GUI/xasyVersion.py
%dir %{_datadir}/asymptote/GUI/configs
%{_datadir}/asymptote/GUI/configs/xasyconfig.cson
%{_datadir}/asymptote/GUI/configs/xasykeymap.cson
%dir %{_datadir}/asymptote/GUI/pyUIClass
%{_datadir}/asymptote/GUI/pyUIClass/custMatTransform.py
%{_datadir}/asymptote/GUI/pyUIClass/labelTextEditor.py
%{_datadir}/asymptote/GUI/pyUIClass/setCustomAnchor.py
%{_datadir}/asymptote/GUI/pyUIClass/widg_addLabel.py
%{_datadir}/asymptote/GUI/pyUIClass/widg_addPolyOpt.py
%{_datadir}/asymptote/GUI/pyUIClass/widg_editBezier.py
%{_datadir}/asymptote/GUI/pyUIClass/widgetPointEditor.py
%{_datadir}/asymptote/GUI/pyUIClass/window1.py
%{_datadir}/asymptote/GUI/res
%if %{with doc}
%{_mandir}/man1/xasy.1*
%endif

%if %{with doc}
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
%{texmfdist}/tex/context/asymptote

%files -n vim-syntax-asymptote
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/syntax/asy.vim
%{_datadir}/vim/vimfiles/syntax/asy_filetype.vim
