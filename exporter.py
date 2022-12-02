"""Application exporter"""

import asyncio
import os
import time
from prometheus_client import CollectorRegistry, start_http_server, Gauge
from checker import Checker


class Exporter:

    def __init__(self, fetchingInterval=5, targetHosts=""):
        # for targetHost in targetHosts:
        self.gauge = Gauge("googleFontsFound", "Metric indicating if target requests Google Fonts", labelnames=[
                           "exporter", "target"])
        #    gauge.labels("googleFontsExporter", targetHost)
        #    self.status[targetHost] = gauge

        self.fetchingInterval = fetchingInterval
        self.targetHosts = targetHosts
        self.checker = Checker(self.targetHosts)

    async def run(self):
        """Metric fetching loop"""

        while True:
            await self.fetch()
            time.sleep(self.fetchingInterval)

    async def fetch(self):
        """
        Check for if the target hosts requests fonts form Google and refresh Prometheus metric with new values.
        """

        await self.checker.main()
        for targetHost in self.targetHosts:
            self.gauge.labels("googleFontsExporter", targetHost).set(
                self.checker.googleFonts[targetHost])


async def main():
    """Main entry point"""

    fetchingInterval = int(os.getenv("FETCHING_INTERVAL_SECONDS", "5"))
    exporterPort = int(os.getenv("EXPORTER_PORT", "9877"))
    targetHosts = []
    with open("./configFile/targets.txt", 'r') as file:
        targetHosts = file.read().split("\n")

    print(targetHosts)
    if len(targetHosts) == 0:
        raise RuntimeError("Empty targetFile!")
    exporter = Exporter(
        fetchingInterval=fetchingInterval,
        targetHosts=targetHosts
    )
    start_http_server(exporterPort)
    await exporter.run()

if __name__ == "__main__":
    asyncio.run(main())
