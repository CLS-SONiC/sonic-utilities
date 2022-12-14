#!/usr/bin/env python

""" SONiC Package Manager exceptions are defined in this module. """

from dataclasses import dataclass
from typing import Optional

from sonic_package_manager.constraint import PackageConstraint, VersionConstraint
from sonic_package_manager.version import Version


class PackageManagerError(Exception):
    """ Base class for exceptions generated by SONiC package manager """

    pass


class ManifestError(Exception):
    """ Class for manifest validate failures. """

    pass


class MetadataError(Exception):
    """ Class for metadata failures. """

    pass


@dataclass
class PackageNotFoundError(PackageManagerError):
    """ Repository not found in repository database exception """

    name: str

    def __str__(self):
        return f'Package {self.name} is not found in packages database'


@dataclass
class PackageAlreadyExistsError(PackageManagerError):
    """ Package already exists in the packages database exception. """

    name: str

    def __str__(self):
        return f'Package {self.name} already exists in packages database'


class PackageInstallationError(PackageManagerError):
    """ Exception for package installation error. """

    pass


class PackageUninstallationError(PackageManagerError):
    """ Exception for package installation error. """

    pass


class PackageUpgradeError(PackageManagerError):
    """ Exception for package upgrade error. """

    pass


@dataclass
class PackageSonicRequirementError(PackageInstallationError):
    """ Exception for installation errors, when SONiC version requirement is not met. """

    name: str
    component: str
    constraint: PackageConstraint
    installed_ver: Optional[Version] = None

    def __str__(self):
        if self.installed_ver is not None:
            return (f'Package {self.name} requires base OS component {self.component} version {self.constraint} '
                    f'while the installed version is {self.installed_ver}')
        return (f'Package {self.name} requires base OS component {self.component} version {self.constraint} '
                f'but it is not present int base OS image')


@dataclass
class PackageDependencyError(PackageInstallationError):
    """ Exception class for installation errors related to missing dependency. """

    name: str
    constraint: PackageConstraint
    installed_ver: Optional[Version] = None

    def __str__(self):
        if self.installed_ver:
            return (f'Package {self.name} requires {self.constraint} '
                    f'but version {self.installed_ver} is installed')
        return f'Package {self.name} requires {self.constraint} but it is not installed'


@dataclass
class PackageComponentDependencyError(PackageInstallationError):
    """ Exception class for installation error caused by component
    version dependency. """

    name: str
    dependency: str
    component: str
    constraint: VersionConstraint
    installed_ver: Optional[Version] = None

    def __str__(self):
        if self.installed_ver:
            return (f'Package {self.name} requires {self.component} {self.constraint} '
                    f'in package {self.dependency} but version {self.installed_ver} is installed')
        return (f'Package {self.name} requires {self.component} {self.constraint} '
                f'in package {self.dependency} but it is not installed')


@dataclass
class PackageConflictError(PackageInstallationError):
    """ Exception class for installation errors related to missing dependency. """

    name: str
    constraint: PackageConstraint
    installed_ver: Version

    def __str__(self):
        return (f'Package {self.name} conflicts with {self.constraint} but '
                f'version {self.installed_ver} is installed')


@dataclass
class PackageComponentConflictError(PackageInstallationError):
    """ Exception class for installation error caused by component
    version conflict. """

    name: str
    dependency: str
    component: str
    constraint: VersionConstraint
    installed_ver: Version

    def __str__(self):
        return (f'Package {self.name} conflicts with {self.component} {self.constraint} '
                f'in package {self.dependency} but version {self.installed_ver} is installed')
