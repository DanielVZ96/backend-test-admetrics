# ConvCLPUSD
> An API that converts between CLP and USD.

ConCLPUSD is a django service that with a bit of help from webscrapping, mantains and exposes a database of historical
rates data between the chilean peso(CLP) and the US dollar(USD).

It grabs the data every morning at about 9:35 am from the chilean tax administration and updates the database for the 
current date.


## Installation

Create virtualenv (recommended):
```
$ pip install virtualenv
$ virtualenv <target dir>
$ source <target dir>/bin/activate
```

Requirements:

```sh
$ pip install requirements.txt
```

Create database:
```
(in proyect root)$ python manage.py migrate
```

Windows:

```sh
edit autoexec.bat
```

## Usage example



## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Release History

* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

## Meta

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


