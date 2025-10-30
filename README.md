[![Test](https://github.com/escalate/aem-dispatcher-security-scan/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/escalate/aem-dispatcher-security-scan/actions/workflows/test.yml)

# AEM Dispatcher Security Scan

A commandline tool to perform an security scan against a [AEM Dispatcher](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/dispatcher.html).

This tool tries to unify all known security relevant AEM Dispatcher URLs from the internet.

If you know some more URLs, please open a [GitHub issue](https://github.com/escalate/aem-dispatcher-security-scan/issues/new) to report them.

## 📚 Usage

1. Build the Docker image.

```
$ make build-docker-image
```

2. Run Docker container from built image to print help.

```
$ make run-docker-image

Usage: cli.py [OPTIONS]

  AEM Dispatcher Security Scan

Options:
  --url TEXT         URL of website e.g. https://www.example.com  [required]
  --page-path TEXT   Page path of website. e.g. /content/geometrixx/en (Default: /)
  --timeout INTEGER  Timeout for HTTP requests in seconds. (Default: 10)
  --file PATH        Text file with test paths. (Default: aem-sec-paths.txt)
  --help             Show this message and exit.
```

3. Run Docker container from built image with custom arguments.

```
$ docker compose \
    --file docker-compose.yml \
    run \
    --rm \
    aem-dispatcher-security-scan \
    --url=https://www.example.com \
    --page-path=/content/geometrixx/en
```

## 🧩 References

- [docs.adobe.com](https://docs.adobe.com/content/help/en/experience-manager-dispatcher/using/configuring/dispatcher-configuration.html#testing-dispatcher-security)
- [0ang3el/aem-hacker](https://github.com/0ang3el/aem-hacker)
- [emadshanab/Adobe-Experience-Manager](https://github.com/emadshanab/Adobe-Experience-Manager)
- [danielmiessler/seclists](https://github.com/danielmiessler/SecLists)
- [aem-design/ansible-role-aem-security-test](https://github.com/aem-design/ansible-role-aem-security-test)
- [cognifide/securecq](https://github.com/Cognifide/SecureCQ)
- [perficientdigital.com](https://blogs.perficientdigital.com/2019/01/10/mastering-aem-dispatcher-part-7-securing-the-dispatcher/)
- [infosecinstitute.com](https://resources.infosecinstitute.com/adobe-cq-pentesting-guide-part-1/)

## 🤝 Contributing

We welcome contributions of all kinds 🎉.

Please read our [Contributing](https://github.com/escalate/aem-dispatcher-security-scan/blob/master/CONTRIBUTING.md) guide to learn how to get started, submit changes, and follow our contribution standards.

## 🌐 Code of Conduct

This project follows a [Code of Conduct](https://github.com/escalate/aem-dispatcher-security-scan/blob/master/CODE_OF_CONDUCT.md) to ensure a welcoming and respectful community.

By participating, you agree to uphold this standard.

## 🐛 Issues

Found a bug or want to request a feature?

Open an issue here: [GitHub Issues](https://github.com/escalate/aem-dispatcher-security-scan/issues)

## 🧪 Development

Development is possible via an interactive Docker container in [VSCode](https://code.visualstudio.com/).

1. Build and launch the [DevContainer](https://code.visualstudio.com/docs/devcontainers/containers) in VSCode.

2. Initiate the Python Virtual Environment via `poetry env activate` in the terminal.

3. Run test suite via `pytest` in the terminal.

## 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](https://github.com/escalate/aem-dispatcher-security-scan/blob/master/LICENSE) file for details.
