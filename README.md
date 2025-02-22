# Visualizion_StockOptionPrice_StockPrice
A subproject I did for Y-FoRM Presentation. The presentation was dealing w/ Ch 19.(Greek Letters) of "Options, Futures, And Other Derivatives" by John C. Hull. 

## Overview
This subproject is about visualizing the relationship btw Stock Prices and Stock Option Prices. I tried to visualize them into a graph so that we can see the relationship and also the Delta Greeks by seeing the slopes of each points. 

### FrontEnd (DeltaGraph.html)
For FrontEnd, I used html code for overall design and plotjson for visualization of specific graphs. I tried to make visualization clear, so i smoothed animation and differentiated colors. Additionally, I wanted to make the interface as interactive as possible, so I made an input blank for users to put option tickers. There is a (wrong) ticker example, and if u put the wrong ticker the UI will turn into whole red screen saying "WRONG TICKER !!! KEEP THE RIGHT FORMAT.". If u put the right ticker, it'll show the graphs.

### BackEnd (BackEnd_DeltaGraph.py)
For BackEnd, I used Python code for getting Option Price and Stock Price using yfinance library. For connecting BackEnd and FrontEnd, i used Flask. I sorted data by x variable(which is Stock Price), and matched the two dataset by using prices from same time.

## Conclusion and Further Developments
### Few Problems
First, The option data seems to be wrongly fetched. Although real world's option price can be different from theoretical option price, the graph looked so strange. On top of that, put option data was mostly 0.00 which means it has no meaning visualizing. 

Second, i fetched the option data but the strike price was not considered. This means that ITM/OTM/ATM prices are all in the data, which can affect the option price in many ways. This has to be considered as well.

### Further Developments
I'll need to specifically check in what point the data is wrong. It can be problems with fetching data, timeline, ITM/OTM classification, etc. Maybe I'll need another API that provides more specialized option data.

I can also make other visualizaiton html such as Gamma, Theta, Vega, Rho, etc. Also, I'm thinking of visualizing trading simulation of delta hedging.
