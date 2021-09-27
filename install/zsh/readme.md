# ZSH Installation

# Issues

## Locale

Error:

```
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
    LANGUAGE = (unset),
    LC_ALL = "zh_TW.UTF-8",
    LC_LANG = "zh_TW.UTF-8",
    LANG = "zh_TW.UTF-8"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
```

Solution:

Run `dpkg-reconfigure locales` and generate desired locale files.

Note: The `dpkg-reconfigure` command is in the `locales` package.

Then specify locales like: `export LC_ALL="en_US.UTF" && export LANG="en_US.UTF-8"`
