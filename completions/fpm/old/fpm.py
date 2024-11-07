#!/usr/bin/env python3

import argparse

from cracy_complete import argparse_mod

argp = argparse.ArgumentParser(prog='fpm', description='Effing package management')

argp.add_argument('FILE', nargs='+').complete('file')

argp.add_argument('-t', '--output-type', metavar='OUTPUT_TYPE',
  choices=['apk', 'cpan', 'deb', 'dir', 'empty', 'freebsd', 'gem', 'npm', 'osxpkg', 'p5p', 'pacman', 'pear', 'pkgin', 'pleaserun', 'puppet', 'python', 'rpm', 'sh', 'snap', 'solaris', 'tar', 'virtualenv', 'zip'],
  help='the type of package you want to create (deb, rpm, solaris, etc)')

argp.add_argument('-s', '--input-type', metavar='INPUT_TYPE',
  choices=['apk', 'cpan', 'deb', 'dir', 'empty', 'freebsd', 'gem', 'npm', 'osxpkg', 'p5p', 'pacman', 'pear', 'pkgin', 'pleaserun', 'puppet', 'python', 'rpm', 'sh', 'snap', 'solaris', 'tar', 'virtualenv', 'zip'],
  help='the package type to use as input (gem, rpm, python, etc)')

argp.add_argument('-C', '--chdir', metavar='CHDIR',
  help='Change directory to here before searching for files').complete('directory')

argp.add_argument('--prefix', metavar='PREFIX',
  help="A path to prefix files with when building the target package. This may not be necessary for all input packages. For example, the 'gem' type will prefix with your gem directory automatically.")

argp.add_argument('-p', '--package', metavar='OUTPUT',
  help='The package file path to output.')

argp.add_argument('-f', '--force', action='store_true',
  help='Force output even if it will overwrite an existing file (default: false)')

argp.add_argument('-n', '--name', metavar='NAME',
  help='The name to give to the package')

argp.add_argument('--log', metavar='LEVEL',
  choices=['error', 'warn', 'info', 'debug'],
  help='Set the log level. Values: error, warn, info, debug.')

argp.add_argument('--verbose', action='store_true',
  help='Enable verbose output')

argp.add_argument('--debug', action='store_true',
  help='Enable debug output')

argp.add_argument('--debug-workspace', action='store_true',
  help='Keep any file workspaces around for debugging. This will disable automatic cleanup of package staging and build paths. It will also print which directories are available.')

argp.add_argument('-v', '--version', metavar='VERSION',
  help='The version to give to the package (default: 1.0)')

argp.add_argument('--iteration', metavar='ITERATION',
  help="The iteration to give to the package. RPM calls this the 'release'. FreeBSD calls it 'PORTREVISION'. Debian calls this 'debian_revision'")

argp.add_argument('--epoch', metavar='EPOCH',
  help="The epoch value for this package. RPM and Debian calls this 'epoch'. FreeBSD calls this 'PORTEPOCH'")

argp.add_argument('--license', metavar='LICENSE',
  help='(optional) license name for this package')

argp.add_argument('--vendor', metavar='VENDOR',
  help='(optional) vendor name for this package')

argp.add_argument('--category', metavar='CATEGORY',
  help='(optional) category this package belongs to (default: "none")')

argp.add_argument('-d', '--depends', metavar='DEPENDENCY',
  help="A dependency. This flag can be specified multiple times. Value is usually in the form of: -d 'name' or -d 'name > version'").set_multiple_option()

argp.add_argument('--no-depends', action='store_true',
  help='Do not list any dependencies in this package (default: false)')

argp.add_argument('--no-auto-depends', action='store_true',
  help='Do not list any dependencies in this package automatically (default: false)')

argp.add_argument('--provides', metavar='PROVIDES',
  help='What this package provides (usually a name). This flag can be specified multiple times.').set_multiple_option()

argp.add_argument('--conflicts', metavar='CONFLICTS',
  help='Other packages/versions this package conflicts with. This flag can be specified multiple times.').set_multiple_option()

argp.add_argument('--replaces', metavar='REPLACES',
  help="Other packages/versions this package replaces. Equivalent of rpm's 'Obsoletes'. This flag can be specified multiple times.").set_multiple_option()

argp.add_argument('--config-files', metavar='CONFIG_FILES',
  help="Mark a file in the package as being a config file. This uses 'conffiles' in debs and %config in rpm. If you have multiple files to mark as configuration files, specify this flag multiple times.  If argument is directory all files inside it will be recursively marked as config files.").set_multiple_option()

argp.add_argument('--directories', metavar='DIRECTORIES',
  help='Recursively mark a directory as being owned by the package. Use this flag multiple times if you have multiple directories and they are not under the same parent directory').set_multiple_option()

