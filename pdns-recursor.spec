Summary:	Recursor for PowerDNS
Name:		pdns-recursor
Version:	3.1.4
Release:	%mkrel 2
License:	GPL
Group:		System/Servers
URL:		http://www.powerdns.com/
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
Source1:	powerdns-recursor.init
Patch:      pdns-recursor-fixbuild.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	libstdc++-devel
BuildRequires:  boost-devel
Provides:	PowerDNS-recursor
Obsoletes:	PowerDNS-recursor
Requires:	pdns
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
%patch -p0
cp %{SOURCE1} .

chmod 644 rrd/*

%build

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

%make basic_checks

%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

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
local-port=5300
local-address=127.0.0.1
trace=off
daemon=yes
quiet=on
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
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

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
