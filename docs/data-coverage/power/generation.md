# Generation

Generation data can be accessed on the TransionZero platform through the [Python Client](https://github.com/transition-zero/tz-client) and [API](https://api.feo.transitionzero.org/latest/docs).

This data is continuously collected from various sources and can be accessed through any of TransitionZero's designated Nodes.

### Background

A power plant consists of units. What a unit consists of depends on the fuel and technology type of the unit. A coal unit, for example, will consist of a boiler and turbine and multiple units usually make up a single coal power station. A wind unit may consist of multiple individual turbines.

These units can be individually turned off and on. Not all units will necessarily always be generating power when a plant is on. Generation is a measure of how much electricity a unit is generating at a specific point in time. This can be anywhere between 0 (the unit is not generating any power) and the installed maximum nameplate capacity of the plant, available from our power asset-level data set.

The capacity in MW is the maximum amount of power a unit will ever be able to generate. Power units rarely operate at maximum capacity and the maximum capacity a unit is capable of can degrade over time. We give the nameplate capacity of a power unit which is usually determined by the manufacturer. Generation (in MW) is how much power is being produced by a unit at a specific point in time. For example, a coal unit with a capacity of 200 MW has a generation of 100 MW at 11:30 on 12 Nov 2020 because its utilisation is only at 50% at that point in time.

Additional units can be added to a plant as time goes on or retired. When these units came online and if they are still operational is available in our power assets data set.

## Sources

Currently, our platform supports unit level generation data from European Network of Transmission System Operators for Electricity (ENTSO-E).

### ENTSO-E Europe

ENTSO-E publishes generation data for the European power system. This data is collected by ENTSO-E from transmission system operations, power exchanges, and other qualified third parties.

Generation data is available for individual generating units with a minimum installed capacity of 100 MW across 35 countries:

> Albania, Austria, Bosnia and Herzegovina, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Latvia, Lithuania, Luxembourg, North Macedonia, Montenegro, Netherlands, Norway, Poland, Portugal, Romania, Serbia, Slovakia, Slovenia, Spain, Sweden, Switzerland, and United Kingdom.

Generation readings are available at resolutions of 60, 30, or 15 minutes.

Earliest available date: December 6, 2014

## Methodology

Generation data for individual power plant units is regularly collected from the ENTSO-E Transparency platform. The data is then cleaned and matched to the power units available in the TransitionZero platform. This allows the retrieval of generation data for a given asset in Europe.

During the matching process, the name, capacity, fuel type, and location of units from ENTSO-E are compared to the corresponding fields in our power asset dataset by our analysts. In some cases, there is a many-to-one match between units in the two datasets due to different conflicting definitions of a single power “unit” in the source data. In the case of many-to-one matches, one of the following actions is taken:

- If multiple ENTSO-E units map to a single TransitionZero unit, the generation data is aggregated for these units.
- In the special case where a single ENTSO-E unit is separated into multiple units in TransitionZero's dataset, the given generation value is evenly split between these units in the TransitionZero platform.

### Coverage

So far,~80% of all the generation unit IDs in ENTSO-E are matched to the power units in our asset dataset. We have only included ENTSO-E units that we have matched to a corresponding unit in our power asset dataset. Therefore, the complete records from ENTSO-E are not yet available.

## Coming soon

We are planning on adding generation data for different geographies in the coming months.

Please contact [power-data-team@transitionzero.org](mailto:power-data-team@transitionzero.org) for any questions regarding this data.
