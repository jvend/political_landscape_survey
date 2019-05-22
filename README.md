# Project Proposal: Surveying the Political Landscape through Political Corpora

In the modern information age, it is imperative to consider the integrity and potential biases of ones source.
This is especially important with the on-going proliferation of "fake news" and usage of media to further agendas as opposed to inform.
Are there certain journalists or news outlets that fixate on particular issues and/or present these issues with biased slants?
The goal of this project is to inform readers not only of the existence of these potential hidden agendas (with evidence) but also to inform them how these agendas fit in the larger political landscape.


Thus the goal of this project is two-fold:
1) To provide users with a readily accessible summary of the current political landscape.
2) To show users how different journalists and media outlets fit into this landscape while highlighting potential biases.

Note: that this is the second iteration of the proposal, the first iteration can be found in /initial\_proposal.

# The Model

For this project, I would scrape data from Muck Rack and Google News. Muck Rack is a media database that operates much like a Facebook for journalists and public relations representatives while Google News is a news aggregator. The strength of the Muck Rack database is that it already organizes articles by user so that a given journalist's political corpus can readily be accessed. Google News on the other hand is more suitable for collecting recent news.

In order to build the model, I would use a combination of topic modeling (e.g. latent Dirichlet allocation) and sentiment analysis to construct a representation of the current political landscape. 

I imagine presenting users with a scatter plot of topics e.g. Trump, immigration, gun-control, etc whose representative points are scaled in size so as to represent the volume of articles on a given topic. Clicking on a topic would yield another scatterplot with each point corresponding to an author and colored according to potential political bias, as determined by the sentiment analysis with point size given by the number of articles by that author on the topic. Hovering over one of these points would yield a link to the article and information on the author. One could also click on an author or media source to see a similar presentation restricted to that source's political corpus. This type of data analysis could be particularly impactful if implemented as a google chrome plug-in that automatically offers such information on the author whenever a news article is visited.

# Exploratory Data Analysis

As a first step, I scraped the most recent 10,000 unique article titles and headlines with associated article links and source names from all users on https://muckrack.com/. This totaled to around 5 GB of data corresponding to around 12,000 authors and 7 millions articles. Code for scraping can be found in the scrape folder.
I then gauged the appropriateness of this dataset for my desired application by looking at site usage statistics. Since I was unfamiliar with the site prior to this project, I needed to verify that the user database and number of articles per user was large enough to be useful. This was confirmed and discussed in detail in the initial proposal. 

The scraped text data was then scrubbed via tokenization, stop word/punctuation removal and lemmatization. In order to build a representation of the associated political landscape, a combination of unsupervised and supervised approaches have been used. In order to have an unbiased initial look at the data, I first used latent Dirichlet allocation (LDA), the archetypal topic modeling algorithm.  LDA was highly successful and able to identify several important topics e.g. Brexit, immigration, the Mueller investigation, marijuana legalization, and others. A larger list of notable topics can be found in the table below and in my opinion constitute a very accurate summary of the current US political landscape. Code for the above LDA can be found in the LDA folder.

