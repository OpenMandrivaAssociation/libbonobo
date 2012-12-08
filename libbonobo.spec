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
%define develname	%mklibname -d bonobo

Name:		libbonobo
Summary:	Library for compound documents in GNOME
Version:	2.32.1
Release:	4
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
%endif
BuildRequires:	intltool
BuildRequires:	pkgconfig(gio-2.0) >= 2.25.7
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.7
BuildRequires:	pkgconfig(gmodule-2.0) >= 2.0.1
BuildRequires:	pkgconfig(gobject-2.0) >= 2.25.7
BuildRequires:	pkgconfig(gthread-2.0) >= 2.25.7
BuildRequires:	pkgconfig(libxml-2.0) >= 2.4.20
BuildRequires:	pkgconfig(ORBit-2.0) >= 2.11.2
BuildRequires:	pkgconfig(ORBit-CosNaming-2.0) >= 2.11.2
BuildRequires:	pkgconfig(popt)
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
Obsoletes:	%{mklibname -d bonobo 2 0} < 2.32.1-4

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
%makeinstall_std

%find_lang %{name}-2.0

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



%changelog
* Tue Nov 15 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.32.1-3
+ Revision: 730746
- rebuild
  spec cleanup
  removed defattr
  removed .la files
  disabled static build
  moved idl folder to devel pkg, allows main pkg to be dropped from devel req
  added use of lib_major macro in lib pkg
  removed obsolete scriptlets for ldconfig
  added workaround for glib2.0 >= 2.31.0
  removed old obsoletes & provides
  removed reqs for devel pkgs in the devel pkg
  corrected summary for devel pkg
  removed req by lib pkg for main pkg, removes dep loop
  updated BRs to pkgconfig providesA
  removed use of mkrel
  dropped api & major from devel pkg, old libbonobo is long retired

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.32.1-2
+ Revision: 662348
- mass rebuild

* Mon Apr 04 2011 Götz Waschk <waschk@mandriva.org> 2.32.1-1
+ Revision: 650232
- new version

* Wed Dec 22 2010 Funda Wang <fwang@mandriva.org> 2.32.0-2mdv2011.0
+ Revision: 623766
- add popt for popt.h

* Sun Sep 26 2010 Götz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581132
- update to new version 2.32.0

* Sun Aug 29 2010 Götz Waschk <waschk@mandriva.org> 2.31.91-1mdv2011.0
+ Revision: 574133
- update to new version 2.31.91

* Tue Mar 30 2010 Götz Waschk <waschk@mandriva.org> 2.24.3-1mdv2010.1
+ Revision: 529642
- update to new version 2.24.3

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.24.2-2mdv2010.1
+ Revision: 520905
- fix deps
- rebuilt for 2010.1

* Wed Sep 23 2009 Götz Waschk <waschk@mandriva.org> 2.24.2-1mdv2010.0
+ Revision: 447640
- update to new version 2.24.2

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.24.1-2mdv2010.0
+ Revision: 425518
- rebuild

* Fri Mar 06 2009 Götz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 349817
- update to new version 2.24.1

* Mon Sep 22 2008 Götz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 286815
- new version

* Tue Aug 19 2008 Götz Waschk <waschk@mandriva.org> 2.23.1-1mdv2009.0
+ Revision: 273737
- new version

* Thu Jul 03 2008 Götz Waschk <waschk@mandriva.org> 2.23.0-1mdv2009.0
+ Revision: 230991
- fix buildrequires
- new version
- update license

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.22.0-3mdv2009.0
+ Revision: 222506
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 2.22.0-2mdv2008.1
+ Revision: 189662
- Fix groups

* Mon Mar 10 2008 Götz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 183616
- new version

* Tue Jan 29 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159999
- new version

* Mon Jan 28 2008 Götz Waschk <waschk@mandriva.org> 2.20.4-1mdv2008.1
+ Revision: 159179
- new version

