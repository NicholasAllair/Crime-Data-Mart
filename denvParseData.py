#!/usr/bin/env python3

import csv
import holidays

from datetime import datetime


LOCATION_TABLE_ROWS = [ "location_id",  "location_name",
                        "longitude",    "latitude",
                        "neighborhood", "neighborhood_stats",
                        "city",         "crime_rate" ]

DATE_TABLE_ROWS     = [ "date_id",      "day_of_week",
                        "month",        "year",
                        "weekend",      "holiday",
                        "holiday_name" ]

CRIME_TABLE_ROWS    = [ "crime_id",     "report_time",
                        "start_time",   "end_time",
                        "details",      "type",
                        "category",     "severity" ]

EVENT_TABLE_ROWS    = [ "event_id",     "name",
                        "type",         "location",
                        "location_size" ]

CRIME_YEARS         = [ 2015, 2016, 2017, 2018, 2019, 2020 ]

CRIME_MAPPING       = { "all-other-crimes":               "all-other-crimes",
                        "public-disorder":                "public-disorder",
                        "drug-alcohol":                   "public-disorder",
                        "sexual-assault":                 "aggravated-assault",
                        "other-crimes-against-persons":   "all-other-crimes",
                        "white-collar-crime":             "all-other-crimes",
                        "traffic-accident":               "traffic-accident",
                        "murder":                         "murder",
                        "robbery":                        "all-other-crimes",
                        "aggravated-assault":             "aggravated-assault",
                        "arson":                          "all-other-crimes",
                        "burglary":                       "burglary",
                        "larceny":                        "burglary",
                        "theft-from-motor-vehicle":       "theft-from-motor-vehicle",
                        "auto-theft":                     "auto-theft"                }


TIME_FORMAT         = "%m/%d/%Y %I:%M:%S %p"



# Holds a unique id identifier for each table entry data
table_entry_id = 1


# ASSUMPTIONS:
# Night time between 10:00PM and 6:00 AM

def read_offense_codes_vsc(path):

    # Holds the denver crime code CSV table used to construct a dictionary
    reader = csv.reader( open(path), delimiter=",", quotechar='"' )

    # Holds all discovered offenses
    offenses = {}


    # Create a dictionary to hold column headers
    head = dict(reversed(field) for field in enumerate(next(reader)))


    for row in reader:

        # Extract the current offense code
        offense_code = row[head["OFFENSE_CODE"]]

        # Ensure the offense code is pointed to a dictionary
        if (not offenses.get(offense_code)):
            offenses[offense_code] = {}

        # Update the offense code dictionary with the content of the row
        offenses[offense_code][row[head["OFFENSE_CODE_EXTENSION"]]] = row

    return (offenses)