argp.add_argument('-a', '--architecture', metavar='ARCHITECTURE',
  help="The architecture name. Usually matches 'uname -m'. For automatic values, you can use '-a all' or '-a native'. These two strings will be translated into the correct value for your platform and target package type.")

argp.add_argument('-m', '--maintainer', metavar='MAINTAINER',
  help='The maintainer of this package. (default: "<user@host>")')

argp.add_argument('-S', '--package-name-suffix', metavar='PACKAGE_NAME_SUFFIX',
  help='a name suffix to append to package and dependencies.')

argp.add_argument('-e', '--edit', action='store_true',
  help='Edit the package spec before building. (default: false)')

argp.add_argument('-x', '--exclude', metavar='EXCLUDE_PATTERN',
  help='Exclude paths matching pattern (shell wildcard globs valid here). If you have multiple file patterns to exclude, specify this flag multiple times.').set_multiple_option()

argp.add_argument('--exclude-file', metavar='EXCLUDE_PATH',
  help='The path to a file containing a newline-sparated list of patterns to exclude from input.').complete('file')

argp.add_argument('--description', metavar='DESCRIPTION',
  help='Add a description for this package. You can include \'\\n\' sequences to indicate newline breaks. (default: "no description")')

argp.add_argument('--url', metavar='URI',
  help='Add a url for this package. (default: "http://example.com/no-uri-given")')

argp.add_argument('--inputs', metavar='INPUTS_PATH',
  help='The path to a file containing a newline-separated list of files and dirs to use as input.').complete('file')

argp.add_argument('--post-install', metavar='FILE',
  help='(DEPRECATED, use --after-install) A script to be run after package installation').complete('file')

argp.add_argument('--pre-install', metavar='FILE',
  help='(DEPRECATED, use --before-install) A script to be run before package installation').complete('file')

argp.add_argument('--post-uninstall', metavar='FILE',
  help='(DEPRECATED, use --after-remove) A script to be run after package removal').complete('file')

argp.add_argument('--pre-uninstall', metavar='FILE',
  help='(DEPRECATED, use --before-remove) A script to be run before package removal').complete('file')

argp.add_argument('--after-install', metavar='FILE',
  help='A script to be run after package installation').complete('file')

argp.add_argument('--before-install', metavar='FILE',
  help='A script to be run before package installation').complete('file')

argp.add_argument('--after-remove', metavar='FILE',
  help='A script to be run after package removal').complete('file')

argp.add_argument('--before-remove', metavar='FILE',
  help='A script to be run before package removal').complete('file')

argp.add_argument('--after-upgrade', metavar='FILE',
  help='A script to be run after package upgrade').complete('file')

argp.add_argument('--before-upgrade', metavar='FILE',
  help='A script to be run before package upgrade').complete('file')

argp.add_argument('--template-scripts', action='store_true',
  help='Allow scripts to be templated. This lets you use ERB to template your packaging scripts (for --after-install, etc). For example, you can do things like <%= name %> to get the package name. For more information, see the fpm wiki: https://github.com/jordansissel/fpm/wiki/Script-Templates')

argp.add_argument('--template-value', metavar='KEY=VALUE',
  help="Make 'key' available in script templates, so <%= key %> given will be the provided value. Implies --template-scripts")

argp.add_argument('--workdir', metavar='WORKDIR',
  help='The directory you want fpm to do its work in, where \'work\' is any file copying, downloading, etc. Roughly any scratch space fpm needs to build your package. (default: "/tmp")').complete('directory')

argp.add_argument('--source-date-epoch-from-changelog', action='store_true',
  help='Use release date from changelog as timestamp on generated files to reduce nondeterminism. Experimental; only implemented for gem so far.  (default: false)')

argp.add_argument('--source-date-epoch-default', metavar='SOURCE_DATE_EPOCH_DEFAULT',
  help='If no release date otherwise specified, use this value as timestamp on generated files to reduce nondeterminism. Reproducible build environments such as dpkg-dev and rpmbuild set this via envionment variable SOURCE_DATE_EPOCH variable to the integer unix timestamp to use in generated archives, and expect tools like fpm to use it as a hint to avoid nondeterministic output. This is a Unix timestamp, i.e. number of seconds since 1 Jan 1970 UTC. See https://reproducible-builds.org/specs/source-date-epoch  (default: $SOURCE_DATE_EPOCH)')

argp.add_argument('--fpm-options-file', metavar='FPM_OPTIONS_FILE',
  help='A file that contains additional fpm options. Any fpm flag format is valid in this file. This can be useful on build servers where you want to use a common configuration or inject other parameters from a file instead of from a command-line flag..').complete('file')

