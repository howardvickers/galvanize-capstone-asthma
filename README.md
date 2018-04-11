## A Breath of Fresh Air: Predicting Asthma Rates with Data Science
### Machine learning algorithms are used to determine the drivers of asthma hospitalization rates and power a tool to predict asthma rates at a county level.

#### Overview & Purpose				
The goal of this project is to build a machine learning algorithm to predict asthma rates as influenced by pollutants and socio-economic factors by county in a sample of US states.

Asthma is a chronic inflammatory airway disease...
While asthma may be considered in social, economic, cultural, environmental, hormonal, and genetic terms, the focus of this analysis was socio-economic and environmental.  

A particular interest is the relative potential impact of external pollution, internal (household) pollution such as cigarette smoke vis-à-vis socio-economic factors.

Location is a key element in both pollution and socio-economic determinants, and so asthma rates are considered at the county level.

ZNA Health have generously offered support with identifying data sources and with environmental/medical questions.

The asthma variable is represented by hospitalization (ER visit) rates and as such are a reflection of both the current prevalence of asthma and the level of immediate ... Asthma hospitalization rates may be a reflection of both temporary triggers (current pollen and pollution levels) and the underlying causes of prevalence.  

#### Data
###### Data Sources
All data are available online as public records, either by county or otherwise geo-located.  The data include:
* Asthma hospitalization rates for each state:
  * California: [data.chhs.ca.gov](https://data.chhs.ca.gov/dataset/asthma-ed-visit-rates-lghc-indicator-07)
  * Colorado: [data-cdphe.opendata.arcgis.com](https://data-cdphe.opendata.arcgis.com/datasets/asthma-hospitalization-rate-counties)
  * Florida: [flhealthcharts.com](http://www.flhealthcharts.com/charts/OtherIndicators/NonVitalIndDataViewer.aspx?cid=0341)
  * New Jersey: [state.nj.us](https://www26.state.nj.us/doh-shad/indicator/view/NJASTHMAHOSP.countyAAR.html)
* Socio-economic data:  [countyhealthrankings.org](http://www.countyhealthrankings.org/rankings/data)
* Air quality data: [epa.gov](https://aqs.epa.gov/aqsweb/airdata/download_files.html)

Data was selected for four US states for the year 2016, as this data is both recent and well presented. The states represent a diversity of populations and locations across the country.  Data includes every county from the following states:
* California
* Colorado
* Florida
* New Jersey

###### Data Considerations
**Age:** Asthma hospitalization rates were available as adjusted for age.  Rates were for both adults and children.

**Single Year Analysis:** Asthma hospitalization rates are likely affected by short-term (exacerbatory) factors and so a longer term consideration of how factors may determine prevalence rates (over perhaps many years) was not considered necessary.  

**Gender:** Asthma has a greater prevalence in boys before puberty and yet a higher prevalence in women in adulthood.  Population gender differences between counties was therefore not included.

**Specific Sources of Pollution:** Wells and power plants were considered as potential sources of pollution.  However, data was ambiguous as to activity level (active/disused/etc) and initial data exploration suggested the relationships may not map to a county level. Therefore specific pollutant levels were considered to better capture the nature of pollution.  

##### Plots
###### Scatter Matrix
The below scatter matrix indicates the potential nature of relationships between the variables.

< image here >
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

###### Distribution of Incidence (hospitalization rates)
The below distribution of incidence demonstrates the range of levels of hospitalization rates across all counties in the four states.

< image here >
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

##### Data Challenges
While socio-economic datasets were largely complete (few missing data-points), the datasets for specific pollutants suffered considerably from sparsity.  

Models were run with NaNs converted to both zero and means; zeros gave a consistently improved performance.

Although datasets included multiple data-points for each year and county, the asthma hospitalization rates were only available as one data-point per county per year.  Multiple entries were therefore averaged to give one data-point per county for the year.

#### Models & Code

##### Models
Create a table with RMSE results and one sentence saying which was chosen and why.

| Model                           | RMSE          | Comments      |
| ------------------------------- |---------------| --------------|
| Linear Regression               | here          | here          |
| Lasso & Ridge (Elastic Net)     | here          | here          |
| Random Forest                   | here          | here          |
| Boosting                        | here          | here          |
| Support Vector Regression       | here          | here          |
| KNN Regression                  | here          | here          |


##### Features
Brief description/list

Although the Support Vector Machine regressor was selected for its predictive performance, the Random Forest model provides insight into the relative significance of the features.  The Feature Importances chart below shows that socio-economic factors have considerable explanatory power.

< image here >
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

##### Code
* Brief comments about structure

The code is publically available at [github.com/howardvickers](https://github.com/howardvickers).

#### Web App
A web app ([asthma-rates.com](http://asthma-rates.com)) allows interaction with the predictive model to gain practical insights into how asthma rates vary with the changes in the determinants.  

Web app users may change selected variables for a given county and/or state to see how the asthma rate is predicted to change under these new conditions.  This functionality can be seen as modeling the effects of policy changes.  

Screenshot of before/after maps

< image here >
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")


#### Results
tbd


#### References
"Gender differences in asthma development and progression. - NCBI." https://www.ncbi.nlm.nih.gov/pubmed/18156099. Accessed 10 Apr. 2018
