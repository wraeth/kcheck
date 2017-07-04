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
`/etc/kcheck.conf`, or you can specify the config file path at runtime with `kcheck --config /path/to/config ...`.

See `./setup.py --help` for other options.

## Usage

`kcheck` has two main operating modes: checking kernel .config files for required symbols, and using the package manager to generate a list of required symbols.

### Generating config

Usage of `kcheck` is pretty straightforward:

To generate a list of required symbols, run `kcheck` in the `genconfig` mode. Optionally specify which package manager to use, or use `--list` to list available ones. At present only Portage is supported, but others may be added at a later date.

Note that the `--output` argument is required - `kcheck` does not write back to the master configuration file as this would lose any existing comments.

```
$ kcheck genconfig -o /tmp/kcheck.conf
2 discovered required symbol(s) written to /tmp/kcheck.conf.
```

Once the found symbols have been added to the temporary config, add these to your master config `/etc/kcheck.conf`.

### Manually listing symbols

Edit the config file `kcheck.conf` to add the kernel symbol names and their required values. This file is reasonably
well documented, but in short, there are three sections: `[system]`, `[ternary]`, and `[string]`.

Kernel symbols listed in the config file may be upper or lowercase, may keep or omit the prefix `CONFIG_`, and may
specify valid values or none to default to "enabled" (`Y` or `M`).

#### [system]

The system section contains configuration items for the running of `kcheck` itself. Any log-format option specified on
the command line can be set in this section.

```
kernel = /proc/config.gz
```

Note that `kcheck` also supports reading from gzip-compressed kernel configs (as in those included via
`CONFIG_IKCONFIG_PROC`).

#### [ternary]

This section lists kernel symbols that must be in one of three states - built-in, built-as-module, or not-built. You can
specify one or more values for a given symbol (for example, if a symbol may be either built-in or as a module, so long
as it's enabled).

```
CONFIG_DRM_RADEON = YM
```

Additionally, a symbol may be listed with no arguments, in which case it is assumed a requirement is simply "enabled".

#### [string]

Config symbols that must have a specific string value are listed here in the same format as above:

```
CONFIG_INITRAMFS_COMPRESSION=.xz
```

### Checking symbols

Running the utility with no arguments, by default, checks for symbols listed in the master config in the kernel .config file. By default it will only list incorrect or missing symbols, but `--verbose` will give more informative output.

```
kcheck -v
Reading symbols...
9 required symbols loaded from config
3459 kernel symbols loaded from /usr/src/linux/.config

CONFIG_INOTIFY_USER matches allowed value(s)
CONFIG_X86 matches allowed value(s)
CONFIG_CIFS matches allowed value(s)
CONFIG_DRM_I915 matches allowed value(s)
CONFIG_SND_HDA_PREALLOC_SIZE matches allowed value(s)

The following config symbols have incorrect values:
    CONFIG_USER_NS set to IS NOT SET when it should be ['Y', 'M']
    CONFIG_USB_PRINTER set to IS NOT SET when it should be ['Y', 'M']
    CONFIG_FW_LOADER_USER_HELPER set to Y when it should be ['N']
    CONFIG_SYSFS_DEPRECATED set to IS NOT SET when it should be ['Y', 'M']
```

## Future

 - More readable output
 - Better portage integration
   - eg. symbols set in variables before calling helpers
 - Investigate/implement other PM integration (paludis?)
 - Hardware detection similar to the [Debian HCL
   list](http://kmuto.jp/debian/hcl/)

