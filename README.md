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

### Data Challenges
While socio-economic datasets were largely complete (few missing data-points), the datasets for specific pollutants suffered considerably from sparsity.  

Models were run with NaNs converted to both zero and means; zeros gave a consistently improved performance.

Although datasets included multiple data-points for each year and county, the asthma hospitalization rates were only available as one data-point per county per year.  Multiple entries were therefore averaged to give one data-point per county for the year.


### Models
Although Elastic Net offered the most generalizable model with only marginal difference between the RMSE figures for train and test data, Random Forest was selected as offering lowest overall RMSE.

| Model                           | RMSE (Train)         | RMSE (Test)      | R Squared     |
| ------------------------------- |---------------| --------------| --------------|
| Linear Regression               | 11.02          | 12.59          |  0.76        |
| Elastic Net (a=1, l1=0.9)     | 11.87           | 12.01          |  0.78        |
| Random Forest                   | 7.09          | 10.80          |    0.82      |
| Gradient Boosting               | 2.00          | 10.68          | 0.82         |
| Support Vector Regressor      | 11.24          | 12.69          |  0.75        |
| KNN Regressor                | 0.03          | 11.49          |    0.80      |

Random Forest was also used to generate Feature Importances that offer insight into the relative importance of the variables.

### Features
Brief description/list

Although the Support Vector Machine regressor was selected for its predictive performance, the Random Forest model provides insight into the relative significance of the features.  The Feature Importances chart below shows that socio-economic factors have considerable explanatory power.

**Feature Importances**

![alt text](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/static/images/feat_imps.png "Feature Importances")

### Code
The code is structured as follows:
* [data.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/data.py) imports data from various csv files (downloaded from above-mentioned sources) and returns a single pandas dataframe.  The resulting dataset is also stored as a csv file to enable faster loading of data on future occasions.  The code includes functionality to run the model with selected states.
* [data_processing.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/data_processing.py) imports data from data.py and processes it for feature selection and for use in the algorithms.  
* [ols_model_hot_one.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/ols_model_hot_one.py) runs (trains and predicts) the OLS model.
* [get_feat_imps.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/get_feat_imps.py) runs the random forest model to generate the feature importances for the feature importances chart.
* [comparison.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/comparison.py) allows a comparison of models and their results.
* [get_results.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/get_results.py) processes data from the web app and returns results for representation as html in the web app.
* [charts.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/charts.py) generates the feature importances chart.
* [state_color_map.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/state_color_map.py) generates the state map-chart according to predictions based on policy changes input via the web app.
* [app.py](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/src/app.py) serves the HTML and related files for the web app, drawing upon the above data and model files.

The code is available at [github.com/howardvickers](https://github.com/howardvickers).

### Web App
A web app ([asthma-rates.com](http://asthma-rates.com)) allows interaction with the predictive model to gain practical insights into how asthma rates vary with the changes in the determinants.  

Web app users may change selected variables for a given county and/or state to see how the asthma rate is predicted to change under these new conditions.  This functionality can be seen as modeling the effects of policy changes.  

**Screenshot of before/after maps**

![alt text](https://github.com/howardvickers/galvanize-capstone-asthma/blob/master/before_after_maps.png "Before and After Policy Changes")


### Results
The selected model predicts asthma rates well with test data and the web app allows users to predict asthma rates given changes in variables according to hypothetical policy changes.  

### References
"Gender differences in asthma development and progression. - NCBI." https://www.ncbi.nlm.nih.gov/pubmed/18156099. Accessed 10 Apr. 2018
