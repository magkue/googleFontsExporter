# googleFontsExporter
Simple Prometheus exporter for Websites, to check if they are requesting Google Fonts. 

# Installation
Use [docker-compose](https://docs.docker.com/compose/install/) to setup the expoter.
Add websites you want to monitor to the `configFile/targets.txt` file (one line per website url).

```bash
export CONFIG_FILE=targets.txt
docker-compose up -d
```

# Update monitored websites
Stop and remove the container and adjust the `configFile/targets.txt` file. Then restart the exporter.

```bash
export CONFIG_FILE=targets.txt
docker-compose down

docker-compose up -d
```

## Contributing

Pull requests are welcome.

## License

[MIT](https://choosealicense.com/licenses/mit/)
