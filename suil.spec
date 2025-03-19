#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_without	gtk2	# GTK+ 2 wrappers
%bcond_without	gtk3	# GTK+ 3 wrappers
%bcond_without	qt5	# Qt5 wrappers
%bcond_without	qt6	# Qt6 wrappers

Summary:	Lightweight C library for loading and wrapping LV2 plugin UIs
Summary(pl.UTF-8):	Lekka biblioteka C do ładowania i obudowywania UI wtyczek LV2
Name:		suil
Version:	0.10.22
Release:	1
License:	ISC
Group:		Libraries
Source0:	http://download.drobilla.net/%{name}-%{version}.tar.xz
# Source0-md5:	3d4891e862a6e3659ed0b0e462ee982c
URL:		http://drobilla.net/software/suil/
%{?with_qt5:BuildRequires:	Qt5Widgets-devel >= 5.1.0}
%{?with_qt5:BuildRequires:	Qt5X11Extras-devel >= 5.1.0}
%{?with_qt6:BuildRequires:	Qt6Widgets-devel >= 6.2.0}
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.14.0}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	lv2-devel >= 1.18.4
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-sphinx_lv2_theme
BuildRequires:	sphinx-pdg
BuildRequires:	sphinxygen
%endif
Requires:	lv2 >= 1.18.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Suil is a lightweight C library for loading and wrapping LV2 plugin
UIs.

Suil makes it possible to load a UI of any toolkit in a host using any
other toolkit (assuming the toolkits are both supported by Suil).
Hosts do not need to build against or link to foreign toolkit
libraries to use UIs written with that toolkit (Suil performs its
magic at runtime using dynamically loaded modules). The API is
designed such that hosts do not need to explicitly support particular
toolkits whatsoever - if Suil supports a particular toolkit, then all
hosts that use Suil will support that toolkit "for free".

%description -l pl.UTF-8
Suil to lekka biblioteka C do ładowania i obudowywania interfejsów
użytkownika (UI) wtyczek LV2.

Suil umożliwia wczytanie UI dowolnego toolkitu do hosta
wykorzystującego dowolny inny toolkit (zakładając, że oba toolkity są
obsługiwane prez Suil). Hosty nie muszą być budowane z obsługą obcych
bibliotek toolkitów, aby można było używać UI napisanego z użyciem
danego toolkitu (Suil wykonuje całą potrzebną magię w czasie działania
przy użyciu modułów ładowanych dynamicznie). API jest zaprojektowane
tak, że hosty nie muszą jawnie obsługiwać konkretnego toolkitu - jeśli
Suil obsługuje ten toolkit, to wszystkie hosty wykorzystujące Suil
będą obsługiwały ten toolkit za darmo.

%package modules
Summary:	UI wrapper modules for suil library
Summary(pl.UTF-8):	Moduły obudowujące UI dla biblioteki suil
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_qt5:Requires:	Qt5Widgets >= 5.1.0}
%{?with_qt5:Requires:	Qt5X11Extras >= 5.1.0}
%{?with_qt6:Requires:	Qt6Widgets >= 6.2.0}
%{?with_gtk2:Requires:	gtk+2 >= 2:2.18.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.14.0}

%description modules
Dynamically loaded modules for suil library, allowing to use X11
UIs in GTK+ or Qt host, GTK+ UI in Qt host, Qt UI in GTK+ host.

%description modules -l pl.UTF-8
Dynamicznie wczytywane moduły dla biblioteki suil, pozwalające na
używanie interfejsów użytkownika X11 w hostach GTK+ lub Qt,
interfejsów GTK+ w hostach Qt oraz  interfejsów Qt w hostach GTK+.

%package devel
Summary:	Header files for suil library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki suil
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lv2-devel >= 1.18.4

%description devel
Header files for suil library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki suil.

%package apidocs
Summary:	API documentation for suil library
Summary(pl.UTF-8):	Dokumentacja API biblioteki suil
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for suil library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki suil.

%prep
%setup -q

%build
%meson \
	--default-library=shared \
	%{!?with_apidocs:-Ddocs=disabled} \
	%{!?with_gtk2:-Dgtk2=disabled} \
	%{!?with_gtk3:-Dgtk3=disabled} \
	%{!?with_qt5:-Dqt5=disabled} \
	%{!?with_qt6:-Dqt6=disabled} \
	-Dsinglehtml=disabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md
%attr(755,root,root) %{_libdir}/libsuil-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsuil-0.so.0
%dir %{_libdir}/suil-0

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11.so
%if %{with gtk2}
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11_in_gtk2.so
%endif
%if %{with gtk3}
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11_in_gtk3.so
%endif
%if %{with qt5}
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11_in_qt5.so
%endif
%if %{with qt6}
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11_in_qt6.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsuil-0.so
%{_includedir}/suil-0
%{_pkgconfigdir}/suil-0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%dir %{_docdir}/suil-0
%{_docdir}/suil-0/html
%endif
