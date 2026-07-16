# rainmeter

[![License: CC BY-NC-SA 4.0](https://img.shields.io/github/license/hanpeter/rainmeter)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub tag](https://img.shields.io/github/v/tag/hanpeter/rainmeter?logo=github)](https://github.com/hanpeter/rainmeter/tags)
[![GitHub release](https://img.shields.io/github/v/release/hanpeter/rainmeter?logo=github)](https://github.com/hanpeter/rainmeter/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/hanpeter/rainmeter/total?logo=github)](https://github.com/hanpeter/rainmeter/releases)
[![Last commit](https://img.shields.io/github/last-commit/hanpeter/rainmeter?logo=github)](https://github.com/hanpeter/rainmeter/commits)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows)](https://www.rainmeter.net)
[![Rainmeter 4.5+](https://img.shields.io/badge/Rainmeter-4.5%2B-00AEEF)](https://www.rainmeter.net)

Personal collection of minimalist Rainmeter system-monitor skins for CPU, GPU, memory, and network.

## Table of Contents

- [Purpose](#purpose)
- [Installation](#installation)
  - [Option 1: Install the Packaged Skin](#option-1-install-the-packaged-skin)
  - [Option 2: Install from Source](#option-2-install-from-source)
- [Usage](#usage)
  - [Loading a Skin](#loading-a-skin)
  - [Customization](#customization)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## Purpose

`rainmeter` is a set of Rainmeter skins that display live system metrics in a clean, minimal
style. Each category ships a `Combo` skin showing all its metrics together, plus individual
skins for placing metrics separately.

| Category | Skins |
|---|---|
| CPU | `Combo`, `Usage`, `Temperature`, `Fan` |
| GPU | `Combo`, `Usage`, `Temperature`, `Fan` |
| Memory | `Combo`, `Percentage`, `Bytes` |
| Network | `Combo`, `Download`, `Upload` |

## Installation

### Option 1: Install the Packaged Skin

Download the latest `.rmskin` from [Releases](https://github.com/hanpeter/rainmeter/releases/latest)
and double-click it to install via the Rainmeter Skin Installer. Requires Rainmeter 4.5.0+ on
Windows 11+.

### Option 2: Install from Source

Clone this repository into your Rainmeter `Skins` folder, then refresh Rainmeter:

```bash
git clone https://github.com/hanpeter/rainmeter.git "%USERPROFILE%\Documents\Rainmeter\Skins\rainmeter"
```

## Usage

### Loading a Skin

Open **Rainmeter → Manage → Skins**, expand a category folder, and load a `.ini`. Load a
`Combo` skin for the all-in-one view (e.g. `CPU\Combo.ini`), or load the individual skins
(`Usage`, `Temperature`, `Fan`, …) to position each metric separately.

### Customization

Shared colors, background size/color, and calculation constants live in
`@Resources/variables.ini`. Edit it and refresh Rainmeter to restyle all widgets at once.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. CI runs a build
(packages the `.rmskin`) and a lint check (`.github/scripts/rainmeter_lint.py`) on every PR,
so keep skins lint-clean.

## Credits

:warning: This skin is heavily based on [Win10 Widgets](http://win10widgets.com) by
[TJ Markham](http://tjmarkham.com).

## License

Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
