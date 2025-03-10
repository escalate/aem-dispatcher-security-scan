[![Test](https://github.com/escalate/aem-dispatcher-security-scan/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/escalate/aem-dispatcher-security-scan/actions/workflows/test.yml)

# AEM Dispatcher Security Scan

A commandline tool to perfom an active security scan against a [AEM Dispatcher](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/dispatcher.html).

This tool tries to unify all known security relevant AEM Dispatcher URLs from the internet.

If you know some more URLs, please open a Github issue to report them.

## Usage

Build Docker image

```
$ make build-docker-image
```

Run Docker container from built image to print help

```
$ make run-docker-image

Usage: cli.py [OPTIONS]

  Commandline interface for AEM Dispatcher Security Scan

Options:
  --host TEXT        Set host of website. Leave empty to use default value: http://localhost:8080.  [required]
  --page-path TEXT   Set path of website. Leave empty to use default value: /content/geometrixx/en.
  --timeout INTEGER  Set timeout for http requests in seconds. Leave emtpy to use default value: 10.
  --help             Show this message and exit.
```

Run Docker container from built image with custom arguments

```
$ docker compose \
    --file docker-compose.yml \
    run \
    --rm \
    aem-dispatcher-security-scan \
    --host "https://www.adobe.com" \
    --page-path "/content/geometrixx/en"
```

## Development

Build and launch the [DevContainer](https://code.visualstudio.com/docs/devcontainers/containers) in [VSCode](https://code.visualstudio.com/).

## References

- [docs.adobe.com](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/configuring/dispatcher-configuration.html#testing-dispatcher-security)
- [0ang3el/aem-hacker](https://github.com/0ang3el/aem-hacker)
- [emadshanab/Adobe-Experience-Manager](https://github.com/emadshanab/Adobe-Experience-Manager)
- [danielmiessler/seclists](https://github.com/danielmiessler/SecLists)
- [aem-design/ansible-role-aem-security-test](https://github.com/aem-design/ansible-role-aem-security-test)
- [cognifide/securecq](https://github.com/Cognifide/SecureCQ)
- [perficientdigital.com](https://blogs.perficientdigital.com/2019/01/10/mastering-aem-dispatcher-part-7-securing-the-dispatcher/)
- [infosecinstitute.com](https://resources.infosecinstitute.com/adobe-cq-pentesting-guide-part-1/)

## License

MIT