argp.add_argument('--gem-bin-path', metavar='DIRECTORY',
  help='The directory to install gem executables').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-package-prefix', metavar='NAMEPREFIX',
  help='(DEPRECATED, use --package-name-prefix) Name to prefix the package name with.').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-package-name-prefix', metavar='PREFIX',
  help='Name to prefix the package name with. (default: "rubygem")').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-gem', metavar='PATH_TO_GEM',
  help='The path to the \'gem\' tool (defaults to \'gem\' and searches your $PATH) (default: "gem")').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-shebang', metavar='SHEBANG',
  help='Replace the shebang in the executables in the bin path with a custom string (default: nil)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-fix-name', action='store_true',
  help='Should the target package name be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--no-gem-fix-name', action='store_true',
  help='Should the target package name be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-fix-dependencies', action='store_true',
  help='Should the package dependencies be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--no-gem-fix-dependencies', action='store_true',
  help='Should the package dependencies be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-env-shebang', action='store_true',
  help='Should the target package have the shebang rewritten to use env? (default: true)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--no-gem-env-shebang', action='store_true',
  help='Should the target package have the shebang rewritten to use env? (default: true)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-prerelease', action='store_true',
  help='Allow prerelease versions of a gem (default: false)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--no-gem-prerelease', action='store_true',
  help='Allow prerelease versions of a gem (default: false)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-disable-dependency', metavar='GEM_NAME',
  help='The gem name to remove from dependency list').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-embed-dependencies', action='store_true',
  help='Should the gem dependencies be installed? (default: false)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--no-gem-embed-dependencies', action='store_true',
  help='Should the gem dependencies be installed? (default: false)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-version-bins', action='store_true',
  help='Append the version to the bins (default: false)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--no-gem-version-bins', action='store_true',
  help='Append the version to the bins (default: false)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-stagingdir', metavar='STAGINGDIR',
  help='The directory where fpm installs the gem temporarily before conversion. Normally a random subdirectory of workdir.').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-git-repo', metavar='GIT_REPO',
  help='Use this git repo address as the source of the gem instead of rubygems.org. (default: nil)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--gem-git-branch', metavar='GIT_BRANCH',
  help='When using a git repo as the source of the gem instead of rubygems.org, use this git branch. (default: nil)').when("option_is -t --output-type -s --input-type -- gem")

argp.add_argument('--cpan-perl-bin', metavar='PERL_EXECUTABLE',
  help='The path to the perl executable you wish to run. (default: "perl")').complete('command').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-cpanm-bin', metavar='CPANM_EXECUTABLE',
  help='The path to the cpanm executable you wish to run. (default: "cpanm")').complete('command').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-mirror', metavar='CPAN_MIRROR',
  help='The CPAN mirror to use instead of the default.').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-mirror-only', action='store_true',
  help='Only use the specified mirror for metadata. (default: false)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--no-cpan-mirror-only', action='store_true',
  help='Only use the specified mirror for metadata. (default: false)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-package-name-prefix', metavar='NAME_PREFIX',
  help='Name to prefix the package name with. (default: "perl")').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-test', action='store_true',
  help='Run the tests before packaging? (default: true)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--no-cpan-test', action='store_true',
  help='Run the tests before packaging? (default: true)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-verbose', action='store_true',
  help='Produce verbose output from cpanm? (default: false)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--no-cpan-verbose', action='store_true',
  help='Produce verbose output from cpanm? (default: false)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-perl-lib-path', metavar='PERL_LIB_PATH',
  help='Path of target Perl Libraries').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-sandbox-non-core', action='store_true',
  help="Sandbox all non-core modules, even if they're already installed (default: true)").when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--no-cpan-sandbox-non-core', action='store_true',
  help="Sandbox all non-core modules, even if they're already installed (default: true)").when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--cpan-cpanm-force', action='store_true',
  help='Pass the --force parameter to cpanm (default: false)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--no-cpan-cpanm-force', action='store_true',
  help='Pass the --force parameter to cpanm (default: false)').when("option_is -t --output-type -s --input-type -- cpan")

