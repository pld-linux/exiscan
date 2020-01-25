Summary:	An EMail Virus Scanner for Exim MTA
Summary(pl.UTF-8):	Antywirusowy skaner poczty elektronicznej dla Exim MTA
Name:		exiscan
Version:	2.4
Release:	2
License:	GPL
Group:		Applications/Mail
Source0:	http://duncanthrax.net/exiscan/%{name}-v%{version}.tar.gz
# Source0-md5:	aecc3771ee9893167ee4e6a90ff12b1b
Source1:	%{name}.init
Patch0:		%{name}-config.patch
Patch1:		%{name}-user.patch
URL:		http://duncanthrax.net/exiscan/
BuildRequires:	perl-MailTools
BuildRequires:	perl-Unix-Syslog
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	exim >= 3.00
# http://www.pldaniels.com/ripmime/
Requires:	ripmime
# http://world.std.com/~damned/software.html
Requires:	tnef
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Exiscan is an email virus scanner which works together with the Exim
MTA (http://www.exim.org). It is written in Perl and designed to be
very easy to implement. Exiscan supports multithreaded unpacking and
scanning of mail, with a configurable number of processes. Exiscan has
generic support for available command line virus scanners. Exiscan can
scan inside of MS-TNEF and SMIME (signed) wrapped messages.

%description -l pl.UTF-8
Exiscan to antywirusowy skaner poczty działający wraz z MTA Exim
(http://www.exim.org). Exiscan został napisany w Perlu oraz
zaprojektowany tak by być bardzo łatwym w użyciu. Exiscan wspiera
wielowątkowe rozpakowywanie i skanowanie poczty z konfigurowalnym
ograniczeniem ilości procesów. Exiscan może współpracować z wieloma
skanerami antywirusowymi wywoływanymi z lini poleceń. Exiscan może
skanować wiadomości opakowane za pomocą MS-TNEF oraz SMIME
(podpisane).

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p0

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{mail,rc.d/init.d}}
install -d $RPM_BUILD_ROOT%{_var}/spool/%{name}/{checkqueue,virusmails}

install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install exiscan*.pl	$RPM_BUILD_ROOT%{_sbindir}/exiscan
install exiscan*.cf	$RPM_BUILD_ROOT%{_sysconfdir}/mail/exiscan.cf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service exiscan restart

%preun
if [ "$1" = "0" -a -f %{_var}/lock/subsys/%{name} ]; then
	%service exiscan stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,exim) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/*.cf
%attr(750,exim,root) %{_var}/spool/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
