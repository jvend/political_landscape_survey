# Project Proposal: Surveying the Political Landscape through Political Corpora

In the modern information age, it is imperative to consider the integrity and potential biases of ones source.
This is especially important with the on-going proliferation of "fake news" and usage of media to further agendas as opposed to inform.
Are there certain journalists or news outlets that fixate on particular issues and/or present these issues with biased slants?
The goal of this project is to inform readers not only of the existence of these potential hidden agendas (with evidence) but also to inform them how these agendas fit in the larger political landscape.


Thus the goal of this project is two-fold:
1) To provide users with a readily accessible summary of the current political landscape.
2) To show users how different journalists and media outlets fit into this landscape while highlighting potential biases.


# The Model

For this project, I would scrape data from Muck Rack and Google News. Muck Rack is a media database that operates much like a Facebook for journalists and public relations representatives while Google News is a news aggregator. The strength of the Muck Rack database is that it already organizes articles by user so that a given journalist's political corpus can readily be accessed. Google News on the other hand is more suitable for collecting recent news.

In order to build the model, I would use a combination of topic modeling (e.g. latent Dirichlet allocation) and sentiment analysis to construct a representation of the current political landscape. 

This sentiment analysis can be facilitated by first learning a set of controversial topics (e.g. gun control, religious freedom, drug laws, marriage rights, immigration, privacy rights etc.) and associated vocabulary by analyzing a corpus of opinion pieces and then emphasizing the sentiment towards these topics in the political text data.  I imagine presenting users with a scatter plot of topics e.g. Trump, immigration, gun-control, etc whose representative points are scaled in size so as to represent the volume of articles on a given topic. These topics points would make use of word embedding methods e.g. word2vec and a dimensionality reduction method e.g. t-SNE or UMAP so that similar topics are related by proximity and readily visualized. Clicking on a topic would yield another scatterplot with each point corresponding to an article and colored according to potential political bias, as determined by the sentiment analysis. Again these points would make use of a word/document embedding method e.g. word2vec or doc2vec and dimensionality reduction method. Hovering over one of these points would yield a link to the article and information on the author. One could also click on an author or media source to see a similar presentation restricted to that source's political corpus.

# Exploratory Data Analysis

As a first step, I scraped the most recent 10,000 article titles, headlines, and links to associated articles from all users on https://muckrack.com/. This totaled to around 10 GB of data. Code for scraping can be found in the scrape folder.
I then gauged the appropriateness of this dataset for my desired application by quantifying site usage tendencies. Since I was unfamiliar with the site prior to this project, I needed to confirm that the user database and number of articles per user was large enough to be useful. To this end I constructed a histogram of the number of authors with a given article count, see below. 

![fig1](Figures/muck_rack-hist.svg)

Note that the x-axis of the histogram utilizes a logarithmic transformation over article number. This allows us to properly visualize the entire user statistics in the same plot as well as see deviation from exponential decay of the number of author numbers per article count. For this dataset, we can see a central "hump" in the histogram after an initial decay. This hump says that the squeezing from our logarithmic scale outpaces the decay rate of the underlying distribution. Ultimately, we can say that underlying distribution is heavy-tailed and the number of prolific authors is high. I've included code for these results in the histogram folder.

The scraped text data was then scrubbed via tokenization and stop word/punctuation removal. In order to build a representation of the political landscape, I performed a word-frequency analysis of title words for all scraped articles. The 1,000 most frequently used words were embedded in a 300-dimensional vector space using word2vec pretrained with Google News data (GoogleNews-vectors-negative300.bin). This embedding was then projected into 2-dimensions using t-SNE and clustered using a Gaussian mixture model. These points are plotted in the scatter plot below. I hand-picked ~50 labels that I thought were interesting to display since displaying everything at once results in an illegible plot and colored the points by cluster.

![fig2](Figures/topic_embedding.svg)

The aforementioned process already provides interesting insight into the political landscape. Two clusters are clearly present in the data. Examining the words constituting these clusters we see that the larger purple cluster contains words related to important social issues of interest to the general public e.g. "immigration", "marijuana", "water", "shooting", "abortion", "gay", etc while the smaller yellow cluster contains language that is highly political or focused on international relations e.g. "gop", "washington", "israel", "iran", "eu", "clinton", "russia", "korea", "obama", etc. Interestingly enough, Trump and Clinton belong to different clusters possibly due to Clinton's role in foreign policy and Trumps active presence in the social commentary of the country. Nonetheless, the above exploratory analysis suggests that this project is certainly viable. Code for these results can be found the the topic-embedding folder

Notable topics can be found below.

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