argp.add_argument('--deb-ignore-iteration-in-dependencies', action='store_true',
  help="For '=' (equal) dependencies, allow iterations on the specified version. Default is to be specific. This option allows the same version of a package but any iteration is permitted").when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-ignore-iteration-in-dependencies', action='store_true',
  help="For '=' (equal) dependencies, allow iterations on the specified version. Default is to be specific. This option allows the same version of a package but any iteration is permitted").when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-build-depends', metavar='DEPENDENCY',
  help='Add DEPENDENCY as a Build-Depends').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-pre-depends', metavar='DEPENDENCY',
  help='Add DEPENDENCY as a Pre-Depends').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-compression', metavar='COMPRESSION',
  choices=['gz', 'bzip2', 'xz', 'none'],
  help='The compression type to use, must be one of gz, bzip2, xz, none. (default: "gz")').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-dist', metavar='DIST-TAG',
  help='Set the deb distribution. (default: "unstable")').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-custom-control', metavar='FILEPATH',
  help='Custom version of the Debian control file.').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-config', metavar='SCRIPTPATH',
  help='Add SCRIPTPATH as debconf config file.').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-templates', metavar='FILEPATH',
  help='Add FILEPATH as debconf templates file.').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-installed-size', metavar='KILOBYTES',
  help='The installed size, in kilobytes. If omitted, this will be calculated automatically').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-priority', metavar='PRIORITY',
  help='The debian package \'priority\' value. (default: "optional")').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-use-file-permissions', action='store_true',
  help='Use existing file permissions when defining ownership and modes').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-use-file-permissions', action='store_true',
  help='Use existing file permissions when defining ownership and modes').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-user', metavar='USER',
  help='The owner of files in this package (default: "root")').complete('user').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-group', metavar='GROUP',
  help='The group owner of files in this package (default: "root")').complete('group').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-changelog', metavar='FILEPATH',
  help='Add FILEPATH as debian changelog').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-generate-changes', action='store_true',
  help='Generate PACKAGENAME.changes file. (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-generate-changes', action='store_true',
  help='Generate PACKAGENAME.changes file. (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-upstream-changelog', metavar='FILEPATH',
  help='Add FILEPATH as upstream changelog').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-recommends', metavar='PACKAGE',
  help='Add PACKAGE to Recommends').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-suggests', metavar='PACKAGE',
  help='Add PACKAGE to Suggests').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-meta-file', metavar='FILEPATH',
  help='Add FILEPATH to DEBIAN directory').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-interest', metavar='EVENT',
  help='Package is interested in EVENT trigger').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-activate', metavar='EVENT',
  help='Package activates EVENT trigger').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-interest-noawait', metavar='EVENT',
  help='Package is interested in EVENT trigger without awaiting').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-activate-noawait', metavar='EVENT',
  help='Package activates EVENT trigger').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-field', metavar='FIELD_AND_VALUE',
  help="'FIELD: VALUE' Add custom field to the control file").when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-no-default-config-files', action='store_true',
  help='Do not add all files in /etc as configuration files by default for Debian packages. (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-no-default-config-files', action='store_true',
  help='Do not add all files in /etc as configuration files by default for Debian packages. (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-auto-config-files', action='store_true',
  help='Init script and default configuration files will be labeled as configuration files for Debian packages. (default: true)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-auto-config-files', action='store_true',
  help='Init script and default configuration files will be labeled as configuration files for Debian packages. (default: true)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-shlibs', metavar='SHLIBS',
  help='Include control/shlibs content. This flag expects a string that is used as the contents of the shlibs file. See the following url for a description of this file and its format: http://www.debian.org/doc/debian-policy/ch-sharedlibs.html#s-shlibs').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-init', metavar='FILEPATH',
  help='Add FILEPATH as an init script').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-default', metavar='FILEPATH',
  help='Add FILEPATH as /etc/default configuration').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-upstart', metavar='FILEPATH',
  help='Add FILEPATH as an upstart script').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-systemd', metavar='FILEPATH',
  help='Add FILEPATH as a systemd script').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-systemd-enable', action='store_true',
  help='Enable service on install or upgrade (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-systemd-enable', action='store_true',
  help='Enable service on install or upgrade (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-systemd-auto-start', action='store_true',
  help='Start service after install or upgrade (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-systemd-auto-start', action='store_true',
  help='Start service after install or upgrade (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-systemd-restart-after-upgrade', action='store_true',
  help='Restart service after upgrade (default: true)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-systemd-restart-after-upgrade', action='store_true',
  help='Restart service after upgrade (default: true)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-after-purge', metavar='FILE',
  help='A script to be run after package removal to purge remaining (config) files (a.k.a. postrm purge within apt-get purge)').complete('file').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--deb-maintainerscripts-force-errorchecks', action='store_true',
  help='Activate errexit shell option according to lintian. https://lintian.debian.org/tags/maintainer-script-ignores-errors.html (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--no-deb-maintainerscripts-force-errorchecks', action='store_true',
  help='Activate errexit shell option according to lintian. https://lintian.debian.org/tags/maintainer-script-ignores-errors.html (default: false)').when("option_is -t --output-type -s --input-type -- deb")

argp.add_argument('--npm-bin', metavar='NPM_EXECUTABLE',
  help='The path to the npm executable you wish to run. (default: "npm")').complete('command').when("option_is -t --output-type -s --input-type -- npm")