def read_denver_csv(path):
    global table_entry_id

    # Holds a dictionary representing offense codes
    offense_codes = read_offense_codes_vsc("Data/offense_codes.csv")

    # Holds the denver crime CSV table used to fill out the db tables
    reader = csv.reader( open(path), delimiter=",", quotechar='"' )

    # Holds a dictionary of Colorado holidays for crime years
    denver_holidays = holidays.UnitedStates(years=CRIME_YEARS, state="CO")


    # Initialize writers for each CSV table
    local   = csv.writer(open("ParsedData/denvLocation.csv",  "w", newline=""))
    dates   = csv.writer(open("ParsedData/denvDate.csv",      "w", newline=""))
    crime   = csv.writer(open("ParsedData/denvCrime.csv",     "w", newline=""))
    facts   = csv.writer(open("ParsedData/denvCrimeFact.csv", "w", newline=""))


    # Write the column headers for each CSV table
    local.writerow(LOCATION_TABLE_ROWS)
    dates.writerow(DATE_TABLE_ROWS    )
    crime.writerow(CRIME_TABLE_ROWS   )
    facts.writerow(["date_Key", "location_Key", "crime_Key", "is_Traffic", "is_Fatal", "is_Nighttime"])


    # Create a dictionary to hold column headers
    head = dict(reversed(field) for field in enumerate(next(reader)))


    for row in reader:

        # Extract date to be used for Crime data
        fst_occur = datetime.strptime( row[head["FIRST_OCCURRENCE_DATE"]],
                                       TIME_FORMAT )

        rpt_occur = datetime.strptime( row[head["REPORTED_DATE"        ]],
                                       TIME_FORMAT )

        try:
            lst_occur = datetime.strptime( row[head["LAST_OCCURRENCE_DATE" ]],
                                        TIME_FORMAT )
            lst_occur = lst_occur.strftime("%Y/%m/%d %H:%M:%S")
        except:
            lst_occur = ""


        # Offense date without time component used to extract holidays
        offense_date = fst_occur.strftime("%Y-%m-%d")

        # year / week / day used to identify weekends
        year, _, day = fst_occur.isocalendar()

        # Extract the type of offense that occured
        offense_code = row[head["OFFENSE_CODE"          ]]
        oc_extension = row[head["OFFENSE_CODE_EXTENSION"]]
        offense_type = offense_codes[offense_code][oc_extension][2]

        # Check if the incident was a traffic one
        is_traffic   = offense_codes[offense_code][oc_extension][7]


        # Check if the incident was fatal
        if (("murder" in offense_codes[offense_code][oc_extension][4]) or
            ("fatal"  in offense_type)
        ):
            is_fatal = "1"
        else:
            is_fatal = "0"


        # Remap the offense type to match Vancouver
        offense_type = offense_codes[offense_code][oc_extension][4]
        offense_type = CRIME_MAPPING.get(offense_type)


        if (offense_type == "traffic-accident"):
            if (is_fatal == "1"):
                offense_category = "Vehicle Collision or Pedestrian Struck (with Fatality)"
            else:
                offense_category = "Vehicle Collision or Pedestrian Struck (with Injury)"

        elif (offense_type == "auto-theft"):
            offense_category = "Theft of Vehicle"

        elif (offense_type == "theft-from-motor-vehicle"):
            offense_category = "Theft from Vehicle"

        elif (offense_type == "aggravated-assault"):
            offense_category = "Offence Against a Person"

        elif (offense_type == "murder"):
            offense_category = "Homicide"

        elif (offense_type == "public-disorder"):
            offense_category = "Mischief"

        elif (offense_type == "all-other-crimes"):
            if ("bicycle" in offense_codes[offense_code][oc_extension][3]):
                offense_category = "Theft of Bicycle"
            else:
                offense_category = "Other Theft"
        elif (offense_type == "burglary"):
            if ("business" in offense_codes[offense_code][oc_extension][3]):
                offense_category = "Break and Enter Commercial"
            else:
                offense_category = "Break and Enter Residential/Other"

        else:
            print("ERROR! Unknown offense category")


        if (year == 2020):
            crime_rate = 411
        elif (year == 2019):
            crime_rate = 3198
        elif (year == 2018):
            crime_rate = 3388
        elif (year == 2017):
            crime_rate = 3435
        elif (year == 2016):
            crime_rate = 3427
        elif (year == 2015):
            crime_rate = 3441
        else:
            crime_rate = 0


        # Check if the incident occured at anight
        time_val = (fst_occur.hour + (0.01 * fst_occur.minute))
        if ((6 >= time_val) or (time_val >= 22)):
            is_night = "1"
        else:
            is_night = "0"

        if (day >= 6):
            is_weekend = "1"
        else:
            is_weekend = "0"

        if (offense_date in denver_holidays):
            is_holiday = "1"
        else:
            is_holiday = "0"


        # Write the resulting data into the respecitve CSV table
        local.writerow( [ table_entry_id,
                          row[head['INCIDENT_ADDRESS'     ]],
                          row[head['GEO_LON'              ]],
                          row[head['GEO_LAT'              ]],
                          row[head['NEIGHBORHOOD_ID'      ]],
                          0, "Denver", crime_rate             ] )

        crime.writerow( [ row[head["INCIDENT_ID"          ]],
                          rpt_occur.strftime("%Y/%m/%d %H:%M:%S"),
                          fst_occur.strftime("%Y/%m/%d %H:%M:%S"),
                          lst_occur,
                          offense_type,
                          offense_category,
                          0                                   ] )

        dates.writerow( [ table_entry_id,
                          fst_occur.strftime('%A'),
                          fst_occur.strftime('%m'),
                          fst_occur.strftime('%Y'),
                          is_weekend,
                          is_holiday,
                          denver_holidays.get(offense_date)   ] )

        facts.writerow( [ table_entry_id,
                          table_entry_id,
                          row[head["INCIDENT_ID"]],
                          is_traffic,
                          is_fatal,
                          is_night                            ] )


        # Update the row count used to identify table data
        table_entry_id += 1


read_denver_csv("Data/crime.csv")

