# Jack saver

## About

Jack saver is a terminal screen saver based on the curses library

## How to build and run ?

1. Get a python environment (version >= 3.9)
2. Install the dependencies
```bash
python3 -m pip install -r requirements.txt
```
3. Run the script named `jacksaver.py`

## Docker

Build the image and run it by name

```bash
docker build -t jack_saver .
docker run -it -d jack_saver
```

## Flags

```bash
usage: jacksaver.py [-h] [-c COUNT] [-x SPRITE_PER_THREAD] [-s SCHEMA]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Amount of pet
  -x SPRITE_PER_THREAD, --sprite_per_thread SPRITE_PER_THREAD
                        Amount of sprite managed by a single thread
  -s SCHEMA, --schema SCHEMA
                        Schema that describe which pet will spawn
```
