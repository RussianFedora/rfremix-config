Summary:        RFRemix configure scripts and configs
Name:           rfremix-config
Version:        18
Release:        0.7%{?dist}
Epoch:          3

License:        GPLv2
Group:          System Environment/Base
URL:            http://russianfedora.ru
Source:         %{name}-%{version}.tar.bz2
BuildArch:      noarch

Requires(post): chkconfig


%description
This package contains some configuration files for RFRemix linux distribution.

rfremixconf     - configuration script run at the first boot
                  it configure keyboard layouts for console, GNOME and MATE
floppy-pnp.conf - enable floppy support
clipitrc        - configure clipit (do not save history by default)

org.gnome.settings-daemon.plugins.xsettings.gschema.override - set antialiasing
                  rgba

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
install -dD %{buildroot}/etc/skel/.config/clipit

# Configure layout switcher in X
#install -m755 10-set-layout-switcher-kbd-combination.sh \
#    %{buildroot}/%{_sysconfdir}/X11/xinit/xinitrc.d/

install -m644 floppy-pnp.conf %{buildroot}/%{_sysconfdir}/modprobe.d/

install -dD %{buildroot}%{_datadir}/glib-2.0/schemas
install -m644 gschema.override/* \
        %{buildroot}%{_datadir}/glib-2.0/schemas/

install -m644 clipitrc %{buildroot}/etc/skel/.config/clipit/

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


%files
%defattr(-,root,root,-)
%doc GPL README AUTHORS Changelog
%{_sysconfdir}/rc.d/init.d/rfremixconf
#%attr(0755, root, root) %{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_sysconfdir}/modprobe.d/floppy-pnp.conf
%config(noreplace) %{_sysconfdir}/skel/.config/clipit/clipitrc
%{_datadir}/glib-2.0/schemas/*.override


%changelog
* Mon Dec 24 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 18-0.7.R
- drop yum cron file. Optional functionality added to firstboot (rf#1146)
- clean up spec

* Mon Dec 24 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 18-0.6.R
- added con script to update yum cache as they do it in dnf

* Thu Nov 29 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 18-0.5.R
- added new switches

* Tue Nov 13 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 18-0.4.R
- added cliptit config (used in GNOME by default in RFRemix)

* Sun Nov 11 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 18-0.3.R
- always set-x11-keymap

* Sat Nov 10 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 18-0.2.R
- fix mate paths

* Thu Nov  8 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 18-0.1.R
- rewrite init script

* Thu Apr 12 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 17-3.R
- use rgba instead of grayscale

* Thu Apr 12 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 17-2.R
- do not install schemas

* Sun Feb 12 2012 Arkady L. Shane <ashejn@yandex-team.ru> - 17-1.R
- rebuilt

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
