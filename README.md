# Police response to offenses in Seattle
The goal of the project I would like to propose is to monitor and improve the response of law enforcement to reports of assaults.

I used two data sets that I downloaded from the city of Seattle website and integrated them together. The first database has records of all offenses reported to the police ([Police Report Incident](https://data.seattle.gov/Public-Safety/Seattle-Police-Department-Police-Report-Incident/7ais-f98f)), and the second database has records of all offenses the police have responded to ([911 Incident Response](https://data.seattle.gov/Public-Safety/Seattle-Police-Department-911-Incident-Response/3k2p-39jp)). 

For the initial analysis I used two attributes – the district in which the offense occurred and the type of offense. There are more attributes that can be used such as date, hour and zone inside the district. 

|**Plot 1**|
|:--:| 
![](https://github.com/sefimin/Seattle_police_response/blob/master/Plot1.png "Plot 1")

In the first row of plot 1, we can observe the number of offenses as a function of offense type and district. There are 56 types of offenses in the dataset from which I chose to show only the 12 most common types.

I defined a new measure called “response time” that represents the delay between the time an offense was reported and the time a police officer was actually at the scene. For this purpose I only took records of offenses that have both a valid report time and an “at scene” time.

The response time can be divided to two types – positive response time and negative response time. For the purpose of my analysis, I assume that offenses with negative response time represent offenses that were reported by a police officer that was on field at the time of the offense, and hence the report only came after the “at scene” time. On the contrary, offenses with positive response time were reported by citizens so the arrival to the crime scene only occurred afterwards. This assumption should be verified in future analysis.

In the leftmost histogram in the bottom row of plot 1, I plotted the distribution of response time for all offense types. Extreme values are defined as values bigger than 300 minutes or smaller than -300 minutes. The extreme values compose only ~2% of all offenses and were omitted from my initial analysis. 

In the bottom row of plot 1, the middle and rightmost plots show the response time distribution of two sample offenses – vehicle theft and assault. Both distributions are different from the distribution when calculating for all offenses. Moreover, it can be observed that the positive response time for vehicle theft is more variable and has a higher mean the positive response time for assault. It seems that assault offenses are usually dealt with within 20 minutes or less, compared to car theft where it sometimes took several hours for the police to arrive to the crime scene.

For the second part of the initial analysis, I used only offenses with a positive response time (more than 1 minute and less than 300 minutes). 

|**Plot 2**|
|:--:| 
![](https://github.com/sefimin/Seattle_police_response/blob/master/Plot2.png "Plot 2")

For each district, I counted the number of assaults and calculated the mean response time. In the first row of plot 2, each point represents a district and it appears that there is no obvious correlation between the number of assaults in a district and the time it took the police to arrive. 

However, when calculating the mean response time for a specific offense in a specific district, it seems like the number of offenses for some type might be correlated with the mean response time of the same offense type. In the second row of plot 2, we can observe that a larger number of vehicle theft offenses in a district is correlated with a slower response time. On the other hand, a larger number of assault offenses in the district is correlated with a quicker response time. 

We can carefully interpret these results in the following way – for some crimes (such as vehicle theft) a large number of offenses can cause a heavy workload and cause delays, while for other crimes (such as assault), frequent occurrences make the law enforcement forces more experienced and efficient and hence they arrive at scene more quickly.

There are many other questions that can be asked using this dataset and the response time measure. For example – how does the frequency of one assault type affect other assaults? We can also ask question about time and date - are the police more efficient during the day or during the night? Is there a difference between weekdays and weekends? Finally, integrating socioeconomic information about the different districts can help to draw more significant conclusions.

---

### Data sources:
Data was downloaded in October 2016.
* [Seattle Police Department Police Report Incident](https://data.seattle.gov/Public-Safety/Seattle-Police-Department-Police-Report-Incident/7ais-f98f)
* [Seattle Police Department 911 Incident Response](https://data.seattle.gov/Public-Safety/Seattle-Police-Department-911-Incident-Response/3k2p-39jp)
