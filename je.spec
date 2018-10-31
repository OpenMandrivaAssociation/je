%{?_javapackages_macros:%_javapackages_macros}
Name:          je
Version:       5.0.97
Release:       3.3
Summary:       Berkeley DB Java Edition
License:       BSD
Group:         Databases
URL:           http://www.oracle.com/us/products/database/berkeley-db/je/overview/index.html
# use SOURCE2: sh je-create-tarball.sh < VERSION >
Source0:       %{name}-%{version}-clean.tar.xz
Source1:       http://download.oracle.com/maven/com/sleepycat/%{name}/%{version}/%{name}-%{version}.pom
Source2:       %{name}-create-tarball.sh
# fix javadoc build
Patch0:        %{name}-5.0.84-build.patch
Patch1:        %{name}-5.0.97-use-system-asm4.patch

BuildRequires: java-devel
BuildRequires: java-javadoc
BuildRequires: javapackages-tools

BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: junit
%if 0
# TODO set -Dandroid.libdir
# https://bugzilla.redhat.com/show_bug.cgi?id=837450
BuildRequires: android
%endif
BuildRequires: jboss-connector-1.6-api
BuildRequires: jboss-ejb-3.1-api
BuildRequires: mvn(org.ow2.asm:asm)
Requires:      mvn(org.ow2.asm:asm)

Requires:      javapackages-tools
BuildArch:     noarch

%description
Berkeley DB Java Edition is a high performance, transactional storage
engine written entirely in Java. Like the highly successful Berkeley DB
product, Berkeley DB Java Edition executes in the address space of the
application, without the overhead of client/server communication. It
stores data in the application's native format, so no run-time data
translation is required. Berkeley DB Java Edition supports full ACID
transactions and recovery. It provides an easy-to-use, programmatic
interface, allowing developers to store and retrieve information
quickly, simply and reliably.

%package examples
Summary:       Examples for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      javapackages-tools

%description examples
This package contains examples for %{name}.

%package javadoc
Summary:       Javadoc for %{name}
Requires:      javapackages-tools

%description javadoc
This package contains javadoc for %{name}.

%package examples-javadoc
Summary:       Javadoc for %{name}-examples
Requires:      %{name}-javadoc = %{version}-%{release}
Requires:      javapackages-tools

%description examples-javadoc
This package contains javadoc for %{name}-examples.

%prep
%setup -q
%patch0 -p0
cp -p %{SOURCE1} pom.xml
%patch1 -p1
sed -i "s|objectweb-asm4|objectweb-asm|" build.xml

%build

ant \
 -Dj2ee.jarfile="$(build-classpath jboss-connector-1.6-api):$(build-classpath jboss-ejb-3.1-api)" \
 -Dant.library.dir=%{_javadir} \
 jar javadoc

cd build/classes
%jar -cf ../../%{name}-examples.jar collections je jmx persist

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 build/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

install -pm 644 %{name}-examples.jar %{buildroot}%{_javadir}/%{name}-examples.jar

mkdir -p %{buildroot}%{_javadocdir}
cp -a docs/java %{buildroot}%{_javadocdir}/%{name}
cp -a docs/examples %{buildroot}%{_javadocdir}/%{name}-examples

%files -f .mfiles
%doc LICENSE README

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%files examples
%{_javadir}/%{name}-examples.jar
%doc LICENSE

%files examples-javadoc
%{_javadocdir}/%{name}-examples
%doc LICENSE

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 5.0.97-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Oct 09 2013 gil cattaneo <puntogil@libero.it> 5.0.97-1
- update to 5.0.97

* Mon Sep 30 2013 gil cattaneo <puntogil@libero.it> 5.0.84-3
- install LICENSE in javadoc subpackage

* Sat Sep 14 2013 gil cattaneo <puntogil@libero.it> 5.0.84-2
- fix files list in main package
- resolve problems during javadocs processing

* Thu Aug 15 2013 gil cattaneo <puntogil@libero.it> 5.0.84-1
- update to 5.0.84

* Mon Jun 24 2013 gil cattaneo <puntogil@libero.it> 5.0.73-1
- initial rpm
