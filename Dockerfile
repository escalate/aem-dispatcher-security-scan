# Dockerfile for the AEM Security Scanner CLI

FROM python:3.12-alpine

LABEL maintainer="Felix Boerner <ich@felix-boerner.de>"

COPY requirements.txt /app/
COPY aem-sec-paths.txt /app/

COPY scan.py /app/
COPY security_scanner.py /app/
COPY security_scan_status.py /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/app/scan.py"]
CMD ["--help"]
