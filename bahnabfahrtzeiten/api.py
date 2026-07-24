import aiohttp
import json

import logging

from datetime import datetime

_LOGGER = logging.getLogger(__name__)


def get_headers(next):
    return {
        "Accept": "text/x-component",
        "Origin": "https://www.bahnhof.de",
        "Next-Action": next,
        "Content-Type": "text/plain;charset=UTF-8",
    }


async def get_bahnhof(session, name) -> str | None:
    headers = get_headers("7fb817bd1a919512e60c7b11efc4733d990209bf8d")

    async with session.post(
        f"https://www.bahnhof.de/suche", headers=headers, data=f'["{name}"]'
    ) as resp:
        resp.raise_for_status()
        output = await resp.text()
        _LOGGER.error(f"Search response {output}")
        output = output[output.index("1:") + 2 :]
        data = json.loads(output)
        return (data[0]["slug"], data[0]["name"])


async def get_eva_number(session, bahnhof) -> str | None:
    async with session.get(f"https://www.bahnhof.de/{bahnhof}/abfahrt") as resp:
        resp.raise_for_status()
        text = await resp.text()
        if "bf:evaNumbers" not in text:
            _LOGGER.error(f"Could not find eva number for bahnhof {bahnhof}")
            return None
        # extract the eva number from the meta tag
        start = text.index('bf:evaNumbers" content="') + len('bf:evaNumbers" content="')
        if start < 0:
            _LOGGER.error(
                f"The eva Number for bahnhof {bahnhof} could not be found in the response text, because the expected string 'bf:evaNumbers\" content=\"' was not found."
            )
            return None
        end = text.index('"', start)
        eva_number = text[start:end]
        _LOGGER.info(f"Found eva number {eva_number} for bahnhof {bahnhof}")
        return eva_number


class BahnAbfahrtzeitenClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        bahnhof: str,
        eva_number: str | None,
        max_results: int,
    ):
        self._session = session
        self._bahnhof = bahnhof.lower()
        self._eva_number = eva_number
        self._max_results = max_results

    async def get_status(self):
        if self._eva_number is None:
            _LOGGER.warning("Eva number is None, calling test_connection() to get it.")
            await self.test_connection()

        headers = get_headers("7f224b883c4a036854b93606d3611b94aebb8ae93b")

        bahn_payload = [
            {
                "duration": 180,
                "type": "departures",
                "locale": "de",
                "evaNumbers": [self._eva_number],
                "additionalEvaNumbers": [],
                "excludeEvaNumbers": [],
                "stationCategory": 5,
                "filterTransports": [
                    "HIGH_SPEED_TRAIN",
                    "INTERCITY_TRAIN",
                    "INTER_REGIONAL_TRAIN",
                    "REGIONAL_TRAIN",
                    "CITY_TRAIN",
                ],
                "sortBy": "TIME_SCHEDULE",
            }
        ]
        async with self._session.post(
            f"https://www.bahnhof.de/{self._bahnhof}/abfahrt",
            headers=headers,
            json=bahn_payload,
        ) as resp:
            resp.raise_for_status()
            output = await resp.text()
            output = output[output.index("1:") + 2 :]
            data = json.loads(output)
            values = []
            for entry in data["entries"][0 : self._max_results]:
                entry = entry[0]
                try:
                    scheduled_time = datetime.strptime(
                        entry["timeSchedule"], "%Y-%m-%dT%H:%M:%S%z"
                    ).strftime("%H:%M")
                except ValueError:
                    scheduled_time = "XX:XX"
                try:
                    delayed_time = datetime.strptime(
                        entry["timeDelayed"], "%Y-%m-%dT%H:%M:%S%z"
                    ).strftime("%H:%M")
                except ValueError:
                    delayed_time = "XX:XX"
                train = {
                    "scheduled_time": scheduled_time,
                    "delayed_time": delayed_time,
                    "delayed": entry["delayed"],
                    "destination": entry["destination"]["name"],
                    "canceled": entry["canceled"] or entry["stopPlace"]["canceled"],
                }
                values.append(train)
            return values
