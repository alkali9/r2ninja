# R2Ninja (v1.0 alpha)
Author: **Austin Emmitt (NowSecure)**
_A plugin to interact with radare2 from binaryninja._
## Description:
This plugin allows binaryninja to interact with radare2. There are shortcuts to decompiling, syncing symbols, and managing zignatures

## Usage:

After a binary has been analyzed, run *Initialize r2ninja*. All UI commands will output to the log.

[[https://raw.githubusercontent.com/alkali9/r2ninja/master/usage.png|alt=usage]]

Currently supported commands include:

* Initialize r2ninja, this needs to be the first thing ran, as well as after switching binaries
* Execute r2 command - Executes r2 command
* Save r2 project - Saves an r2 project, currently with a default name of *file*-r2bn
* Load r2 project - Loads an r2 project
* Save r2 zignatures - Saves an r2 zig file
* Load r2 zignatures - Loads an r2 zig file
* Seek r2 to address - Sets the current address in r2
* Decompile with r2dec - Decompiles function with r2dec, a pseudocode decompiler plugin for r2
* Disassemble with r2 - Disassembles function with r2, useful for contrasating disassemblies
* Sync symbols - Sync symbols with r2, only does import and functions for right now

Additionally r2 can be ran interactively in the script console by running *import r2ninja; r2ninja.interactive()*. The instance of r2 in this console is the same as the one in the UI, so they will be synchronized. 

## Minimum Version

This plugin requires the following minimum version of Binary Ninja:

 * release - 9999
 * dev - 1.0.dev-576


## Required Dependencies

The following dependencies are required for this plugin:

 * pip - r2pipe
 * installers - 
 * other - r2, r2dec
 * apt - 


## License
This plugin is released under a [MIT](LICENSE) license.

