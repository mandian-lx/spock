%{?_javapackages_macros:%_javapackages_macros}

%global namedreltag  -groovy-2.0
%global namedversion %{version}%{?namedreltag}
%global nameddottag  %(echo %{?namedreltag} | tr \- \. )
Name:          spock
Version:       0.7
Release:       0.16%{?nameddottag}%{?dist}
Summary:       A testing and specification framework
Group:         Development/Java
License:       ASL 2.0
URL:           https://github.com/spockframework/spock
Source0:       https://github.com/spockframework/spock/archive/%{name}-%{namedversion}.tar.gz
Source100:     https://repo1.maven.org/maven2/org/spockframework/%{name}-core/%{namedversion}/%{name}-core-%{namedversion}.pom
Source101:     https://repo1.maven.org/maven2/org/spockframework/%{name}-guice/%{namedversion}/%{name}-guice-%{namedversion}.pom
Patch0:        0001-Build-with-Gradle-local-mode.patch
Patch1:        spock-0.7-core-port-to-groovy2.4.8.patch
Patch100:      spock-0.7-gradle-use-local-repo.patch

BuildRequires: gradle #gradle-local
BuildRequires: maven-local
BuildRequires: apache-parent

BuildRequires: ant
BuildRequires: antlr
BuildRequires: aopalliance
BuildRequires: apache-commons-cli
BuildRequires: cglib
BuildRequires: google-guice
BuildRequires: groovy >= 2.0
BuildRequires: hamcrest
BuildRequires: junit
BuildRequires: objenesis
BuildRequires: objectweb-asm

Requires:      java
BuildArch:     noarch

Obsoletes:     %{name}-javadoc < 0.7-0.5

%description
Spock is a testing and specification framework for Java and
Groovy applications.

%package core
Summary:       Spock Framework - Core Module

%description core
Spock Framework - Core Module.

%package guice
Summary:       Spock Framework - Guice Module

%description guice
Spock Framework - Guice Module provides support for
testing Guice 2/3 based applications.

%prep
%setup -q -n %{name}-%{name}-%{namedversion}
%patch0 -p1
%patch1 -p1
#patch100 -p1 -b .local
find . -name "*.class" -delete
find . -name "*.jar" -delete

sed -i "s|sourceCompatibility = 1.5|sourceCompatibility = 1.6|" build.gradle

# We don't need these modules.
rm -rf spock-maven spock-specs spock-spring spock-tapestry spock-unitils
%mvn_package ":spock-{maven,specs,spring,tapestry,unitils}" __noinstall

# fix name in build script
sed -i "s|version = \"%{namedversion}\"|version = \"%{version}%{nameddottag}\"|" build.gradle

# add maven
cp %{SOURCE100} pom-%{name}-core.xml
cp %{SOURCE101} pom-%{name}-guice.xml
%pom_xpath_replace "pom:project/pom:version" "<version>%{version}%{nameddottag}</version>" ./pom-%{name}-core.xml
%pom_xpath_replace "pom:project/pom:version" "<version>%{version}%{nameddottag}</version>" ./pom-%{name}-guice.xml
%pom_xpath_replace "pom:dependency[pom:artifactId[./text()='spock-core']]/pom:version" "
<version>\${project.version}</version>" ./pom-%{name}-guice.xml
%pom_change_dep :junit-dep :junit ./pom-%{name}-core.xml

%build

# install task used for generate pom files
#%gradle_build -s -- -x javadoc
gradle build -s -x javadoc -x test -Dfile.encoding=UTF-8 -Dproject.rootProject=%{version}%{nameddottag}

%install
%mvn_package ':%{name}-{*}' @1
%mvn_artifact pom-%{name}-core.xml %{name}-core/build/libs/%{name}-core-%{version}%{nameddottag}.jar
%mvn_artifact pom-%{name}-guice.xml %{name}-guice/build/libs/%{name}-guice-%{version}%{nameddottag}.jar
%mvn_install

%files core -f .mfiles-core
%doc LICENSE NOTICE

%files guice -f .mfiles-guice

%changelog
* Wed Feb 08 2017 gil cattaneo <puntogil@libero.it> 0.7-0.16.groovy.2.0
- fix FTBFS

* Mon Oct  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7-0.15.groovy.2.0
- Remove BR on perl

* Thu Jul 21 2016 gil cattaneo <puntogil@libero.it> 0.7-0.14.groovy.2.0
- add missing BR

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.13.groovy.2.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan  5 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7-0.12.groovy.2.0
- Remove workaround for rhbz#1290399

* Thu Dec 10 2015 gil cattaneo <puntogil@libero.it> 0.7-0.11.groovy.2.0
- Enable local mode

* Wed Oct 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7-0.10.groovy.2.0
- Build with %%gradle_build

* Tue Jun 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7-0.9.groovy.2.0
- Use gradle-local script for building

* Fri Mar 13 2015 gil cattaneo <puntogil@libero.it> 0.7-0.8.groovy.2.0
- fix Url tag

* Wed Feb 11 2015 gil cattaneo <puntogil@libero.it> 0.7-0.7.groovy.2.0
- introduce license macro

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7-0.6.groovy.2.0
- Rebuild to fix Maven auto-requires

* Tue Nov 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7-0.5.groovy.2.0
- Build with groovy 2.x
- Remove javadoc package

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-0.4.groovy.1.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 0.7-0.3.groovy.1.8
- use objectweb-asm3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-0.2.groovy.1.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 04 2013 gil cattaneo <puntogil@libero.it> 0.7-0.1.groovy.1.8
- update to 0.7-groovy-1.8

* Tue Feb 19 2013 gil cattaneo <puntogil@libero.it> 0.6-0.5.groovy.1.8
- fixed google-guice in ant build script

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-0.4.groovy.1.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 gil cattaneo <puntogil@libero.it> 0.6-0.3.groovy.1.8
- fixed guice depmap

* Thu Aug 02 2012 gil cattaneo <puntogil@libero.it> 0.6-0.2.groovy.1.8
- Removed nonexisting requires

* Wed Aug 01 2012 gil cattaneo <puntogil@libero.it> 0.6-0.1.groovy.1.8
- initial rpm
