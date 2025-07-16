# Synthetic Denver

The goal of this population is to be used for testing by the [Childhood Obesity Data Initiative](https://www.cdc.gov/obesity/initiatives/codi/childhood-obesity-data-initiative.html) (CODI) project. It is comprised of 6,357 simulated child patients residing in Colorado.

* Represents an approximately 1 / 100th simulation of Denver
* Realistic name, address, contact info. Contains messiness modeled after patterns that found in a Denver area healthcare provider
  * Some names and address have special characters or other odd formatting things, like an address city of “###Boulder”
* Split across 5 providers/sites

## Purpose of the data set

This population was generated to test the Privacy Preserving Record Linkage (PPRL) solution being used within CODI. It replaced the demographic information with realistic and messy information to test an identity matching solution. Synthea's record splitting was used to generate multiple records for some individuals. In those split records, the demographic information may vary in ways that are expected in a real world system. For example, given name may be "John" in one instance of the record and "Johnny" in another.

## Record Splitting

The records are split across five synthetic providers. The Patient Resource in each bundle contains two identifiers that can be used to work with:
* http://codi.mitre.org - A unique ID for the record in the population
* http://codi.mitre.org/link_id - An ID that can be used to identify unique individuals across bundles across sites.

## Differences from populations generated with default Synthea settings

* Age range is 2 - 19
* Growth Errors Health Record Editor is turned on
* Addition of a MEND Module
* Navigational Assistance

### MEND Module

The [MEND Module](https://github.com/synthetichealth/synthea/blob/clinical-weight-loss/src/main/resources/modules/mend_program.json) was developed to simulate the [Mind, Exercise, Nutrition, Do It!](https://www.mendfoundation.org/) (MEND) Program . In this module, patients between ages five and seventeen are evaluated at wellness visits. For those with a BMI at or above the 95th percentile for age will have a small chance to be referred into the MEND Program. Over half of the referred individuals will not start the program. For individuals who do participate in MEND, they will do so for ten weeks. Each week has two sessions. The module simulates individuals missing sessions. Those who adhere to the program probabilistically attend a greater number of sessions.

### Navigational Assistance

The Navigational Assistance module was developed to simulate interaction with community organizations as well as test asset delivery. A fraction of patients with a household income at or under $35000 will seek navigational assistance from an organization called “Hunger Free” within six months of the birth of a patient. A fraction of those patients will receive asset delivery from WIC from when the patient is seven months old until they reach five years old.

Information related to navigational assistance or asset delivery is not easily represented in the FHIR standard. To accommodate this limitation, information was stored in FHIR DocumentReference resources.