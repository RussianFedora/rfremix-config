Summary:	Russian Fedora Remix firstboot configure scripts
Name:		rfremix-config
Version:	0.9.2
Release:	1%{?dist}
Epoch:		3

License:	GPLv2
Group:		System Environment/Base
URL:		http://fedoraproject.org
Source:		https://github.com/Tigro/tarballs/raw/master/rfremix-config-%{version}.tar.bz2
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


%post
# We do not want to run rfremixconf during updating for 0.9.1 (FIXME? later)
if [ $1 -eq 1 ]; then
    test -f /sbin/chkconfig && /sbin/chkconfig rfremixconf on || :
fi

%preun
if [ $1 -eq 0 ]; then
    test -f /sbin/chkconfig && /sbin/chkconfig --del rfremixconf || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc GPL README AUTHORS Changelog
%{_sysconfdir}/rc.d/init.d/rfremixconf
%attr(0755, root, root) %{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_sysconfdir}/modprobe.d/floppy-pnp.conf


%changelog
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