argp.add_argument('--npm-package-name-prefix', metavar='PREFIX',
  help='Name to prefix the package name with. (default: "node")').when("option_is -t --output-type -s --input-type -- npm")

argp.add_argument('--npm-registry', metavar='NPM_REGISTRY',
  help='The npm registry to use instead of the default.').when("option_is -t --output-type -s --input-type -- npm")

argp.add_argument('--rpm-use-file-permissions', action='store_true',
  help='Use existing file permissions when defining ownership and modes.').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-use-file-permissions', action='store_true',
  help='Use existing file permissions when defining ownership and modes.').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-user', metavar='USER',
  help='Set the user to USER in the %files section. Overrides the user when used with use-file-permissions setting.').complete('user').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-group', metavar='GROUP',
  help='Set the group to GROUP in the %files section. Overrides the group when used with use-file-permissions setting.').complete('group').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-defattrfile', metavar='ATTR',
  help='Set the default file mode (%defattr). (default: "-")').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-defattrdir', metavar='ATTR',
  help='Set the default dir mode (%defattr). (default: "-")').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-rpmbuild-define', metavar='DEFINITION',
  help='Pass a --define argument to rpmbuild.').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-dist', metavar='DIST-TAG',
  help='Set the rpm distribution.').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-digest', metavar='RPPM_DIGEST',
  choices=['md5', 'sha1', 'sha256', 'sha384', 'sha512'],
  help='Select a digest algorithm. md5 works on the most platforms. md5|sha1|sha256|sha384|sha512 (default: "md5")').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-compression-level', metavar='LEVEL',
  choices=range(0, 10),
  help='Select a compression level. 0 is store-only. 9 is max compression. (default: "9")').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-compression', metavar='COMPRESSION',
  choices=['none', 'xz', 'xzmt', 'gzip', 'bzip2'],
  help='Select a compression method. gzip works on the most platforms. none|xz|xzmt|gzip|bzip2 (default: "gzip")').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-os', metavar='OS',
  help="The operating system to target this rpm for. You want to set this to 'linux' if you are using fpm on OS X, for example").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-changelog', metavar='FILEPATH',
  help='Add changelog from FILEPATH contents').complete('file').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-summary', metavar='SUMMARY',
  help='Set the RPM summary. Overrides the first line on the description if set').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-sign', action='store_true',
  help='Pass --sign to rpmbuild').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-sign', action='store_true',
  help='Pass --sign to rpmbuild').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-auto-add-directories', action='store_true',
  help='Auto add directories not part of filesystem').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-auto-add-directories', action='store_true',
  help='Auto add directories not part of filesystem').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-auto-add-exclude-directories', metavar='DIRECTORIES',
  help="Additional directories ignored by '--rpm-auto-add-directories' flag").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-autoreqprov', action='store_true',
  help="Enable RPM's AutoReqProv option").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-autoreqprov', action='store_true',
  help="Enable RPM's AutoReqProv option").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-autoreq', action='store_true',
  help="Enable RPM's AutoReq option").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-autoreq', action='store_true',
  help="Enable RPM's AutoReq option").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-autoprov', action='store_true',
  help="Enable RPM's AutoProv option").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-autoprov', action='store_true',
  help="Enable RPM's AutoProv option").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-attr', metavar='ATTRFILE',
  help='Set the attribute for a file (%attr), e.g. --rpm-attr 750,user1,group1:/some/file').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-init', metavar='FILEPATH',
  help='Add FILEPATH as an init script').complete('file').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-filter-from-provides', metavar='REGEX',
  help='Set %filter_from_provides to the supplied REGEX.').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-filter-from-requires', metavar='REGEX',
  help='Set %filter_from_requires to the supplied REGEX.').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-tag', metavar='TAG',
  help="Adds a custom tag in the spec file as is. Example: --rpm-tag 'Requires(post): /usr/sbin/alternatives'").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-ignore-iteration-in-dependencies', action='store_true',
  help="For '=' (equal) dependencies, allow iterations on the specified version. Default is to be specific. This option allows the same version of a package but any iteration is permitted").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-ignore-iteration-in-dependencies', action='store_true',
  help="For '=' (equal) dependencies, allow iterations on the specified version. Default is to be specific. This option allows the same version of a package but any iteration is permitted").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-verbatim-gem-dependencies', action='store_true',
  help="When converting from a gem, leave the old (fpm 0.4.x) style dependency names. This flag will use the old 'rubygem-foo' names in rpm requires instead of the redhat style rubygem(foo). (default: false)").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-verbatim-gem-dependencies', action='store_true',
  help="When converting from a gem, leave the old (fpm 0.4.x) style dependency names. This flag will use the old 'rubygem-foo' names in rpm requires instead of the redhat style rubygem(foo). (default: false)").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-macro-expansion', action='store_true',
  help='install-time macro expansion in %pre %post %preun %postun scripts (see: https://rpm.org/user_doc/scriptlet_expansion.html) (default: false)').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--no-rpm-macro-expansion', action='store_true',
  help='install-time macro expansion in %pre %post %preun %postun scripts (see: https://rpm.org/user_doc/scriptlet_expansion.html) (default: false)').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-verifyscript', metavar='FILE',
  help='a script to be run on verification').complete('file').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-pretrans', metavar='FILE',
  help='pretrans script').complete('file').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-posttrans', metavar='FILE',
  help='posttrans script').complete('file').when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-trigger-before-install', metavar='PACKAGE',
  help="'[OPT]PACKAGE: FILEPATH' Adds a rpm trigger script located in FILEPATH, having 'OPT' options and linking to 'PACKAGE'. PACKAGE can be a comma seperated list of packages. See: http://rpm.org/api/4.4.2.2/triggers.html").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-trigger-after-install', metavar='PACKAGE',
  help="'[OPT]PACKAGE: FILEPATH' Adds a rpm trigger script located in FILEPATH, having 'OPT' options and linking to 'PACKAGE'. PACKAGE can be a comma seperated list of packages. See: http://rpm.org/api/4.4.2.2/triggers.html").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-trigger-before-uninstall', metavar='PACKAGE',
  help="'[OPT]PACKAGE: FILEPATH' Adds a rpm trigger script located in FILEPATH, having 'OPT' options and linking to 'PACKAGE'. PACKAGE can be a comma seperated list of packages. See: http://rpm.org/api/4.4.2.2/triggers.html").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--rpm-trigger-after-target-uninstall', metavar='PACKAGE',
  help="'[OPT]PACKAGE: FILEPATH' Adds a rpm trigger script located in FILEPATH, having 'OPT' options and linking to 'PACKAGE'. PACKAGE can be a comma seperated list of packages. See: http://rpm.org/api/4.4.2.2/triggers.html").when("option_is -t --output-type -s --input-type -- rpm")

