## A Breath of Fresh Air: Predicting Asthma Rates with Data Science
#### Machine learning to determine the drivers of asthma hospitalization rates and predict asthma rates at county level.

### Overview & Purpose				
The goal of this project is to build a machine learning algorithm to predict asthma rates as influenced by pollutants and socio-economic factors by county in a sample of US states.

Asthma is a chronic inflammatory airway disease...
While asthma may be considered in social, economic, cultural, environmental, hormonal, and genetic terms, the focus of this analysis was socio-economic and environmental.  

A particular interest is the relative potential impact of external pollution, internal (household) pollution such as cigarette smoke vis-à-vis socio-economic factors.

Location is a key element in both pollution and socio-economic determinants, and so asthma rates are considered at the county level.

ZNA Health have generously offered support with identifying data sources and with environmental/medical questions.

The asthma variable is represented by hospitalization (ER visit) rates and as such are a reflection of both the current prevalence of asthma and the level of immediate ... Asthma hospitalization rates may be a reflection of both temporary triggers (current pollen and pollution levels) and the underlying causes of prevalence.  

### Data Sources
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

~~#### Data Considerations~~
~~**Age:** Asthma hospitalization rates were available as adjusted for age.  Rates were for both adults and children.~~

~~**Single Year Analysis:** Asthma hospitalization rates are likely affected by short-term (exacerbatory) factors and so a longer term consideration of how factors may determine prevalence rates (over perhaps many years) was not considered necessary.~~

~~**Gender:** Asthma has a greater prevalence in boys before puberty and yet a higher prevalence in women in adulthood.  Population gender differences between counties was therefore not included.~~

~~**Specific Sources of Pollution:** Wells and power plants were considered as potential sources of pollution.  However, data was ambiguous as to activity level (active/disused/etc) and initial data exploration suggested the relationships may not map to a county level. Therefore specific pollutant levels were considered to better capture the nature of pollution.~~

### Plots
~~**Scatter Matrix**
The below scatter matrix indicates the potential nature of relationships between the variables.~~

Scatter plot for presentation.

**Distribution of Incidence**
The below distribution of incidence demonstrates the range of levels of hospitalization rates across all counties in the four states.

< image here >


### Data Challenges
While socio-economic datasets were largely complete (few missing data-points), the datasets for specific pollutants suffered considerably from sparsity.  

Models were run with NaNs converted to both zero and means; zeros gave a consistently improved performance.

Although datasets included multiple data-points for each year and county, the asthma hospitalization rates were only available as one data-point per county per year.  Multiple entries were therefore averaged to give one data-point per county for the year.


### Models
Although Elastic Net offered the most generalizable model with only marginal difference between the RMSE figures for train and test data, Random Forest was selected as offering lowest overall RMSE.

| Model                           | RMSE (Train)         | RMSE (Test)      |
| ------------------------------- |---------------| --------------|
| Linear Regression               | 18.25          | 22.37          |
| Elastic Net (a=1, l1=0.9)     | 19.86           | 19.91          |
| Random Forest                   | 11.27          | 16.50          |
| Gradient Boosting               | 0.09          | 20.15          |
| Support Vector Regressor      | 16.38          | 19.14          |
| KNN Regressor                | 0.03          | 18.02          |

Random Forest was also used to generate Feature Importances that offer insight into the relative importance of the variables.

### Features
Brief description/list

Although the Support Vector Machine regressor was selected for its predictive performance, the Random Forest model provides insight into the relative significance of the features.  The Feature Importances chart below shows that socio-economic factors have considerable explanatory power.

**Feature Importances**

![alt text](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/static/images/feat_imps.png "Feature Importances")

### Code
The code is structured as follows:
* [data.py](https://github.com/howardvickers) imports data from various csv files (downloaded from above-mentioned sources) and returns a single pandas dataframe.  The code includes functionality to run the model with selected states.
* [model.py](https://github.com/howardvickers) runs (trains and predicts) the final model.  
* [rf.py](https://github.com/howardvickers) runs the random forest model that is used to generate the feature importances chart.
* [chart.py](https://github.com/howardvickers) generates the feature importances chart from the random forest model.
* [app.py](https://github.com/howardvickers) serves the HTML and related files for the web app, drawing upon the above data and model files.

The code is available at [github.com/howardvickers](https://github.com/howardvickers).

### Web App
A web app ([asthma-rates.com](http://asthma-rates.com)) allows interaction with the predictive model to gain practical insights into how asthma rates vary with the changes in the determinants.  

Web app users may change selected variables for a given county and/or state to see how the asthma rate is predicted to change under these new conditions.  This functionality can be seen as modeling the effects of policy changes.  

**Screenshot of before/after maps**

![alt text](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/before_after_maps.png "Before and After Policy Changes")


### Results
brief sentence here.


### References
"Gender differences in asthma development and progression. - NCBI." https://www.ncbi.nlm.nih.gov/pubmed/18156099. Accessed 10 Apr. 2018
