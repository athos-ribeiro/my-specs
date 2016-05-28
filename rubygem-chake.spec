%global gem_name chake

Name: rubygem-%{gem_name}
Version: 0.13
Release: 4%{?dist}
Summary: serverless configuration management tool for chef
Group: Development/Languages
License: MIT
URL: https://gitlab.com/terceiro/chake
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(asciidoctor)
BuildArch: noarch

%description
chake allows one to manage a number of hosts via SSH by combining chef (solo)
and rake. It doesn't require a chef server; all you need is a workstation from
where you can SSH into all your hosts. chake automates copying the
configuration management repository to the target host (including managing
encrypted files), running chef on them, and running arbitrary commands on the
hosts.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

#rake -f man/Rakefile
sed -f .%{gem_instdir}/man/readme2man.sed README.md > .%{gem_instdir}/man/chake.adoc || (rm -f .%{gem_instdir}/man/chake.adoc; false)
asciidoctor --backend manpage --out-file .%{gem_instdir}/man/chake.1 .%{gem_instdir}/man/chake.adoc

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{gem_instdir}/man/chake.1 %{buildroot}%{_mandir}/man1

# Run the test suite
%check
pushd .%{gem_instdir}
rspec -Ilib spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/chake
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.gitlab-ci.yml
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/bin
%exclude %{gem_instdir}/chake.spec.erb
%{gem_libdir}
%exclude %{gem_instdir}/man
%exclude %{gem_cache}
%{gem_spec}
%doc %{_mandir}/man1/*

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/ChangeLog.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/chake.gemspec
%{gem_instdir}/examples
%{gem_instdir}/spec

%changelog
* Fri May 20 2016 Athos Ribeiro - 0.13-4
- Install manpages

* Fri May 20 2016 Athos Ribeiro - 0.13-3
- Remove spec file template

* Fri May 20 2016 Athos Ribeiro - 0.13-2
- Remove gitlab-ci

* Fri May 20 2016 Athos Ribeiro - 0.13-1
- Version update

* Wed Jul 15 2015 Athos Ribeiro - 0.7-2
- Fix install by removing unnecessary commands

* Fri Jul 10 2015 Athos Ribeiro - 0.7-1
- Initial package