argp.add_argument('--pear-package-name-prefix', metavar='PREFIX',
  help='Name prefix for pear package (default: "php-pear")').when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--pear-channel', metavar='CHANNEL_URL',
  help='The pear channel url to use instead of the default.').when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--pear-channel-update', action='store_true',
  help="call 'pear channel-update' prior to installation").when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--no-pear-channel-update', action='store_true',
  help="call 'pear channel-update' prior to installation").when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--pear-bin-dir', metavar='BIN_DIR',
  help='Directory to put binaries in').when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--pear-php-bin', metavar='PHP_BIN',
  help='Specify php executable path if differs from the os used for packaging').when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--pear-php-dir', metavar='PHP_DIR',
  help='Specify php dir relative to prefix if differs from pear default (pear/php)').when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--pear-data-dir', metavar='DATA_DIR',
  help='Specify php dir relative to prefix if differs from pear default (pear/data)').when("option_is -t --output-type -s --input-type -- pear")

argp.add_argument('--python-bin', metavar='PYTHON_EXECUTABLE',
  help='The path to the python executable you wish to run. (default: "python")').complete('command').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-easyinstall', metavar='EASYINSTALL_EXECUTABLE',
  help='The path to the easy_install executable tool (default: "easy_install")').complete('command').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-pip', metavar='PIP_EXECUTABLE',
  help='The path to the pip executable tool. If not specified, easy_install is used instead (default: nil)').complete('command').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-pypi', metavar='PYPI_URL',
  help='PyPi Server uri for retrieving packages. (default: "https://pypi.python.org/simple")').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-trusted-host', metavar='PYPI_TRUSTED',
  help='Mark this host or host:port pair as trusted for pip (default: nil)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-package-prefix', metavar='NAMEPREFIX',
  help='(DEPRECATED, use --package-name-prefix) Name to prefix the package name with.').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-package-name-prefix', metavar='PREFIX',
  help='Name to prefix the package name with. (default: "python")').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-fix-name', action='store_true',
  help='Should the target package name be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--no-python-fix-name', action='store_true',
  help='Should the target package name be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-fix-dependencies', action='store_true',
  help='Should the package dependencies be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--no-python-fix-dependencies', action='store_true',
  help='Should the package dependencies be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-downcase-name', action='store_true',
  help='Should the target package name be in lowercase? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--no-python-downcase-name', action='store_true',
  help='Should the target package name be in lowercase? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-downcase-dependencies', action='store_true',
  help='Should the package dependencies be in lowercase? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--no-python-downcase-dependencies', action='store_true',
  help='Should the package dependencies be in lowercase? (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-install-bin', metavar='BIN_PATH',
  help='The path to where python scripts should be installed to.').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-install-lib', metavar='LIB_PATH',
  help="The path to where python libs should be installed to (default depends on your python installation). Want to find out what your target platform is using? Run this: python -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()'").when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-install-data', metavar='DATA_PATH',
  help="The path to where data should be installed to. This is equivalent to 'python setup.py --install-data DATA_PATH").when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-dependencies', action='store_true',
  help='Include requirements defined in setup.py as dependencies. (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--no-python-dependencies', action='store_true',
  help='Include requirements defined in setup.py as dependencies. (default: true)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-obey-requirements-txt', action='store_true',
  help='Use a requirements.txt file in the top-level directory of the python package for dependency detection. (default: false)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--no-python-obey-requirements-txt', action='store_true',
  help='Use a requirements.txt file in the top-level directory of the python package for dependency detection. (default: false)').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-scripts-executable', metavar='PYTHON_EXECUTABLE',
  help="Set custom python interpreter in installing scripts. By default distutils will replace python interpreter in installing scripts (specified by shebang) with current python interpreter (sys.executable). This option is equivalent to appending 'build_scripts --executable PYTHON_EXECUTABLE' arguments to 'setup.py install' command.").complete('command').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-disable-dependency', metavar='PYTHON_PACKAGE_NAME',
  help='The python package name to remove from dependency list (default: [])').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-setup-py-arguments', metavar='SETUP_PY_ARGUMENT',
  help='Arbitrary argument(s) to be passed to setup.py (default: [])').when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--python-internal-pip', action='store_true',
  help="Use the pip module within python to install modules - aka 'python -m pip'. This is the recommended usage since Python 3.4 (2014) instead of invoking the 'pip' script (default: true)").when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--no-python-internal-pip', action='store_true',
  help="Use the pip module within python to install modules - aka 'python -m pip'. This is the recommended usage since Python 3.4 (2014) instead of invoking the 'pip' script (default: true)").when("option_is -t --output-type -s --input-type -- python")