However, as a clustering algorithm, LDA is limited in it's classification abilities and little control can be exerted over the results e.g. it is unable to pick out user-specified topics. One might hope to alleviate this by heavily influencing the underlying prior over words for each topic but this yielded poor performance in practice so we opt to supplement it with a secondary, discriminative approach based on seeded word-frequency analysis. Several topics were chosen by me based on the top voting issues of previous elections e.g. gun control, immigration, the national budge, etc. I then specified words and phrases that would nearly guarantee correct classification. For example headlines with "gun policy" in them certainly deal with gun policy. This topic seeding was done in a two-level fashion by providing a list of phrases that would automatically assign a topic and another list that would assign a topic if the number of instances exceeded a threshold. Although no ground truth exists for our dataset, a random sampling of classified articles shows that this procedure works extremely well. Having obtained a subset of our data for which we are highly confident in its classification, we can use this subset as train data for a more powerful classifier such as an SVM that isn't limited to picking out certain phrases. This is to be done in future work. Code for this work can be found in the topic\_assist folder. Futhermore, some front-end development has been done [here](https://jvend.github.io/political_landscape_survey/) to produce an interactive plot of the political landscape implemented in d3.js. At the moment this plot only shows the topics for the above approach and their associated article counts but in the future will contain the functionality described in the model.

Having already obtained a first order topic model and classification scheme, we can now ask if any articles/authors within a particular topic exhibit strong sentiment towards said topic. By thresholding for strong positive and negative headline sentiment, we can pick successfully pick out articles with titles like "Why Trump deserves a Nobel Prize" and negative ones like "Donald Trump Can Go to Hell and If You Defend This, So Can You".  However, a naive application of sentiment analysis also picks out articles such as "A Divided Syria Reacts Wearily to Airstrikes From U.S. and Allies" which contains the phrase "President Donald Trump said the recent suspected chemical attack in Syria was the crime of a monster". Unsurprisingly a naive application of sentiment analysis is subject to mistakes. Nevertheless this can be largely alleviated by the use of parse trees to detect subject object relations to ensure that only sentiment corresponding to a particular subject is captured. This is to be done in future work but even this preliminary sentiment analysis reinforces the picture that authors can be heavily biased and suggests that profiling authors for bias is a meaningful goal.


The preliminary work above already provides interesting insight into the political landscape and the existence of author bias in polical media. It suggests that this project is certainly viable and is something I would be excited to pursue this summer.

Notable topics from the LDA clustering can be found below. Note that topic labels have been provided by me.

| Topic         | Keywords and Importance |
| ------------- |:------------------:|
| Brexit        | 0.021*"brexit" + 0.015*"eu" + 0.013*"theresa" + 0.012*"may" + 0.011*"minister" + 0.011*"european" + 0.009*"uk" + 0.008*"prime" + 0.007*"union" + 0.006*"deal" |
| North Korea   | 0.014*"korea" + 0.013*"china" + 0.013*"north" + 0.011*"trump" + 0.009*"trade" + 0.007*"president" + 0.006*"korean" + 0.006*"kim" + 0.006*"tariff" + 0.005*"nuclear" |
| Iran/Israel/Palestine | 0.020*"iran" + 0.013*"israel" + 0.010*"saudi" + 0.008*"nuclear" + 0.007*"netanyahu" + 0.007*"israeli" + 0.006*"palestinian" + 0.006*"arabia" + 0.006*"deal" + 0.006*"trump" | 
| UK Parliament        | 0.024*"labour" + 0.013*"corbyn" + 0.011*"jeremy" + 0.007*"party" + 0.007*"moore" + 0.006*"gorsuch" + 0.006*"britain" + 0.006*"chancellor" + 0.005*"quit" + 0.0    05*"neil" |
| US Supreme Court| 0.025*"court" + 0.015*"supreme" + 0.011*"judge" + 0.008*"law" + 0.007*"appeal" + 0.007*"rule" + 0.007*"ban" + 0.007*"justice" + 0.006*"federal" + 0.006*"abortion" | 
| Speaker of the House |0.010*"ryan" + 0.009*"paul" + 0.009*"climate" + 0.006*"pelosi" + 0.005*"ed" + 0.005*"change" + 0.005*"transgender" + 0.005*"rand" + 0.005*"speaker" + 0.004*"nancy" |
| Education/School Shooting| 0.019*"school" + 0.013*"student" + 0.009*"gun" + 0.007*"college" + 0.007*"texas" + 0.006*"university" + 0.006*"teacher" + 0.005*"high" + 0.004*"campus" + 0.004*"education" |
| Stock Market | 0.008*"stock" + 0.007*"oil" + 0.006*"market" + 0.006*"bank" + 0.005*"debt" + 0.005*"growth" + 0.005*"price" + 0.005*"percent" + 0.005*"rate" + 0.005*"company" |
| Immigration | 0.014*"border" + 0.014*"trump" + 0.011*"immigration" + 0.009*"immigrant" + 0.008*"wall" + 0.008*"shutdown" + 0.007*"president" + 0.006*"donald" + 0.005*"government" + 0.005*"mexico" |
| Brett Kavanaugh | 0.032*"kavanaugh" + 0.016*"brett" + 0.010*"ford" + 0.008*"saginaw" + 0.007*"supreme" + 0.007*"abbott" + 0.007*"liverpool" + 0.007*"pete" + 0.006*"turnbull" + 0.006*"court" |
| National Budget | 0.015*"tax" + 0.014*"budget" + 0.009*"health" + 0.007*"million" + 0.007*"cut" + 0.007*"state" + 0.006*"pay" + 0.006*"care" + 0.006*"plan" + 0.006*"billion" |
| Police | 0.021*"police" + 0.011*"man" + 0.010*"officer" + 0.008*"arrest" + 0.008*"charge" + 0.007*"county" + 0.007*"kill" + 0.007*"shoot" + 0.006*"baltimore" + 0.005*"suspect" | 
| Mueller Investigation | 0.018*"trump" + 0.012*"fbi" + 0.011*"mueller" + 0.010*"investigation" + 0.008*"president" + 0.008*"russia" + 0.008*"attorney" + 0.007*"russian" + 0.007*"donald" + 0.007*"counsel" |
| Syria | 0.011*"syria" + 0.009*"military" + 0.008*"attack" + 0.008*"islamic" + 0.008*"iraq" + 0.007*"isi" + 0.007*"war" + 0.007*"syrian" + 0.007*"force" + 0.006*"army" |
| Canada |  0.031*"mp" + 0.020*"trudeau" + 0.014*"justin" + 0.009*"ukrainian" + 0.008*"canadian" + 0.007*"ontario" + 0.007*"floyd" + 0.007*"canada" + 0.007*"ottawa" + 0.006*"ndp" |
| Republican Primary | 0.009*"cruz" + 0.008*"trump" + 0.008*"bush" + 0.007*"republican" + 0.007*"hogan" + 0.006*"ted" + 0.005*"maryland" + 0.005*"presidential" + 0.005*"rubio" + 0.005*"biden" |
| Marijuana | 0.012*"marijuana" + 0.006*"medical" + 0.006*"state" + 0.005*"company" + 0.004*"cannabis" + 0.004*"license" + 0.004*"law" + 0.004*"industry" + 0.004*"drug" + 0.004*"energy" |
| Russia| 0.030*"putin" + 0.020*"ukraine" + 0.019*"russian" + 0.018*"moscow" + 0.018*"vladimir" + 0.014*"russia" + 0.011*"jefferson" + 0.009*"xi" + 0.008*"kremlin" + 0.008*"chinese" |
| Transportation | 0.005*"airport" + 0.005*"flight" + 0.005*"plane" + 0.004*"airline" + 0.004*"rail" + 0.004*"transit" + 0.003*"passenger" + 0.003*"train" + 0.003*"air" + 0.003*"new" |
| NJ/NY Gov| 0.023*"md" + 0.021*"christie" + 0.019*"cuomo" + 0.011*"jersey" + 0.010*"beto" + 0.010*"chris" + 0.009*"walter" + 0.008*"hampshire" + 0.007*"andrew" + 0.007*"ron" |
| US Congress | 0.015*"bill" + 0.013*"senate" + 0.011*"house" + 0.009*"vote" + 0.008*"republican" + 0.007*"tax" + 0.007*"lawmaker" + 0.006*"gop" + 0.006*"pass" + 0.005*"care" |
| Tech Companies | 0.005*"apple" + 0.004*"facebook" + 0.004*"amazon" + 0.004*"company" + 0.004*"new" + 0.003*"zika" + 0.003*"varvel" + 0.003*"food" + 0.003*"user" + 0.003*"use" |
| Me Too Movement | 0.014*"sexual" + 0.010*"tory" + 0.008*"harassment" + 0.007*"allegation" + 0.007*"woman" + 0.006*"assault" + 0.005*"sex" + 0.005*"misconduct" + 0.004*"rape" + 0.004*"accuse" |
| 2016 Election | 0.015*"clinton" + 0.011*"trump" + 0.010*"election" + 0.010*"hillary" + 0.009*"republican" + 0.009*"democratic" + 0.008*"candidate" + 0.008*"presidential" + 0.008*"democrat" + 0.008*"voter" |

Some front-end development has been done [here](https://jvend.github.io/political_landscape_survey/)
