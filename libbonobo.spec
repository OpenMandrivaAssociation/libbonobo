# enable_gtkdoc: toggle if gtk-doc stuff should be rebuilt.
#	0 = no
#	1 = yes
%define	enable_gtkdoc	1

# End of user configurable section
%{?_without_gtkdoc: %{expand: %%define	enable_gtkdoc 0}}
%{?_with_gtkdoc: %{expand: %%define	enable_gtkdoc 1}}

%define api_version	2
%define lib_major	0
%define lib_name	%mklibname bonobo %{api_version} %{lib_major}
%define	develname	%mklibname -d bonobo

Name:		libbonobo
Summary:	Library for compound documents in GNOME
Version:	2.32.1
Release:	3
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: automake
BuildRequires: bison 
BuildRequires: flex
%if %enable_gtkdoc
BuildRequires: gtk-doc >= 0.9
%endif
BuildRequires: intltool
BuildRequires: pkgconfig(gio-2.0) >= 2.25.7
BuildRequires: pkgconfig(glib-2.0) >= 2.25.7
BuildRequires: pkgconfig(gmodule-2.0) >= 2.0.1
BuildRequires: pkgconfig(gobject-2.0) >= 2.25.7
BuildRequires: pkgconfig(gthread-2.0) >= 2.25.7
BuildRequires: pkgconfig(libxml-2.0) >= 2.4.20
BuildRequires: pkgconfig(ORBit-2.0) >= 2.11.2
BuildRequires: pkgconfig(ORBit-CosNaming-2.0) >= 2.11.2
BuildRequires: pkgconfig(popt)
Requires:	%{lib_name} = %{version}-%{release}

%description
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package contains various needed modules and files for bonobo 2
to operate.


%package -n %{lib_name}
Summary:	Library for compound documents in GNOME
Group:		%{group}

%description -n %{lib_name}
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package provides libraries to use Bonobo.


%package -n %{develname}
Summary:	Development libraries, include files and sample code for Bonobo 2
Group:		Development/GNOME and GTK+
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d bonobo %{api_version} %lib_major}

%description -n %{develname}
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package provides the necessary development libraries and include
files to allow you to develop programs using the Bonobo document model;
it includes demonstration executables and codes as well.


%prep
%setup -q

# this is a hack for glib2.0 >= 2.31.0
sed -i -e 's/-DG_DISABLE_DEPRECATED//g' \
    ./activation-server/Makefile.*

%build
%configure2_5x \
	--disable-static \
%if %enable_gtkdoc
	--enable-gtk-doc
%endif

%make

%check
#make check

%install
rm -rf %{buildroot}
%makeinstall_std

%{find_lang} %{name}-2.0

# remove unpackaged files
find %{buildroot} -name *.la | xargs rm
rm -f %{buildroot}%{_libdir}/bonobo/servers/{empty,broken,plugin}.server


%files -f %{name}-2.0.lang
%doc README NEWS AUTHORS
%config(noreplace) %{_sysconfdir}/bonobo-activation
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/bonobo-activation-server
%dir %{_libdir}/bonobo
%dir %{_libdir}/bonobo/monikers
%dir %{_libdir}/bonobo/servers
%{_libdir}/bonobo/monikers/*.so
%{_libdir}/bonobo/servers/*
%{_libdir}/bonobo-2.0
%{_libdir}/orbit-2.0/*.so
%{_mandir}/man1/*

%files -n %{lib_name}
%{_libdir}/libbonobo-2.so.%{lib_major}*
%{_libdir}/libbonobo-activation.so.4*

%files -n %{develname}
%doc changes.txt TODO ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libbonobo*.so
%{_libdir}/pkgconfig/*
%{_datadir}/idl/*