argp.add_argument('--osxpkg-identifier-prefix', metavar='IDENTIFIER_PREFIX',
  help="Reverse domain prefix prepended to package identifier, ie. 'org.great.my'. If this is omitted, the identifer will be the package name.").when("option_is -t --output-type -s --input-type -- osxpkg")

argp.add_argument('--osxpkg-payload-free', action='store_true',
  help='Define no payload, assumes use of script options. (default: false)').when("option_is -t --output-type -s --input-type -- osxpkg")

argp.add_argument('--no-osxpkg-payload-free', action='store_true',
  help='Define no payload, assumes use of script options. (default: false)').when("option_is -t --output-type -s --input-type -- osxpkg")

argp.add_argument('--osxpkg-ownership', metavar='OWNERSHIP',
  help='--ownership option passed to pkgbuild. Defaults to \'recommended\'. See pkgbuild(1). (default: "recommended")').when("option_is -t --output-type -s --input-type -- osxpkg")

argp.add_argument('--osxpkg-postinstall-action', metavar='POSTINSTALL_ACTION',
  choices=['logout', 'restart', 'shutdown'],
  help="Post-install action provided in package metadata. Optionally one of 'logout', 'restart', 'shutdown'.").when("option_is -t --output-type -s --input-type -- osxpkg")

argp.add_argument('--osxpkg-dont-obsolete', metavar='DONT_OBSOLETE_PATH',
  help="A file path for which to 'dont-obsolete' in the built PackageInfo. Can be specified multiple times.").when("option_is -t --output-type -s --input-type -- osxpkg").set_multiple_option()

argp.add_argument('--solaris-user', metavar='USER',
  help='Set the user to USER in the prototype files. (default: "root")').complete('user').when("option_is -t --output-type -s --input-type -- solaris")

argp.add_argument('--solaris-group', metavar='GROUP',
  help='Set the group to GROUP in the prototype file. (default: "root")').complete('group').when("option_is -t --output-type -s --input-type -- solaris")

argp.add_argument('--p5p-user', metavar='USER',
  help='Set the user to USER in the prototype files. (default: "root")').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--p5p-group', metavar='GROUP',
  help='Set the group to GROUP in the prototype file. (default: "root")').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--p5p-zonetype', metavar='ZONETYPE',
  help='Set the allowed zone types (global, nonglobal, both) (default: "value=global value=nonglobal")').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--p5p-publisher', metavar='PUBLISHER',
  help='Set the publisher name for the repository (default: "FPM")').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--p5p-lint', action='store_true',
  help='Check manifest with pkglint (default: true)').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--no-p5p-lint', action='store_true',
  help='Check manifest with pkglint (default: true)').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--p5p-validate', action='store_true',
  help='Validate with pkg install (default: true)').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--no-p5p-validate', action='store_true',
  help='Validate with pkg install (default: true)').when("option_is -t --output-type -s --input-type -- p5p")

