%include	/usr/lib/rpm/macros.perl
Summary:	A EMail Virus Scanner for Exim MTA
Summary(pl):	Antywirusowy skaner poczty elektronicznej dla Exim MTA
Name:		exiscan
Version:	2.4
Release:	2
URL:		http://duncanthrax.net/exiscan/
Source0:	http://duncanthrax.net/exiscan/%{name}-v%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-config.patch
Patch1:		%{name}-user.patch
License:	GPL
Group:		Applications/Mail
BuildRequires:	perl-devel
BuildRequires:	perl-modules
BuildRequires:	perl-MailTools
BuildRequires:	perl-Unix-Syslog
Requires:	exim >= 3.00
# http://www.pldaniels.com/ripmime/
Requires:	ripmime
# http://world.std.com/~damned/software.html
Requires:	tnef
Prereq:		/sbin/chkconfig
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Exiscan is an email virus scanner which works together with the Exim
MTA (http://www.exim.org). It is written in Perl and designed to be
very easy to implement. Exiscan supports multithreaded unpacking and
scanning of mail, with a configurable number of processes. Exiscan has
generic support for available command line virus scanners. Exiscan can
scan inside of MS-TNEF and SMIME (signed) wrapped messages.

%description -l pl
Exiscan to antywirusowy skaner poczty dzia³aj±cy wraz z MTA Exim
(http://www.exim.org). Exiscan zosta³ napisany w Perlu oraz
zaprojektowany tak by byæ bardzo ³atwym w u¿yciu. Exiscan wspiera
wielow±tkowe rozpakowywanie i skanowanie poczty z konfigurowalnym
ograniczeniem ilo¶ci procesów. Exiscan mo¿e wspó³pracowaæ z wieloma
skanerami antywirusowymi wywo³ywanymi z lini poleceñ. Exiscan mo¿e
skanowaæ wiadomo¶ci opakowane za pomoc± MS-TNEF oraz SMIME
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

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" -a -f %{_var}/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} stop 1>&2
fi
/sbin/chkconfig --del %{name}

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL README*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,exim) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/*.cf
%attr(750,exim,root) %{_var}/spool/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT
