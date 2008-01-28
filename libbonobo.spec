# enable_gtkdoc: toggle if gtk-doc stuff should be rebuilt.
#	0 = no
#	1 = yes
%define enable_gtkdoc	1

# End of user configurable section
%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}

%define req_ORBit_version	2.9.2
%define req_libxml_version	2.4.20

%define api_version	2
%define lib_major	0
%define lib_name    %mklibname bonobo %{api_version} %{lib_major}
#gw we must keep this, the other name is taken by a gnome 1.4 package
%define develname %mklibname -d bonobo %{api_version} %lib_major

Name:		libbonobo
Summary:	Library for compound documents in GNOME
Version: 2.20.4
Release:	%mkrel 1
License:	LGPL
URL:		http://www.gnome.org/
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: bison 
BuildRequires: flex
BuildRequires: libORBit2-devel >= %{req_ORBit_version}
BuildRequires: libxml2-devel >= %{req_libxml_version}
BuildRequires: perl-XML-Parser
BuildRequires: automake1.9
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif
Requires:	%{lib_name} = %{version}
Obsoletes: bonobo-activation
Provides: bonobo-activation

%description
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package contains various needed modules and files for bonobo 2
to operate.


%package -n %{lib_name}
Summary:	Library for compound documents in GNOME
Group:		%{group}
Requires:	%{name} >= %{version}
Obsoletes:  libbonobo-activation4
Provides:	libbonobo-activation4
Provides:	libbonobo-activation

%description -n %{lib_name}
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package provides libraries to use Bonobo.


%package -n %develname
Summary:	Static libraries, include files and sample code for Bonobo 2
Group:		Development/GNOME and GTK+
# Intentional, the name libbonobo2-devel was already used for bonobo 1.0.x
Provides:	%{name}%{api_version}_x-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}
Requires:	%{name} = %{version}
Obsoletes:  libbonobo-activation4-devel
Provides:	libbonobo-activation4-devel
Provides:	libbonobo-activation-devel
Requires:	libxml2-devel >= %{req_libxml_version}
Requires:	libORBit2-devel >= %{req_ORBit_version}

%description -n %develname
Bonobo is a library that provides the necessary framework for GNOME
applications to deal with compound documents, i.e. those with a
spreadsheet and graphic embedded in a word-processing document.

This package provides the necessary development libraries and include
files to allow you to develop programs using the Bonobo document model;
it includes demonstration executables and codes as well.


%prep
%setup -q

%build

%configure2_5x \
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
rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/monikers/*.{a,la} \
  $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.{a,la} \
  $RPM_BUILD_ROOT%{_bindir}/bonobo-activation-{run-query,empty-server} \
  $RPM_BUILD_ROOT%{_libdir}/bonobo/servers/{empty,broken,plugin}.server

%clean
rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc README NEWS AUTHORS
%config(noreplace) %{_sysconfdir}/bonobo-activation
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/bonobo-activation-server
%{_datadir}/idl/*
%dir %{_libdir}/bonobo
%dir %{_libdir}/bonobo/monikers
%{_libdir}/bonobo/monikers/*.so*
%dir %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/*
%{_libdir}/bonobo-2.0
%{_libdir}/orbit-2.0/*.so*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/libbonobo-2.so.0*
%_libdir/libbonobo-activation.so.4*

%files -n %develname
%defattr(-, root, root)
%doc changes.txt TODO ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libbonobo*.so
%{_libdir}/libbonobo*.a
%attr(644,root,root) %{_libdir}/libbonobo*.la
%{_libdir}/pkgconfig/*