argp.add_argument('--freebsd-origin', metavar='ABI',
  help='Sets the FreeBSD \'origin\' pkg field (default: "fpm/<name>")').when("option_is -t --output-type -s --input-type -- freebsd")

argp.add_argument('--snap-yaml', metavar='FILEPATH',
  help='Custom version of the snap.yaml file.').complete('file').when("option_is -t --output-type -s --input-type -- snap")

argp.add_argument('--snap-confinement', metavar='CONFINEMENT',
  help='Type of confinement to use for this snap. (default: "devmode")').when("option_is -t --output-type -s --input-type -- snap")

argp.add_argument('--snap-grade', metavar='GRADE',
  help='Grade of this snap. (default: "devel")').when("option_is -t --output-type -s --input-type -- snap")

argp.add_argument('--pacman-optional-depends', metavar='PACKAGE',
  help='Add an optional dependency to the pacman package.').when("option_is -t --output-type -s --input-type -- pacman")

argp.add_argument('--pacman-use-file-permissions', action='store_true',
  help='Use existing file permissions when defining ownership and modes').when("option_is -t --output-type -s --input-type -- pacman")

argp.add_argument('--no-pacman-use-file-permissions', action='store_true',
  help='Use existing file permissions when defining ownership and modes').when("option_is -t --output-type -s --input-type -- pacman")

argp.add_argument('--pacman-user', metavar='USER',
  help='The owner of files in this package (default: "root")').complete('user').when("option_is -t --output-type -s --input-type -- pacman")

argp.add_argument('--pacman-group', metavar='GROUP',
  help='The group owner of files in this package (default: "root")').complete('group').when("option_is -t --output-type -s --input-type -- pacman")

argp.add_argument('--pacman-compression', metavar='COMPRESSION',
  choices=['gz', 'bzip2', 'xz', 'zstd', 'none'],
  help='The compression type to use, must be one of gz, bzip2, xz, zstd, none. (default: "zstd")').when("option_is -t --output-type -s --input-type -- pacman")

argp.add_argument('--pleaserun-name', metavar='SERVICE_NAME',
  help='The name of the service you are creating').when("option_is -t --output-type -s --input-type -- pleaserun")

argp.add_argument('--pleaserun-chdir', metavar='CHDIR',
  help='The working directory used by the service').complete('directory').when("option_is -t --output-type -s --input-type -- pleaserun")

argp.add_argument('--pleaserun-user', metavar='USER',
  help='The user to use for executing this program.').when("option_is -t --output-type -s --input-type -- pleaserun")

argp.add_argument('--virtualenv-pypi', metavar='PYPI_URL',
  help='PyPi Server uri for retrieving packages. (default: "https://pypi.python.org/simple")').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-package-name-prefix', metavar='PREFIX',
  help='Name to prefix the package name with. (default: "virtualenv")').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-install-location', metavar='DIRECTORY',
  help='DEPRECATED: Use --prefix instead.  Location to which to install the virtualenv by default. (default: "/usr/share/python")').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-fix-name', action='store_true',
  help='Should the target package name be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--no-virtualenv-fix-name', action='store_true',
  help='Should the target package name be prefixed? (default: true)').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-other-files-dir', metavar='DIRECTORY',
  help='Optionally, the contents of the specified directory may be added to the package. This is useful if the virtualenv needs configuration files, etc. (default: nil)').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-pypi-extra-url', metavar='PYPI_EXTRA_URL',
  help='PyPi extra-index-url for pointing to your priviate PyPi (default: nil)').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-setup-install', action='store_true',
  help='After building virtualenv run setup.py install useful when building a virtualenv for packages and including their requirements from').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--no-virtualenv-setup-install', action='store_true',
  help='After building virtualenv run setup.py install useful when building a virtualenv for packages and including their requirements from').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-system-site-packages', action='store_true',
  help='Give the virtual environment access to the global site-packages').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--no-virtualenv-system-site-packages', action='store_true',
  help='Give the virtual environment access to the global site-packages').when("option_is -t --output-type -s --input-type -- virtualenv")

argp.add_argument('--virtualenv-find-links', metavar='PIP_FIND_LINKS',
  help="If a url or path to an html file, then parse for links to archives. If a local path or file:// url that's a directory, then look for archives in the directory listing. (default: nil)").when("option_is -t --output-type -s --input-type -- virtualenv")

