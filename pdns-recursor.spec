Name:		pdns-recursor
Version:	5.2.2
Release:	1
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
Source1:	vendor.tar.xz
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
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd
BuildRequires:	cargo

%description
The PowerDNS Recursor is a high-performance DNS recursor with built-in scripting
capabilities. It is known to power the resolving needs of over 150 million
internet connections.

%prep
%autosetup -p1
cd settings/rust
tar xf %{S:1}
mkdir .cargo
cat >.cargo/config.toml <<EOF

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
cargo generate-lockfile --offline
cd ../..

%conf -a
mkdir -p _OMV_rpm_build/settings/rust/.cargo
ln -s ../../../settings/rust/vendor _OMV_rpm_build/settings/rust/
cat >_OMV_rpm_build/settings/rust/.cargo/config.toml <<EOF

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

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
