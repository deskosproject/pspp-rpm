Name:           pspp
Version:        0.10.1
Release:        1%{?dist}
Summary:        A program for statistical analysis of sampled data
Group:          Applications/Engineering
License:        GPLv3+
URL:            https://www.gnu.org/software/pspp/
VCS:            scm:git:git://git.savannah.gnu.org/pspp.git
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig
BuildRequires:  plotutils-devel, ncurses-devel, readline-devel
BuildRequires:  gsl-devel >= 1.11-2
BuildRequires:  postgresql-devel
BuildRequires:  glade3-libgladeui-devel, libglade2-devel
BuildRequires:  gettext, desktop-file-utils
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:	autoconf automake libtool gettext-devel texinfo libxml2
BuildRequires:	gtksourceview3-devel
Provides:       bundled(gnulib)
Requires:	hicolor-icon-theme
Requires(post): info
Requires(preun): info


%description
PSPP is a program for statistical analysis of sampled data. It
interprets commands in the SPSS language and produces tabular
output in ASCII, PostScript, or HTML format.

PSPP development is ongoing. It already supports a large subset
of SPSS's transformation language. Its statistical procedure
support is currently limited, but growing.


%prep
%setup -q


%build
autoreconf -ifv
%configure CFLAGS="${CFLAGS:-%optflags} -fgnu89-inline" \
    --disable-static --disable-rpath
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Install docs
mkdir -p %{buildroot}%{_pkgdocdir}
cp -p AUTHORS NEWS ONEWS README THANKS %{buildroot}%{_pkgdocdir}
# don't own /usr/share/info/dir
rm %{buildroot}%{_infodir}/dir

# don't lala
find %{buildroot}%{_libdir}/ \
   -name \*.la -delete

# desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/pspp.desktop

# localization
%find_lang %{name}

# clean up some stuff
rm -f %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache


%check
make check


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
	/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%preun
if [ $1 = 0 ] ; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%files -f %{name}.lang
%license COPYING
%{_bindir}/pspp
%{_bindir}/psppire
%{_bindir}/pspp-convert
%{_bindir}/pspp-dump-sav
%{_infodir}/pspp*
%{_libdir}/%{name}/
%{_datadir}/appdata/pspp.appdata.xml
%{_datadir}/applications/pspp.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%{_datadir}/icons/hicolor/scalable/apps/pspp.svg
%{_datadir}/pspp/
%{_pkgdocdir}/
%{_mandir}/man1/pspp.1.*
%{_mandir}/man1/psppire.1.*
%{_mandir}/man1/pspp-convert.1.*
%{_mandir}/man1/pspp-dump-sav.*


%changelog
* Fri Apr  8 2016 Peter Lemenkov <lemenkov@gmail.com> - 0.10.1-1
- Ver. 0.10.1
- Switched to GTK3

* Mon Feb 22 2016 Orion Poplawski <orion@cora.nwra.com> - 0.8.5-4
- Rebuild for gsl 2.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Orion Poplawski <orion@cora.nwra.com> - 0.8.5-2
- Fix documentation install

* Sun Jun 21 2015 Peter Lemenkov <lemenkov@gmail.com> - 0.8.5-1
- Ver. 0.8.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Nov 08 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.8.4-1
- Ver. 0.8.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 10 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.8.3-1
- Ver. 0.8.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.8.2-1
- Ver. 0.8.2

* Tue Sep 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.8.1-1
- Ver. 0.8.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.8.0-1
- Ver. 0.8.0

* Sun Feb 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.7.9-5
- Fixed FTBFS in Rawhide / Fedora 19 (see rhbz #914398)
- Added provides(gnulib) (see rhbz #821785)
- Added accidentally removed pspp docs (see rhbz #822610)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.9-2
- Drop useless patch

* Sun Apr 15 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.7.9-1
- Ver. 0.7.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.7.8-1
- Ver. 0.7.8

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.6.2-5
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.6.2-3
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Peter Lemenkov <lemenkov@gmail.com> 0.6.2-2
- Rebuild (fixes ftbfs rhbz #599955)

* Fri Oct 16 2009 Peter Lemenkov <lemenkov@gmail.com> 0.6.2-1
- Ver. 0.6.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Matěj Cepl <mcepl@redhat.com> - 0.6.1-3
- Make .so symlink to versioned libraries -- shouldn't be needed
  but helps to fix bug 471180

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 28 2008 Matěj Cepl <mcepl@redhat.com> 0.6.1-1
- New upstream release.
- Added home made logo.
- Fix file permissions.

* Wed Nov 12 2008 Matěj Cepl <mcepl@redhat.com> - 0.6.0-9
- Fix in the %%preun script -- install-info wants only .info file
  as an argument.

* Thu Sep 25 2008 Matěj Cepl <mcepl@redhat.com> - 0.6.0-8
- Fix wrong CFLAGS -- add -fgnu89-inline

* Mon Jul 07 2008 Matej Cepl <mcepl@redhat.com> 0.6.0-7
- Fix BuildRequires.

* Wed Jun 18 2008 Matej Cepl <mcepl@redhat.com> 0.6.0-6
- Bug 451006 has been resolved, so we don't have to munge CFLAGS
  anymore.

* Sat Jun 14 2008 Matěj Cepl <mcepl@redhat.com> 0.6.0-5
- Approved version with fixed duplicate %%{_sysconfdir}/pspp

* Fri Jun 13 2008 Matěj Cepl <mcepl@redhat.com> 0.6.0-4
- Second wave of Package Review -- .desktop file
- Mysterious libraries eliminated

* Thu Jun 12 2008 Matěj Cepl <mcepl@redhat.com> 0.6.0-3
- First wave of Package Review nitpicking -- added %%doc and fixed Texinfo
  handling.

* Thu Jun 12 2008 Matěj Cepl <mcepl@redhat.com> 0.6.0-2
- Upstream release, this build is to be put into the package review.

* Tue Apr 22 2008 Matěj Cepl <mcepl@redhat.com> 0.6.0-0.1.pre2
- Upstream pre-release.

* Mon Apr 23 2007 Matej Cepl <mcepl@redhat.com> - 0.4.0-1
- The first experimental package of PSPP for Fedora.
