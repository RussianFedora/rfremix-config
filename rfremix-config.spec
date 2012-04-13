Summary:	Russian Fedora Remix firstboot configure scripts
Name:		rfremix-config
Version:	16
Release:	1%{?dist}
Epoch:		3

License:	GPLv2
Group:		System Environment/Base
URL:		http://russianfedora.ru
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Provides:	russianfedora-config
Provides:	russianfedoraremix-config
Obsoletes:	russianfedora-config
Obsoletes:	russianfedoraremix-config
Obsoletes:	tedora-config

Requires(post):	chkconfig


%description
These are some scripts to configure Russian Fedora Remix at
the first boot.

Also package contains some configuration files for swhitching
keyboard layout in KDE, GNOME and others.


%prep
%setup -q


%build
# Nothing to build


%install
rm -rf %{buildroot}

# Install rfremixconf
install -d -m 755 %{buildroot}/etc/rc.d/init.d
install -m 755 rfremixconf.init %{buildroot}/etc/rc.d/init.d/rfremixconf

# make skel
install -dD %{buildroot}/etc/X11/xinit/xinitrc.d
install -dD %{buildroot}/etc/modprobe.d

# Configure layout switcher in X
install -m755 10-set-layout-switcher-kbd-combination.sh \
    %{buildroot}/%{_sysconfdir}/X11/xinit/xinitrc.d/

install -m644 floppy-pnp.conf %{buildroot}/%{_sysconfdir}/modprobe.d/

install -dD %{buildroot}%{_datadir}/glib-2.0/schemas
install -m644 gschema.override/* \
	%{buildroot}%{_datadir}/glib-2.0/schemas/


%post
# We do not want to run rfremixconf during updating for 0.9.1 (FIXME? later)
if [ $1 -eq 1 ]; then
    test -f /sbin/chkconfig && /sbin/chkconfig rfremixconf on || :
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%preun
if [ $1 -eq 0 ]; then
    test -f /sbin/chkconfig && /sbin/chkconfig --del rfremixconf || :
fi


%postun
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc GPL README AUTHORS Changelog
%{_sysconfdir}/rc.d/init.d/rfremixconf
%attr(0755, root, root) %{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_sysconfdir}/modprobe.d/floppy-pnp.conf
%{_datadir}/glib-2.0/schemas/*.override


%changelog
* Mon Mar 26 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 16-1.R
- drop Sans font by default
- drop Slight by default

* Tue May 17 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 15.1-1
- drop restricted schemas
- drop restricted rules from rfremixconf
- apply rule 'menus-have-icons'

* Fri Apr 22 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 15-0.1
- bump version. One for distribution
- change smolt config to detect rfremix

* Fri Apr  8 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 0.10.0-2
- added glib-compile-schemas

* Fri Apr  8 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 0.10.0-1
- override font. Sans 10 by default
- override hinting. Slight by default
- override antialiasing. Rgba by default
- set Sans Bold 11 as default metacity font

* Mon Jan 21 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 0.9.2-1
- attach floppy in modprobe.d
- do not start rfremixconf service after update from 0.9.1

* Sat Oct 30 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.9.1-4
- added R(post): chkconfig

* Sat Oct 30 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.9.1-3
- always enable script after install

* Wed Sep 29 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.9.1-2
- bump epoch to update from RFRemix 13.1

* Thu Sep 23 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.9.1-1
- update to 0.9.1
- drop kxkbrc

* Mon Mar 15 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.9-0.1
- split rfremix-config from rfremix-release
- bump epoch
