'''
parsing document van Crime Data into seperate CSV files
which will be used to populate DB
Nicholas Allair 02/19/
'''

import csv
import holidays
import calendar
from datetime import date
from datetime import datetime

#YEARS INCLUDED IN BOTH DATA SETS
crimeYears = [2015,2016,2017,2018,2019,2020]

    #TYPE                       #CATAGORIE
#burglary                   Break and Enter Commercial
#burglary                   Break and Enter Residential/Other
#murder                     Homicide
#public-disorder            Mischief
#aggravated-assault         Offence Against a Person
#all-other-crimes           Other Theft
#theft-from-motor-vehicle   Theft from Vehicle
#all-other-crimes           Theft of Bicycle
#auto-theft                 Theft of Vehicle
#traffic-accident           Vehicle Collision or Pedestrian Struck (with Fatality)
#traffic-accident           Vehicle Collision or Pedestrian Struck (with Injury)



#DAYS OF WEEK
week_Days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

#HOLIDAYS for BC AND COLORADO
bc_holidays = holidays.Canada(years = crimeYears, state = "BC")
co_holidays = holidays.UnitedStates(years=crimeYears, state="CO")

#DEFINING ARRAY TO HOLD INFO FROM DATA CSV
type = []
year = []
month = []
day = []
hour = []
min = []
hundBlock = []
neighbourhood = []
x = []
y = []


