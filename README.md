# kcheck

A python utility for recording required kernel symbols and checking .config files for them.

## Dependencies


 - python-3
 - setuptools
 - configargparse

## Installation

While installing through your distributions package manager would be preferable, you can also simply download, unpack,
and install with setuptools:

```
wget https://github.com/wraeth/kcheck/archive/0.0.1.tar.gz -O kcheck-0.0.1.tar.gz
tar xzf kcheck-0.0.1.tar.gz
cd kcheck-0.0.1
./setup.py install
```

Note that, by default, the configuration file may get installed to `/usr/etc/kcheck.conf`. This will need to be moved to
`/etc/kcheck.conf`, or you can specify the config file path with `--config`.

See `./setup.py --help` for other options.

## Usage

Edit the config file `kcheck.conf` to add the kernel symbol names and their required values. This file is reasonably
well documented, but in short, there are three sections: `[system]`, `[ternary]`, and `[string]`.

Kernel symbols listed in the config file may be upper or lowercase, may keep or omit the prefix `CONFIG_`, and may
specify valid values or none to default to "enabled" (`Y` or `N`).

### [System]

The system section contains configuration items for the running of `kcheck` itself. Any log-format option specified on
the command line can be set in this section.

```
kernel = /proc/config.gz
```

Note that `kcheck` also supports reading from gzip-compressed kernel configs (as in those included via
`CONFIG_IKCONFIG_PROC`).

### [ternary]

This section lists kernel symbols that must be in one of three states - built-in, built-as-module, or not-built. You can
specify one or more values for a given symbol (for example, if a symbol may be either built-in or as a module, so long
as it's enabled).

```
CONFIG_DRM_RADEON = YM
```

Additionally, a symbol may be listed with no arguments, in which case it is assumed a requirement is simply "enabled".

### [string]

Config symbols that must have a specific string value are listed here in the same format as above:

```
CONFIG_INITRAMFS_COMPRESSION=.xz
```

## Future

I hope to introduce some level of integration into (some) package managers such that required kernel symbols as
specified by installed packages can be automatically recorded into the config file. This, however, will likely be met
with varying levels of success, depending on the way package managers list kernel configuration requirements.