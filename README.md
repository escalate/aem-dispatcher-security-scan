# AEM Dispatcher Security Scan

A commandline tool to perfom an active security scan against a [AEM Dispatcher](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/dispatcher.html)

## Usage
```
$ ./scan.py --help

Usage: scan.py [OPTIONS]

  Commandline interface for AEM Dispatcher Security Scan

Options:
  --website-url TEXT        Set URL of website e.g. http://www.adobe.com
                            [required]
  --website-page-path TEXT  Set path of website page e.g. /content/geometrixx/en
  --verbose                 Enable verbose logging output
  --help                    Show this message and exit.
```

## Installation

Tested with Python 3.6.x on Ubuntu 18.04

If you encounter issues with 3.6.x patch versions of Python, please open a Github issue.

### Install needed requirements

```
make requirements
```

### Run tool from commandline

```
$ ./scan.py
```

## Docker

### Build Docker image

```
$ make build
```

### Run Docker container from built image

```
$ docker run scan
```

### Run Docker container from built image with arguments

```
$ docker run scan \
    --website-url "http://www.adobe.com"
    --website-page-path "/content/geometrixx/en"
    --verbose
```

## Dependencies
* [click](https://pypi.python.org/pypi/click)
* [requests](https://pypi.python.org/pypi/requests)

## References
* [docs.adobe.com](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/configuring/dispatcher-configuration.html#testing-dispatcher-security)
* [0ang3el/aem-hacker](https://github.com/0ang3el/aem-hacker)
* [danielmiessler/SecLists](https://github.com/danielmiessler/SecLists)
* [aem-design/ansible-role-aem-security-test](https://github.com/aem-design/ansible-role-aem-security-test)

## License
MIT
