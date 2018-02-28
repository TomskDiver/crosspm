<a class="mk-toclify" id="table-of-contents"></a>

# Table of Contents
- [��� ��������� � ������� ����������� ����������� �������?](#)
- [CrossPM �������� � ������� ��� ������ � ����������� � ��������� �������� (type: artifactory-aql)](#crosspm-type-artifactory-aql)
- [��� ������������� ������, ����� ���������� ������ ��� feature � ������?](#feature)
- [� ��� ������������� ������, ����� ���������� ������ feature ������?](#feature)
- [��� ������� ��� ������ � ������ �������, �� ���� ������?](#)
- [���� ������ ������ 5 �����, ��� �������� �����? (type: artifactory)](#5-type-artifactory)
- [��� ������� ������ �� ����� ������������?](#)
- [��� ������� �������� ��� ��� ������������ ������ ����� ���������� ������? ��������, ��� ��� ���������� ��������� ������ openssl?](#openssl)
- [���� ������������ ���, �� crosspm ������� ���� ����� - ����� ��� ������ � ������ �������?](#crosspm)

Frequently Asked Questions
==========================

<a class="mk-toclify" id=""></a>
## ��� ��������� � ������� ����������� ����������� �������?
����� ������ ������������ ����� ������ dependencies, ����� �� �� ������ �� � �� ������ ������
```yaml
cpm:
dependencies: no-dependencies.txt
dependencies-lock: no-dependencies.txt.lock
```
� �������� � ��������� ����������� �����:
```bash
crosspm download --depslock-path=./dependencies.txt.lock
```

<a class="mk-toclify" id="crosspm-type-artifactory-aql"></a>
## CrossPM �������� � ������� ��� ������ � ����������� � ��������� �������� (type: artifactory-aql)
��� ����������� �������� AQL � Artifactory - �� �������� ������������ ������ � ������������. �������� � ������ ����� ������� ������ ��� ������� � ���� ������������

<a class="mk-toclify" id="feature"></a>
## ��� ������������� ������, ����� ���������� ������ ��� feature � ������?
���� ������ ������ � ������� ��������� ���:
```yaml
columns:
version: "{int}.{int}.{int}[-{str}]"
```
�� � dependencies ����� �������, ��� �������������� ����� ������� ���� �� ������. ��� ����� ����� �������� ����������� �� �������������� ����� � ����� ����� ������. ��������� ��������� ��� �������:
```
PackageName    *-         R14.1    >=snapshot
PackageName    *.*.*-     R14.1    >=snapshot
PackageName    14.*.*-    R14.1    >=snapshot
```

<a class="mk-toclify" id="feature"></a>
## � ��� ������������� ������, ����� ���������� ������ feature ������?
���� ������ ������ � ������� ��������� ���:
```yaml
columns:
version: "{int}.{int}.{int}[-{str}]"
```
�� � dependencies ����� �������, ��� �������������� ����� ������� ������ ����. ��� ����� ����� �������� ��� �������������� ����� � ����� ����� ������. � ����� ������ CrossPM �� ����� ����� ������ ��� feature. ��������� ��������� ��� �������:
```
Agent    *-*            R14.1    >=snapshot
Agent    *-develop      R14.1    >=snapshot
Agent    *.*.*-*        R14.1    >=snapshot
Agent    14.*.*-*       R14.1    >=snapshot
Agent    14.*.*-CERT*   R14.1    >=snapshot
```

<a class="mk-toclify" id=""></a>
## ��� ������� ��� ������ � ������ �������, �� ���� ������?

����� ������� "���������������� ��� ������". ������ ����� **dependencies.txt.lock**
```
PackageRelease17 Package 17.0.*
PackageRelease161 Package 16.1.*
OtherPackage OtherPackage *
```
� �������� � ������ ������

```yaml
columns: "*uniquename, package, version" # �������� � ����� ������� ������� ��� ������

output: # ��� ��������� ������ � stdout
tree:
- uniquename: 25
- version: 0
```


<a class="mk-toclify" id="5-type-artifactory"></a>
## ���� ������ ������ 5 �����, ��� �������� �����? (type: artifactory)
������ �������� ����� ����������� � �������� **artifactory**, ����� �������� ��� �� **artifactory-aql**
```yaml
type: artifactory-aql
```

<a class="mk-toclify" id=""></a>
## ��� ������� ������ �� ����� ������������?
� ������� [���������� �� ��� ����� ������������ � ������������� import](config/IMPORT)


<a class="mk-toclify" id="openssl"></a>
## ��� ������� �������� ��� ��� ������������ ������ ����� ���������� ������? ��������, ��� ��� ���������� ��������� ������ openssl?

���� ����� ���������, ��� ��� ������ ���������� ���� ������ �������, **��** ��������� ������ �����, ��������� ��������������� � **dependencies.txt**, ����� ��������� ��������� �������:
1. [��������� ����� ������������](config/IMPORT) �� **crosspm.main.yaml**, **crosspm.download.yaml**, **crosspm.lock.yaml**
2. � **lock**-������������ ������� ������������ **dependencies.txt.lock**
3. � **download**-������������ ������� �� ������������ **no-dependencies.txt.lock**
4. ��������� crosspm � ��������� ������ ������������:

```bash
# CrossPM: lock and recursive check packages
# ���������� ������� lock-���� ��� ������� �� dep.txt, ��� ���� �������� ��� ����������� �� ������������� ����� ������ �������
crosspm lock \
dependencies.txt dependencies.txt.lock \
--recursive \
--options cl="gcc-5.1",arch="x86_64",os="debian-8" \
--config=".\crosspm.lock.yaml"
(( $? )) && exit 1

# CrossPM: downloading packages
# ������� ������ ������, ������� ������� � dependencies.txt
crosspm download \
--config=".\crosspm.download.yaml" \
--lock-on-success \
--deps-path=".\dependencies.txt" \
--out-format="cmd" \
--output=".\klmn.cmd" \
--options cl="gcc-5.1",arch="x86_64",os="debian-8" \
(( $? )) && exit 1
```

<a class="mk-toclify" id="crosspm"></a>
## ���� ������������ ���, �� crosspm ������� ���� ����� - ����� ��� ������ � ������ �������?
�� ������ ������, ���� � ���� �� ����� ��� ������, �������� `repo/projectname/projectname/projectname.version.zip`
�� ����� ��������������� � ����� `PROJECTNAME`.
� ������, ����� ������������ ����� � ����� ������� `PROJECTNAME`, �� �� � �� �������������, �.�. ��� ���������� ��� � ������ `PROJECTNAME`.

������� - ������������ ��������� ���� �� �������������\������������ ������:

```yaml
cache:
storage:
packed: '{package}/{branch}/{version}/{compiler}/{arch}/{osname}/{package}.{version}.tar.gz'
unpacked: '{package}/{branch}/{version}/{compiler}/{arch}/{osname}'
```


----------------
Table of content auto generated: https://github.com/rasbt/markdown-toclify