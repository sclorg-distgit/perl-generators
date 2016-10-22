%{?scl:%scl_package perl-generators}

Name:           %{?scl_prefix}perl-generators
Version:        1.10
Release:        2%{?dist}
Summary:        RPM Perl dependencies generators
Group:          Development/Libraries
License:        GPL+
URL:            http://jplesnik.fedorapeople.org/generators
Source0:        %{url}/generators-%{version}.tar.gz
Patch0:         generators-1.10-Update-shebang-for-SCL.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl >= 4:5.22.0-351
%if !%{defined perl_bootstrap}
# Break build cycle: reflexive dependency
BuildRequires:  %{?scl_prefix}perl-generators
%endif
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(Fedora::VSP)
BuildRequires:  %{?scl_prefix}perl(File::Copy)
BuildRequires:  %{?scl_prefix}perl(File::Find)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(Test::More)
BuildRequires:  %{?scl_prefix}perl(warnings)
BuildRequires:  sed
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl >= 4:5.22.0-351
# Per Perl packaging guidelines, build-requiring perl-generators should
# deliver Perl macros
Requires:       %{?scl_prefix}perl-macros
%if %{defined perl_bootstrap}
# Supply run-time dependencies manually when perl-generators is not available
Requires:       %{?scl_prefix}perl(Fedora::VSP)
%endif
%{?scl:Requires: scl-utils}

# The generators and attribute files were split from rpm-build
%{!?scl:Conflicts:      rpm-build < 4.11.2-15}

%description
This package provides RPM Perl dependencies generators which are used for
getting provides and requires from Perl binaries and modules.

%prep
%setup -q -n generators-%{version}
%{?scl:sed -i "s/@SCL@/%{scl}/" %{PATCH0}}
%{?scl:%patch0 -p1}

%build
%{?scl:scl enable %{scl} 'PERL_NS=%{scl} }perl Makefile.PL INSTALLDIRS=vendor INSTALLVENDORSCRIPT=%{_rpmconfigdir}%{?scl:'}
%{?scl:scl enable %{scl} '}make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
mkdir -p %{buildroot}%{_root_prefix}/lib/rpm/fileattrs/
install -p -m 644 fileattrs/* '%{buildroot}%{_root_prefix}/lib/rpm/fileattrs'
%endif

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc Changes TODO
%{_root_prefix}/lib/rpm/perl.*
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%{_root_prefix}/lib/rpm/fileattrs/perl*.attr
%endif

%changelog
* Sun Jul 24 2016 Petr Pisar <ppisar@redhat.com> - 1.10-2
- Rebuild without bootstrap

* Tue Jul 12 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.10-1
- 1.10 bump

* Thu Jun 23 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-1
- 1.09 bump

* Wed Jun 15 2016 Petr Pisar <ppisar@redhat.com> - 1.08-4
- Run-require perl-macros to provide the Perl macros for building Perl packages

* Wed Jun 01 2016 Petr Pisar <ppisar@redhat.com> - 1.08-3
- Supply run-time depenencies manually when perl-generators is not available on
  bootstrap

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-2
- Perl 5.24 rebuild

* Mon Mar 21 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-1
- 1.08 bump; Resolves BZ#1318658

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-2
- Add epoch to perl BR

* Tue Oct 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.07-1
- 1.07 bump
- Return perl version as normalized perl(:VERSION) symbol

* Tue Oct 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.06-1
- 1.06 bump

* Tue Sep 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.05-1
- 1.05 bump
- Resolves: bug #1267267

* Wed Jul 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.04-1
- 1.04 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-2
- Perl 5.22 rebuild

* Mon Feb 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.03-1
- 1.03 bump
- Update parcing of here-doc and quoted section

* Fri Dec 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.02-1
- 1.02 bump

* Tue Oct 21 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-1
- 1.01 bump

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-2
- Perl 5.20 rebuild

* Mon Jun 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-1
- Introduce Perl generators as a standalone package
