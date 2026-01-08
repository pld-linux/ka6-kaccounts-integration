#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kaccounts-integration
Summary:	Kaccounts integration
Name:		ka6-%{kaname}
Version:	25.12.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	47afc23471c9a5743612d26cbb4d0ce2
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdeclarative-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	libaccounts-glib-devel >= 1.21
BuildRequires:	libaccounts-qt6-devel >= 1.13
BuildRequires:	libsignon-qt6-devel >= 8.55
BuildRequires:	ninja
BuildRequires:	qcoro-qt6-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Administer web accounts for the sites and services across the Plasma
desktop.

%description -l pl.UTF-8
Zarządzaj kontami internetowymi w środowisku Plazmy.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
%dir %{_libdir}/qt6/qml/org/kde/kaccounts
%{_libdir}/qt6/qml/org/kde/kaccounts/libkaccountsdeclarativeplugin.so
%{_libdir}/qt6/qml/org/kde/kaccounts/qmldir
%dir %{_libdir}/qt6/plugins/kaccounts
%dir %{_libdir}/qt6/plugins/kaccounts/daemonplugins
%{_libdir}/qt6/plugins/kaccounts/daemonplugins/kaccounts_kio_webdav_plugin.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_kaccounts.so
%{_desktopdir}/kcm_kaccounts.desktop
%ghost %{_libdir}/libkaccounts6.so.2
%{_libdir}/libkaccounts6.so.*.*
%{_libdir}/qt6/plugins/kf6/kded/kded_accounts.so
%{_libdir}/qt6/qml/org/kde/kaccounts/kaccountsdeclarativeplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/kaccounts/kde-qmlmodule.version
%{_datadir}/qlogging-categories6/kaccounts.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KAccounts6
%{_libdir}/cmake/KAccounts6
%{_libdir}/libkaccounts6.so
