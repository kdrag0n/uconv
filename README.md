# uconv

A flexible and extensible unit converter written in Python for GCI 2019.

## Requirements

An installation of Python 3.6 or newer is required.

## Usage

The program accepts 3 command-line arguments: the amount to convert, the unit
given amount is in, and the unit to convert the given amount into. There is no
need to specify a category as the program uses a graph-based path-finding
algorithm to find the shortest possible path between any two arbitrary units,
should such a path exist. Impossible conversions, such as kilometers to watts
(distance to power), will result in an error.

Example commands:

- Windows: `python uconv.py 1 in cm`
- Unix-likes: `./uconv.py 1 in cm`

Example usage:

```
❯ ./uconv.py 1 in cm  
1 inch => 2.54 centimeters
```

There is also a debug mode which can be activated with the `-d` argument that
shows the path-finding and conversion process:

```
❯ ./uconv.py -d 1 century ns
Found conversion path: 1 century -> 100 years, 1 year -> 365.25 days, 1 day -> 24 hours, 1 hour -> 60 minutes, 1 minute -> 60 seconds, 1 second -> 1,000 milliseconds, 1 millisecond -> 1,000 microseconds, 1 microsecond -> 1,000 nanoseconds
Converting 1 century -> 100 years
Converting 100 years -> 36,525 days
Converting 36,525 days -> 876,600 hours
Converting 876,600 hours -> 52,596,000 minutes
Converting 52,596,000 minutes -> 3,155,760,000 seconds
Converting 3,155,760,000 seconds -> 3,155,760,000,000 milliseconds
Converting 3,155,760,000,000 milliseconds -> 3,155,760,000,000,000 microseconds
Converting 3,155,760,000,000,000 microseconds -> 3,155,760,000,000,000,000 nanoseconds
1 century => 3,155,760,000,000,000,000 nanoseconds
```

Help regarding usage is available with the `-h` or `--help` arguments should you
ever be left stranded.

## Custom Units

Custom units can be added easily by editing the `units.toml` file, which is
written in [TOML](https://learnxinyminutes.com/docs/toml/) — a simple and standardized configuration format. Everything is documented thoroughly by
comments in the file. Blatantly incorrect data, such as invalid syntax or
duplicate units, will be detected and reported when the file is being parsed.