#function to read from vancouver csv
def readVanData():
    with open('Data/van_Crime_Data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                thisYear = int(row[1])

                if thisYear > 2014:
                    type.append(row[0])
                    year.append(int(row[1]))
                    month.append(row[2])
                    day.append(row[3])
                    hour.append(int(row[4]))
                    min.append(int(row[5]))
                    hundBlock.append(row[6])
                    neighbourhood.append(row[7])
                    x.append(row[8])
                    y.append(row[9])

def writeVanDate():
    with open('ParsedData/vanDate.csv', 'w', newline='') as file:
        date_Key = 1000000
        writer = csv.writer(file)
        writer.writerow(["date-Key", "day-of-week", "month", "year", "weekend(Y/N)", "holiday(Y/N)", "holiday_Name"])

        for i in range(len(year)):
            this_year = int(year[i]) #hold int of year
            this_month = int(month[i]) #hold int of month
            this_day = int(day[i]) #hold int of day
            this_date_day = calendar.weekday(this_year, this_month, this_day)
            day_of_week = week_Days[this_date_day]#find the day of the week
            weekend = 0 #weekdend t/f
            holiday = 0 #holiday t/f
            holiday_name = "" #to hold holiday name if day is holiday

            if day_of_week == 'Saturday': #if day of the week is sat or sun then wet weekend == true
                weekend = 1

            if day_of_week == 'Sunday': #if day of the week is sat or sun then wet weekend == true
                weekend = 1

            if date(this_year, this_month, this_day) in bc_holidays: #if the day is a vancouver holiday
                holiday = 1 #set holiday == true
                holiday_name = bc_holidays.get(date(this_year, this_month, this_day)) #set holiday name
                is_Canadian_holiday = 1 #set is canadian holiday == true

            #setting array to then be written into csv
            newRow =    [
                        date_Key,
                        day_of_week,
                        this_month,
                        this_year,
                        weekend,
                        holiday,
                        holiday_name,
                        ]

            writer.writerow(newRow)

            date_Key += 1


def writeVanLocation():
    with open('ParsedData/vanLocation.csv', 'w', newline='') as file:
        location_Key = 1000000
        writer = csv.writer(file)
        writer.writerow(["location_Key", "location_Name", "longitude", "latitude", "neighbourhood","neighborhood_stats", "city","crime_rate"])
        for i in range(len(year)):
            this_location_Name = hundBlock[i]
            this_longitude = x[i]
            this_latitude = y[i]
            this_neighbourhood = neighbourhood[i]
            this_neighborhood_stats = 0
            this_city = "Vancouver"

            if year[i] == 2015:
                this_crime_rate = 1409

            if year[i] == 2016:
                this_crime_rate = 1536

            if year[i] == 2017:
                this_crime_rate = 1480

            if year[i] == 2018:
                this_crime_rate =1504

            if year[i] == 2019:
                this_crime_rate =1620

            if year[i] == 2020:
                this_crime_rate = 180

            newRow = [
                        location_Key,
                        this_location_Name,
                        this_longitude,
                        this_latitude,
                        this_neighbourhood,
                        this_neighborhood_stats,
                        this_city,
                        this_crime_rate
                    ]

            writer.writerow(newRow)

            location_Key += 1


def writeVanCrime():
    with open('ParsedData/vanCrime.csv', 'w', newline='') as file:
        crime_Key = 1000000
        writer = csv.writer(file)
        writer.writerow(["crime_key", "report_time",  "start_time", "end_time" , "details", "type" , "category" , "severity"])
        for i in range(len(year)):
            if type[i] == 'Break and Enter Commercial':
                this_type = "burglary"
                this_catagory = "Break and Enter Commercial"

            if type[i] == 'Break and Enter Residential/Other':
                this_type = "burglary"
                this_catagory = "Break and Enter Residential/Other"

            if type[i] == 'Homicide':
                this_type = "murder"
                this_catagory = "Homicide"


            if type[i] == 'Mischief':
                this_type = "public-disorder"
                this_catagory = "Mischief"

            if type[i] == 'Offence Against a Person':
                this_type = "aggravated-assault "
                this_catagory = "Offence Against a Person"

            if type[i] == 'Other Theft':
                this_type = "all-other-crimes "
                this_catagory = "Other Theft"

            if type[i] == 'Theft from Vehicle':
                this_type = "theft-from-motor-vehicle"
                this_catagory = "Theft from Vehicle"

            if type[i] == 'Theft of Bicycle':
                this_type = "all-other-crimes "
                this_catagory = "Theft of Bicycle"

            if type[i] == 'Theft of Vehicle':
                this_type = "auto-theft"
                this_catagory = "Theft of Vehicle"

            if type[i] == 'Vehicle Collision or Pedestrian Struck (with Fatality)':
                this_type = "traffic-accident"
                this_catagory = "Vehicle Collision or Pedestrian Struck (with Fatality)"

            if type[i] == 'Vehicle Collision or Pedestrian Struck (with Injury)':
                this_type = "traffic-accident"
                this_catagory = "Vehicle Collision or Pedestrian Struck (with Injury)"

            this_time = str(year[i]) + "/" + str(month[i]) + "/" + str(day[i]) + " " + str(hour[i]) + ":" + str(min[i]) + ":0"

            this_report_time = this_time
            this_start_time = this_time
            this_end_time = ""
            this_details = ""
            this_severity = ""

            newRow = [
                            crime_Key,
                            this_report_time,
                            this_start_time,
                            this_end_time,
                            this_details,
                            this_type,
                            this_catagory,
                            this_severity
                        ]

            writer.writerow(newRow)

            crime_Key += 1

def writeVanCrimeFact():
    with open('ParsedData/vanCrimeFact.csv', 'w', newline='') as file:
        key = 100000
        writer = csv.writer(file)
        writer.writerow(["date_Key", "location_Key", "crime_Key", "is_Traffic", "is_Fatal", "is_Nighttime"])
        for i in range(len(year)):
            this_date_key = key
            this_location_key = key
            this_crime_key = key
            this_is_Traffic = 0
            this_is_Fatal = 0
            this_is_Nighttime = 0

            if (hour[i] >= 22) or (hour[i] < 6):
                this_is_Nighttime = 1

            if type[i] == 'Vehicle Collision or Pedestrian Struck (with Fatality)':
                this_is_Traffic = 1
                this_is_Fatal = 1

            if type[i] == 'Vehicle Collision or Pedestrian Struck (with Injury)':
                this_is_Traffic = 1

            if type[i] == 'Homicide':
                this_is_Fatal =  1




            newRow = [
                        this_date_key,
                        this_location_key,
                        this_crime_key,
                        this_is_Traffic,
                        this_is_Fatal,
                        this_is_Nighttime
                    ]

            writer.writerow(newRow)

            key += 1


# def writeVanEvent():

readVanData()
writeVanDate()
writeVanLocation()
writeVanCrime()
writeVanCrimeFact()











