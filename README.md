# Jupiter Ace TAP/TZX to WAV/DAT/CD conversion tools

These tools allow TAP and TZX files for the Jupiter Ace to be converted to WAV files, which can in turn be recorded onto DAT tape, audio cassette or CD.

MAME's `castool` tool is used to perform the TAP-to-WAV conversion.

DAT recording requires a SCSI DAT/DDS drive with SGI audio firmware (e.g. Archive/Conner/Seagate Python or Peregrine), and the `wdat` tool (http://www.hoxnet.com/dat-tools/)

`tap2tzx.py` reads a TZX file (e.g. from the www.jupiter-ace.co.uk archive) and converts it to a TAP file. This is required because MAME's `castool`

## Notes on Jupiter Ace audio levels

Audio levels on the Ace are quite touchy. Use the headphone output of the deck: a line-out will not output enough voltage.

  - Start with the volume set about half-way.
  - If the volume is too low, the Ace won't detect the header blocks. Increase the volume.
  - If the volume is too high (or possibly too low), the Ace will report tape loading errors (`ERROR 10`).

Note that `ERROR 10` is a general tape loading error. In addition to audio level issues, `ERROR 10` also appears if the program being loaded is too large for the available memory. You may need to connect a RAM pack to the Ace.

