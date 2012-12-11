Summary:	Recursor for PowerDNS
Name:		pdns-recursor
Version:	3.3
Release:	%mkrel 1
License:	GPLv2
Group:		System/Servers
URL:		http://www.powerdns.com/
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
Source1:	powerdns-recursor.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	libstdc++-devel
BuildRequires:  boost-devel
BuildRequires:  lua-devel
Provides:	PowerDNS-recursor
Obsoletes:	PowerDNS-recursor
Requires:	pdns
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
With a small codebase, the PowerDNS Recursor is an advanced recursor currently
serving the DNS resolving needs of over 2 million Internet connections. Besides
high performance (using kqueue or epoll, over 15 thousand qps on commodity
hardware), it provides advanced anti-spoofing measures. In addition, the
program caches server performance and timeouts, making it both network and user
friendly. It also has built-in hooks for making graphs with rrdtool, providing
insight into nameserver performance.

%prep

%setup -q -n %{name}-%{version}

cp %{SOURCE1} .

chmod 644 rrd/*

%build
%serverbuild

export OPTFLAGS=""
export LUA="1"
export LUA_CPPFLAGS_CONFIG="-I%{_includedir}"
export LUA_LIBS_CONFIG="-L%{_libdir} -llua -lm"

%make basic_checks

%make

%install
rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/powerdns
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}/var/run/powerdns

install -m0755 pdns_recursor %{buildroot}%{_sbindir}/
install -m0755 rec_control %{buildroot}%{_bindir}/
install -m0644 pdns_recursor.1 %{buildroot}%{_mandir}/man1
install -m0644 rec_control.1 %{buildroot}%{_mandir}/man1

%{buildroot}%{_sbindir}/pdns_recursor --config >  %{buildroot}%{_sysconfdir}/powerdns/recursor.conf

cat >> %{buildroot}%{_sysconfdir}/powerdns/recursor.conf << EOF
socket-dir=/var/run/powerdns/
soa-minimum-ttl=0
soa-serial-offset=0
aaaa-additional-processing=off
local-port=53
local-address=127.0.0.1
trace=off
daemon=yes
quiet=on
setgid=powerdns
setuid=powerdns
EOF

install -m0755 powerdns-recursor.init %{buildroot}%{_initrddir}/powerdns-recursor

%pre
%_pre_useradd powerdns /var/lib/powerdns /bin/false

%postun
%_postun_userdel powerdns

%post
%_post_service powerdns-recursor

%preun
%_preun_service powerdns-recursor

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README rrd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/powerdns/recursor.conf
%attr(0755,root,root) %{_initrddir}/powerdns-recursor
%attr(0755,root,root) %{_bindir}/rec_control
%attr(0755,root,root) %{_sbindir}/pdns_recursor
%attr(0755,powerdns,powerdns) %dir /var/run/powerdns
%attr(0644,root,root) %{_mandir}/man1/pdns_recursor.1*
%attr(0644,root,root) %{_mandir}/man1/rec_control.1*


%changelog
* Tue Apr 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.3-1mdv2011.0
+ Revision: 650717
- 3.3

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 3.2-2mdv2011.0
+ Revision: 614491
- the mass rebuild of 2010.1 packages

* Sat Mar 27 2010 Michael Scherer <misc@mandriva.org> 3.2-1mdv2010.1
+ Revision: 528262
- update to 3.2
- remove first patch, do not apply anymore ( code completly changed, and still build )
- remove second patch, not needed ( compile fine without it )

* Wed Jan 06 2010 Michael Scherer <misc@mandriva.org> 3.1.7.2-1mdv2010.1
+ Revision: 486754
- update to 3.1.7.2, fix security issue

* Tue Aug 04 2009 Oden Eriksson <oeriksson@mandriva.com> 3.1.7.1-1mdv2010.0
+ Revision: 409378
- 3.1.7.1
- drop the boost patch, it's implemented upstream

* Sat Sep 13 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.7-2mdv2009.0
+ Revision: 284545
- added a gcc43 patch from gentoo (P1)
- added P2 to fix build against latest boost
- fix #40099 (pdns-recursor init file (/etc/init.d/powerdns-recursor) cannot start when configured for low ports)

* Thu Jun 26 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.7-1mdv2009.0
+ Revision: 229241
- 3.1.7

* Thu May 08 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.6-1mdv2009.0
+ Revision: 204497
- 3.1.6

* Mon Mar 31 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.5-1mdv2008.1
+ Revision: 191268
- 3.1.5

* Sun Mar 23 2008 Oden Eriksson <oeriksson@mandriva.com> 3.1.5-0.rc1.1mdv2008.1
+ Revision: 189575
- 3.1.5-rc1 (3.1.4 won't build on 2008.1)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Michael Scherer <misc@mandriva.org>
    - fix default config and fix build

* Mon Apr 23 2007 Oden Eriksson <oeriksson@mandriva.com> 3.1.4-1mdv2008.0
+ Revision: 17246
- 3.1.4


* Tue Jun 27 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.2-1mdv2007.0
- 3.1.2

* Wed May 24 2006 Oden Eriksson <oeriksson@mandriva.com> 3.1.1-1mdk
- initial Mandriva package

