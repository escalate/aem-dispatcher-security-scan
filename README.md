# AEM Dispatcher Security Scan

A commandline tool to perfom an active security scan against a [AEM Dispatcher](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/dispatcher.html).

This tool tries to unify all known security relevant AEM Dispatcher URLs from the internet.

If you know some more URLs, please open a Github issue to report them.

## Usage

### Docker

Start using scanner with minimal effort. Docker images are available in the [Docker Hub](https://hub.docker.com/repository/docker/daspicko/aem-dispatcher-scanner/general).

Run AEM Dispatcher Scanner as Docker container with default settings

```bash
$ docker run daspicko/aem-dispatcher-scanner:latest --host http://localhost:8080 
```

Run Docker container with arguments

```bash
$ docker run daspicko/aem-dispatcher-scanner:latest \
    --website-url "http://www.adobe.com" \
    --page-path "/content/geometrixx/en" \
    --timeout 10
```

##### Build local Docker image
If for some reason you want to use local image, build image using
```bash
$ ./aem-dispatcher-scanner.sh
```

### Local development
If you want to customize code or run scanner directly on your machine using Python, setup local environment. Setup use Conda or Virtual environment to install all dependencies.

##### How to use
In the repository you can find a handling script:
```bash
$ ./aem-dispatcher-scanner.sh
```
Run the setup script and choose: `1. Setup (Clean) environment`. Required to be done only once. Once it is completed, you can simply activate it.
    
###### Activate virtual environment: 
If you are using conda:
```bash
conda activate "$(pwd)/.venv"
```
otherwise use
```bash
source .venv/bin/activate
```
###### Deactivate virtual environment:
Once you are done with development, you can deactiveate virtual environment: 
If you are using conda:
```bash
conda deactivate
```
otherwise use
```bash
deactivate
```

##### Starting scanner

Tested with Python 3.12.x on Ubuntu 22.04

If you encounter issues with 3.12.x patch versions of Python, please open a Github issue.

```bash
$ ./scan.py --help

Usage: scan.py [OPTIONS]

    Commandline interface for AEM Dispatcher Security Scan

Options:
    --website-url TEXT        Set URL of website e.g. http://www.adobe.com [required]
    --page-path TEXT  Set path of website page e.g. /content/geometrixx/en
    --timeout FLOAT           Set timeout for http requests in secs e.g. 1.5 or 5
    --help                    Show this message and exit.
```

## Dependencies

* [click](https://pypi.python.org/pypi/click)
* [requests](https://pypi.python.org/pypi/requests)

## References

* [docs.adobe.com](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/configuring/dispatcher-configuration.html#testing-dispatcher-security)
* [0ang3el/aem-hacker](https://github.com/0ang3el/aem-hacker)
* [emadshanab/Adobe-Experience-Manager](https://github.com/emadshanab/Adobe-Experience-Manager)
* [danielmiessler/seclists](https://github.com/danielmiessler/SecLists)
* [aem-design/ansible-role-aem-security-test](https://github.com/aem-design/ansible-role-aem-security-test)
* [cognifide/securecq](https://github.com/Cognifide/SecureCQ)
* [perficientdigital.com](https://blogs.perficientdigital.com/2019/01/10/mastering-aem-dispatcher-part-7-securing-the-dispatcher/)
* [infosecinstitute.com](https://resources.infosecinstitute.com/adobe-cq-pentesting-guide-part-1/)

## License

MIT
