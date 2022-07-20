
import sys

sys.path.append("../..") 

import csv_handler as ch
from os import makedirs
import logging
import simpy
from tqdm import tqdm

from city import City
from infrastructure import Cloud, FogNode, Taxi, LinkWanDown, LinkWanUp, \
    LinkWifiTaxiToTrafficLight, LinkWifiBetweenTrafficLights, TrafficLight
from mobility import MobilityManager
from settings import SIMULATION_TIME, FOG_DCS, POWER_MEASUREMENT_INTERVAL, \
    FOG_IDLE_SHUTDOWN
from leaf.infrastructure import Infrastructure
from leaf.power import PowerMeter




def main(count_taxis: bool, measure_infrastructure: bool, measure_applications: bool):
    # ----------------- Set up experiment -----------------
    env = simpy.Environment()
    city = City(env)
    mobility_manager = MobilityManager(city)
    env.process(mobility_manager.run(env))

    # ----------------- Initialize meters -----------------
    if count_taxis:
        # Measures the amount of taxis on the map
        taxi_counter = TaxiCounter(env, city.infrastructure)
    if measure_infrastructure:
        # Measures the power usage of cloud and fog nodes as well as WAN and WiFi links
        pm_cloud = PowerMeter(entities=city.infrastructure.nodes(type_filter=Cloud), name="cloud", measurement_interval=POWER_MEASUREMENT_INTERVAL)
        pm_fog = PowerMeter(entities=city.infrastructure.nodes(type_filter=FogNode), name="fog", measurement_interval=POWER_MEASUREMENT_INTERVAL)
        pm_wan_up = PowerMeter(entities=city.infrastructure.links(type_filter=LinkWanUp), name="wan_up", measurement_interval=POWER_MEASUREMENT_INTERVAL)
        pm_wan_down = PowerMeter(entities=city.infrastructure.links(type_filter=LinkWanDown), name="wan_down", measurement_interval=POWER_MEASUREMENT_INTERVAL)
        pm_wifi = PowerMeter(entities=lambda: city.infrastructure.links(type_filter=(LinkWifiBetweenTrafficLights, LinkWifiTaxiToTrafficLight)), name="wifi", measurement_interval=POWER_MEASUREMENT_INTERVAL)

        env.process(pm_cloud.run(env))
        env.process(pm_fog.run(env))
        env.process(pm_wan_up.run(env))
        env.process(pm_wan_down.run(env))
        env.process(pm_wifi.run(env))
    if measure_applications:
        # Measures the power usage of the V2I and CCTV applications
        pm_v2i = PowerMeter(entities=lambda: [taxi.application for taxi in city.infrastructure.nodes(type_filter=Taxi)], name="v2i", measurement_interval=POWER_MEASUREMENT_INTERVAL)
        pm_cctv = PowerMeter(entities=lambda: [tl.application for tl in city.infrastructure.nodes(type_filter=TrafficLight)], name="cctv", measurement_interval=POWER_MEASUREMENT_INTERVAL)
        env.process(pm_v2i.run(env))
        env.process(pm_cctv.run(env))

    # ------------------ Run experiment -------------------
    env.run(until=360)

    # ------------------ Write results --------------------
    

    ch.output_csv(PM=pm_cloud, rename='Cloud',type = 1)
    ch.output_csv(PM=pm_fog, rename='Fog',type = 1)
    ch.output_csv(PM=pm_wan_up, rename='Wan up',type = 1)
    ch.output_csv(PM=pm_wan_down, rename='Wan down',type = 1)
    ch.output_csv(PM=pm_wifi, rename='WIFI',type = 1)

    ch.output_csv(PM=pm_v2i, rename='V2I',type = 2)
    ch.output_csv(PM=pm_cctv, rename='CCTV',type = 2)

    ch.merge_results()

class TaxiCounter:
    def __init__(self, env: simpy.Environment, infrastructure: Infrastructure):
        self.env = env
        self.measurements = []
        self.process = env.process(self._run(infrastructure))

    def _run(self, infrastructure: Infrastructure):
        yield self.env.timeout(0.01)
        while True:
            self.measurements.append(len(infrastructure.nodes(type_filter=Taxi)))
            yield self.env.timeout(1)


if __name__ == '__main__':
    main(count_taxis=True, measure_infrastructure=True, measure_applications=True)
