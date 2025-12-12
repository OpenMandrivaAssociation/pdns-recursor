Name:		pdns-recursor
Version:	5.3.1
Release:	2
Source0:	http://downloads.powerdns.com/releases/%{name}-%{version}.tar.xz
Source1:	vendor.tar.xz
Summary:	High-performance DNS recursor
URL:		https://powerdns.com/recursor/
License:	GPL-2.0
Group:		Servers
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	libtool-base
BuildRequires:	make
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(luajit)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libsodium)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd
BuildRequires:	cargo

%patchlist
pdns-recursor-boost-1.89.patch

%description
The PowerDNS Recursor is a high-performance DNS recursor with built-in scripting
capabilities. It is known to power the resolving needs of over 150 million
internet connections.

%prep
%autosetup -p1 -a1
cd rec-rust-lib/rust
mkdir .cargo
cat >.cargo/config.toml <<EOF

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
cargo generate-lockfile --offline
cd ../..

aclocal -I m4
autoconf

%conf
%configure \
	--enable-systemd \
	--enable-lto \
	--enable-dns-over-tls

%build
%make_build

%install
%make_install

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
