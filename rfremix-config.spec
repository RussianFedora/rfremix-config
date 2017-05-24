Summary:        RFRemix configure scripts and configs
Name:           rfremix-config
Version:        26
Release:        5%{?dist}
Epoch:          3

License:        GPLv2
URL:            http://russianfedora.pro
Source:         %{name}-%{version}.tar.xz
BuildArch:      noarch

%description
This package contains some configuration files for RFRemix linux distribution.

floppy-pnp.conf - enable floppy support
clipitrc        - configure clipit (do not save history by default)


%package gnome
Summary:        RFRemix configurations for GNOME

Requires:       gnome-shell-theme-korora
Requires:       gnome-shell-extension-user-theme
Requires(post): glib2


%description gnome
This package contain configuration files for GNOME 3

org.gnome.settings-daemon.plugins.xsettings.gschema.override - set antialiasing
                  rgba
org.gnome.shell.extensions.user-theme.gschema.override - set Korora GNOME
                  Shell theme by default

%package external-repos
Summary:        External repos with well known proprietaty products

Requires:	fedora-repos

%description external-repos
This package contaion repository configs to easy setup several proprietaty
products. At this time supported:
    google-chrome
    mail.ru-cloud
    MEGAsync
    skype-stable
    slack
    virtualbox
    vk
    yandex-browser
    yandex-disk

All repos are disabled you should enable it by:

dnf config-manager --set-enabled <repo>

%prep
%setup -q


%build
# Nothing to build


%install
# make skel
install -dD %{buildroot}/etc/X11/xorg.conf.d/
install -dD %{buildroot}/etc/modprobe.d
install -dD %{buildroot}/etc/skel/.config/clipit

install -m644 floppy-pnp.conf %{buildroot}/%{_sysconfdir}/modprobe.d/
install -m644 11-evdev-trackpoint.conf %{buildroot}/%{_sysconfdir}/X11/xorg.conf.d/11-evdev-trackpoint.conf

install -dD %{buildroot}%{_datadir}/glib-2.0/schemas
install -m644 gschema.override/* \
        %{buildroot}%{_datadir}/glib-2.0/schemas/

install -m644 clipitrc %{buildroot}/etc/skel/.config/clipit/

install -dD %{buildroot}%{_datadir}/%{name}-external-repos
cp repos/*.repo %{buildroot}%{_datadir}/%{name}-external-repos

install -dD %{_sysconfdir}/yum.repos.d

%post gnome
if [ -x /usr/bin/glib-compile-schemas ]; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi


%postun gnome
if [ -x /usr/bin/glib-compile-schemas ]; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%post external-repos
if [ $1 -eq 1 ]; then
    cp %{_datadir}/%{name}-external-repos/*.repo \
        %{_sysconfdir}/yum.repos.d/
fi

%postun external-repos
if [ $1 -eq 0 ]; then
    if [ ! -f /usr/bin/yandex-disk ]; then
        rm -f %{_sysconfdir}/yum.repos.d/yandex-disk.repo
    fi

    if [ ! -f /usr/bin/yandex-browser ]; then
        rm -f %{_sysconfdir}/yum.repos.d/yandex-browser*.repo
    fi

    if [ ! -f /usr/bin/cloud ]; then
        rm -f %{_sysconfdir}/yum.repos.d/mail.ru-cloud.repo
    fi

    if [ ! -f /usr/bin/megasync ]; then
        rm -f %{_sysconfdir}/yum.repos.d/megasync.repo
    fi

    if [ ! -f /usr/bin/google-chrome ]; then
        rm -f %{_sysconfdir}/yum.repos.d/google-chrome.repo
    fi

    if [ ! -f /usr/bin/VirtualBox ]; then
        rm -f %{_sysconfdir}/yum.repos.d/virtualbox.repo
    fi

    if [ ! -f /usr/bin/skypeforlinux ]; then
        rm -f %{_sysconfdir}/yum.repos.d/skype-stable.repo
    fi

    if [ ! -f /usr/bin/slack ]; then
        rm -f %{_sysconfdir}/yum.repos.d/slack.repo
    fi

    if [ ! -f /usr/bin/vk ]; then
        rm -f %{_sysconfdir}/yum.repos.d/vk.repo
    fi

fi

%files
%license COPYING
%doc README AUTHORS Changelog
%{_sysconfdir}/modprobe.d/floppy-pnp.conf
%{_sysconfdir}/X11/xorg.conf.d/11-evdev-trackpoint.conf
%config(noreplace) %{_sysconfdir}/skel/.config/clipit/clipitrc

%files gnome
%doc README AUTHORS Changelog
%{_datadir}/glib-2.0/schemas/*.override

%files external-repos
%doc README AUTHORS Changelog
%{_datadir}/%{name}-external-repos
%dir %{_sysconfdir}/yum.repos.d



%changelog
* Wed May 24 2017 Arkady L. Shane <ashejn@russianfedora.ru> - 26-5.R
- added R: fedora-repos
- provides yum.repos.d too

* Thu May 10 2017 Arkady L. Shane <ashejn@russianfedora.ru> - 26-4.R
- drop dropbox repo
- use keyserver gpg path for VK
- update path for slack

* Wed May 10 2017 Arkady L. Shane <ashejn@russianfedora.ru> - 26-3.R
- fix typos

* Fri Mar 24 2017 Arkady L. Shane <ashejn@russianfedora.ru> - 26-2.R
- added external repo package

* Fri Mar 24 2017 Arkady L. Shane <ashejn@russianfedora.ru> - 26-1.R
- added GPaste@gnome-shell-extensions.gnome.org extension to start

* Sun Jun  5 2016 Arkady L. Shane <ashejn@russianfedora.ru> - 24-5.R
- fix setup of terminal theme

* Wed Jun  1 2016 Arkady L. Shane <ashejn@russianfedora.ru> - 24-4.R
- fix setup of dark theme for terminal

* Wed Jun  1 2016 Arkady L. Shane <ashejn@russianfedora.ru> - 24-3.R
- enable user-theme extension in GNOME Shell

* Thu Mar 24 2016 Arkady L. Shane <ashejn@russianfedora.ru> - 24-2.R
- drop quotes in schema

* Wed Mar 23 2016 Arkady L. Shane <ashejn@russianfedora.ru> - 24-1.R
- set scaling to 0.97
- set hinting to medium

* Tue Feb  2 2016 Arkady L. Shane <ashejn@russianfedora.ru> - 23-2.R
- added russianfedora override schema file

* Tue Jan 19 2016 Arkady L. Shane <ashejn@russianfedora.ru> - 23-1.R
- set Korora as default theme for GNOME Shell
- create separate package to configure GNOME

* Mon Jan 13 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 20-2.R
- added trackpoint config

* Thu Dec 26 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 20-1.R
- drop init script. All keyboard setting successfull setup without it

* Fri Jun 28 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 19-0.5.R
- Zaebalo. Fix typo

* Fri Jun 28 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 19-0.4.R
- update TOOGLE field

* Fri Jun 28 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 19-0.3.R
- read config from 00-keyboard.conf

* Fri Jun 28 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 19-0.2.R
- fix typo in script

* Wed May 29 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 19-0.1.R
- make changes for new gnome input source modifiers
- write http_caching=none into yum.conf

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

* Mon Jan 24 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 0.9.2-1
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
