# musescore-rip
This (very limited) python script attempts to retrieve sheet music from musescore.com given a specific URL. It fails in many circumstances.
## Installation
Clone the repository and install necessary dependences (see `requirements.txt`).
## Usage
`python3 main.py <musescore url> [nocleanup]`
Produced files will be placed in `downloads/` within a subdirectory which will be printed to the terminal upon completion. By default, the only file preserved will be a combined pdf. If you would like to keep the svg and png files retrieved in the process, include the optional `nocleanup` flag.