Summary:	Asymptote is a powerful descriptive vector graphics language for technical drawing
Summary(hu.UTF-8):	Asymptote egy leíró vektorgrafikus nyelv technikai rajzokhoz.
Name:		asymptote
Version:	1.43
Release:	1
License:	GPL
Group:		Applications/Science
Group:		X11/Applications/Science
Source0:	http://dl.sourceforge.net/asymptote/%{name}-%{version}.src.tgz
# Source0-md5:	8f85e1d9c455700f304960a8c5f7f113
URL:		http://asymptote.sourceforge.net
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
Asymptote egy leíró vektorgrafikus nyelv technikai rajzokhoz,
hasonló a MetaPost-hoz, de kibővítve C++-szerű szintaxissal.
Asymptote még képes olyan szintű szövegszedésre is, amelyre a
LaTeX képes a tudományos szöveggel.

%package doc
Summary:	Asymptote documentation
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description doc
Asymptote documentation.

%package examples
Summary:	Asymptote examples
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Asymptote documentation.

%prep
%setup -q

%build
%configure \
	CPPFLAGS=-I/usr/include/gc \
	--disable-static \
	--enable-gc=%{_includedir}/gc \
	--with-docdir=%{_docdir}/%{name}-doc

CPPFLAGS=-I/usr/include/gc %{__make}

%install
rm -rf $RPM_BUILD_ROOT

# I don't know why need it - maybe the bad tetex configuration?
# And the solution suggested by asympote's doc doesn't work too :(
cp %{_datadir}/texmf/tex/{plain/pdfcolor/pdfcolor.tex,generic/epsf/epsf.tex,texinfo/texinfo.tex} doc
%{__make} all
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-doc/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/asy
%attr(755,root,root) %{_bindir}/xasy
%{_datadir}/%{name}
%{_datadir}/texmf/tex/latex/asymptote
%{_mandir}/man1/*
%doc README TODO BUGS

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc
