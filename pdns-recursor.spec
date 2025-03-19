Name:		pdns-recursor
Version:	5.2.0
Release:	1
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
Summary:	High-performance DNS recursor
URL:		https://powerdns.com/recursor/
License:	GPL-2.0
Group:		Servers
BuildSystem:	autotools
BuildOption:	--enable-systemd
BuildOption:	--enable-lto
BuildOption:	--enable-dns-over-tls
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(luajit)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libsodium)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	cargo

%description
The PowerDNS Recursor is a high-performance DNS recursor with built-in scripting
capabilities. It is known to power the resolving needs of over 150 million
internet connections.

%prep
%autosetup -p1

%install -a
mv %{buildroot}%{_sysconfdir}/recursor.yml-dist %{buildroot}%{_sysconfdir}/recursor.yml
mkdir -p %{buildroot}%{_sysusersdir}
echo 'u pdns-recursor - "PowerDNS Recursor" / %{_bindir}/nologin' >%{buildroot}%{_sysusersdir}/%{name}.conf

%files
%config %{_sysconfdir}/recursor.yml
%{_bindir}/pdns_recursor
%{_bindir}/rec_control
%{_unitdir}/pdns-recursor.service
%{_unitdir}/pdns-recursor@.service
%{_sysusersdir}/%{name}.conf
%{_mandir}/man1/pdns_recursor.1*
%{_mandir}/man1/rec_control.1*
