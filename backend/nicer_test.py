from astroquery.heasarc import Heasarc

# Initialize the HEASARC interface
heasarc = Heasarc()

# Query the nicermastr catalog for all observations using 'all-sky'
# This will return a table of all publicly available NICER observations.
print("Querying the full NICER master catalog using query_region with 'all-sky' spatial search...")
all_nicer_obs = heasarc.query_region(catalog="nicermastr", spatial='all-sky')

# Print some basic information about the results
if all_nicer_obs:
    print(f"Found a total of {len(all_nicer_obs)} NICER observations.")
    print("Here are the first 5 entries:")
    all_nicer_obs[:5].pprint(max_width=-1)
else:
    print("No NICER observations found in the master catalog.")