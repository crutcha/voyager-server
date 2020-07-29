from celery import shared_task
from voyager_server.probes.models import ProbeResult, ProbeHop, PrefixInfo
import requests
import re
import ipaddress
import time


@shared_task
def ip_api_info(ip: str) -> None:
    response = requests.get(f"http://ip-api.com/json/{ip}")
    print(response.json())


@shared_task()
def process_probe_result(probe_uuid: str) -> None:
    """ async post_signal handler to fire off probe hop data enrichment. """

    # Placing a countdown on the task from the signal delays the return to caller by the
    # countdown amount, so instead we will put a sleep here to avoid potential race condition
    # between celery consumer and django post_save DB commit.
    time.sleep(5)

    result = ProbeResult.objects.get(id=probe_uuid)
    for hop in result.hops.all():
        process_hop_result.delay(hop.id)


@shared_task()
def process_hop_result(pk: int) -> None:
    hop = ProbeHop.objects.get(id=pk)

    # Ignore timeouts
    if not hop.ip:
        return

    existing_prefix = PrefixInfo.objects.filter(prefix__net_contains=hop.ip)

    if existing_prefix:
        hop.prefix = existing_prefix
        hop.save()

    # Private prefixes may or may not be populated....
    elif not existing_prefix and not ipaddress.ip_address(hop.ip).is_private:

        # We can use this API to determine ASN then persist into database based on data from
        # BGPView API.
        ip_info = requests.get(f"http://ip-api.com/json/{hop.ip}").json()
        asn = re.match("AS(\d+)\s.*", ip_info["as"]).groups()[0]
        asn_info = requests.get(f"https://api.bgpview.io/asn/{asn}/prefixes").json()
        for prefix in asn_info["data"]["ipv4_prefixes"]:
            PrefixInfo.objects.create(
                asn=asn,
                prefix=prefix["prefix"],
                name=prefix["name"],
                description=prefix["description"],
                country_code=prefix["country_code"],
                rir=prefix["parent"]["rir_name"],
            )
