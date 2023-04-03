#
# Conditional build:
%bcond_with	apidocs	# API documentation
%bcond_without	gtk	# GTK+ (2,3) support
%bcond_without	qt5	# Qt5 support

Summary:	Lightweight C library for loading and wrapping LV2 plugin UIs
Summary(pl.UTF-8):	Lekka biblioteka C do ładowania i obudowywania UI wtyczek LV2
Name:		suil
Version:	0.10.18
Release:	1
License:	ISC
Group:		Libraries
Source0:	http://download.drobilla.net/%{name}-%{version}.tar.xz
# Source0-md5:	4e6b74025721a8117526e6d2ebece352
URL:		http://drobilla.net/software/suil/
%{?with_qt5:BuildRequires:	Qt5Widgets-devel >= 5.1.0}
%{?with_qt5:BuildRequires:	Qt5X11Extras-devel >= 5.1.0}
%{?with_gtk:BuildRequires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.14.0}
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	lv2-devel >= 1.18.3
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	sphinx-pdg
%endif
Requires:	lv2 >= 1.18.3
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
%{?with_gtk:Requires:	gtk+2 >= 2:2.18.0}
%{?with_gtk:Requires:	gtk+3 >= 3.14.0}

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
Requires:	lv2-devel >= 1.18.3

%description devel
Header files for suil library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki suil.

%prep
%setup -q

%build
%meson build \
	--default-library=shared \
	%{!?with_apidocs:-Ddocs=disabled} \
	%{!?with_gtk:-Dgtk2=disabled} \
	%{!?with_gtk:-Dgtk3=disabled} \
	%{!?with_qt5:-Dqt5=disabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%if %{with gtk}
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11_in_gtk2.so
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11_in_gtk3.so
%endif
%if %{with qt5}
%attr(755,root,root) %{_libdir}/suil-0/libsuil_x11_in_qt5.so
%endif
%if %{with gtk} && %{with qt5}
%attr(755,root,root) %{_libdir}/suil-0/libsuil_gtk2_in_qt5.so
%attr(755,root,root) %{_libdir}/suil-0/libsuil_qt5_in_gtk2.so
%attr(755,root,root) %{_libdir}/suil-0/libsuil_qt5_in_gtk3.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsuil-0.so
%{_includedir}/suil-0
%{_pkgconfigdir}/suil-0.pc
