"""Application exporter"""

import asyncio
import os
import time
from prometheus_client import start_http_server, Enum
from checker import Checker


class AppMetrics:

    def __init__(self, fetchingInterval=5, targetHost="https://ase.in.tum.de/lehrstuhl_1/"):
        self.status = Enum("googleFonts", "Metric indicating if the target webste requests Google Fonts", states=[
                           "ok - no requests detected", "requests detected"])
        self.fetchingInterval = fetchingInterval
        self.targetHost = targetHost
        self.checker = Checker(self.targetHost)

    async def run_metrics_loop(self):
        """Metric fetching loop"""

        while True:
            await self.fetch()
            time.sleep(self.fetchingInterval)

    async def fetch(self):
        """
        Check for if the target hosts requests fonts form Google and refresh Prometheus metric with new values.
        """

        await self.checker.main()
        self.status.state(
            "requests detected" if self.checker.googleFontsFound else "ok - no requests detected")


async def main():
    """Main entry point"""

    fetchingInterval = int(os.getenv("FETCHING_INTERVAL_SECONDS", "5"))
    exporterPort = int(os.getenv("EXPORTER_PORT", "9877"))
    targetHost = os.getenv("TARGET_WEBSITE")

    app_metrics = AppMetrics(
        fetchingInterval=fetchingInterval,
        targetHost=targetHost
    )
    start_http_server(exporterPort)
    await app_metrics.run_metrics_loop()

if __name__ == "__main__":
    asyncio.run(main())