* Sun Dec 23 2007 Götz Waschk <waschk@mandriva.org> 2.20.3-1mdv2008.1
+ Revision: 137343
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Götz Waschk <waschk@mandriva.org> 2.20.2-1mdv2008.1
+ Revision: 117826
- new version

  + Frederic Crozat <fcrozat@mandriva.com>
    - move test to check section (but still disabled)
    - remove killall workaround, no longer needed

* Mon Oct 15 2007 Götz Waschk <waschk@mandriva.org> 2.20.1-1mdv2008.1
+ Revision: 98395
- new version

* Mon Sep 17 2007 Götz Waschk <waschk@mandriva.org> 2.20.0-1mdv2008.0
+ Revision: 89097
- new version

* Mon Jul 30 2007 Götz Waschk <waschk@mandriva.org> 2.19.6-1mdv2008.0
+ Revision: 56555
- new version

* Tue Jun 19 2007 Götz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 41395
- new version


* Mon Mar 12 2007 Götz Waschk <waschk@mandriva.org> 2.18.0-1mdv2007.1
+ Revision: 141803
- new version

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 2.17.92-1mdv2007.1
+ Revision: 125965
- new version

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 2.17.91-2mdv2007.1
+ Revision: 125866
- rebuild for pkgconfig provides

* Mon Feb 12 2007 Götz Waschk <waschk@mandriva.org> 2.17.91-1mdv2007.1
+ Revision: 119042
- new version

* Mon Jan 22 2007 Götz Waschk <waschk@mandriva.org> 2.17.90-1mdv2007.1
+ Revision: 112091
- Import libbonobo

* Mon Jan 22 2007 Götz Waschk <waschk@mandriva.org> 2.17.90-1mdv2007.1
- New version 2.17.90

* Tue Sep 05 2006 Götz Waschk <waschk@mandriva.org> 2.16.0-1mdv2007.0
- New release 2.16.0

* Tue Aug 15 2006 Götz Waschk <waschk@mandriva.org> 2.15.3-1mdv2007.0
- New release 2.15.3

* Wed Aug 09 2006 Götz Waschk <waschk@mandriva.org> 2.15.2-1mdv2007.0
- New release 2.15.2

* Thu Jul 13 2006 G�tz Waschk <waschk@mandriva.org> 2.15.0-1mdv2007.0
- drop patch
- New release 2.15.0
- Disable check, tests are broken ATM

* Wed Jul 12 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.0-2mdv2007.0
- Patch0 (CVS): add API from gnome-vfs for mimetype (needed until new
  version of gnome-vfs is released to keep stable ABI/API)

* Tue Apr 11 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.0-1mdk
- Release 2.14.0
- enable parallel build and tests

* Thu Feb 23 2006 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-3mdk
- Use mkrel
- fix build

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.10.1-2mdk
- Rebuild

* Tue Aug 23 2005 Götz Waschk <waschk@mandriva.org> 2.10.1-1mdk
- New release 2.10.1

* Thu Jul 07 2005 G�tz Waschk <waschk@mandriva.org> 2.10.0-1mdk
- New release 2.10.0

* Fri Feb 25 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.8.1-2mdk
- rebuild to sync up with x86_64 tree and current cooker env, aka no
  more indent in orbit-idl

* Sat Feb 05 2005 G�tz Waschk <waschk@linux-mandrake.com> 2.8.1-1mdk
- enable gtk-doc
- New release 2.8.1

* Tue Oct 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.0-1mdk
- New release 2.8.0
- Remove patch0 (merged upstream)

* Fri Oct 01 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-2mdk
- Patch0 (CVS): Fix server registration

* Tue Jun 01 2004 G�tz Waschk <waschk@linux-mandrake.com> 2.6.2-1mdk
- reenable libtoolize
- New release 2.6.2

* Fri May 28 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.6.1-1mdk
- New release 2.6.1

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-2mdk
- Fix Buildrequires

* Sat Apr 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-1mdk
- Release 2.6.0 (with Goetz help)

