import feedparser
import re
import codecs

feedlist = [
	'http://today.reuters.com/rss/topNews',
	'http://today.reuters.com/rss/domesticNews',
	'http://today.reuters.com/rss/worldNews',
	'http://hosted.ap.org/lineups/TOPHEADS-rss_2.0.xml',
	'http://hosted.ap.org/lineups/USEHEADS-rss_2.0.xml',
	'http://hosted.ap.org/lineupsWORLDHEADS-rss_2.0.xml',
	'http://hosted.ap.org/lineups/POLITICSHEADS-rss_2.0.xml',
	'http://www.nytimes.com/services/xml/rss/nyt/HomPage.xml',
	'http://www.nytimes.com/services/xml/rss/nyt/International.xml',
	'http://news.google.com/?output=rss',
	'http://rss.cnn.com/rss/edition.rss',
	'http://rss.cnn.com/rss/edition_world.rss',
	'http://rss.cnn.com/rss/edition_us.rss'
]

def stripHTML(h) :
	p=''
	s=0
	for c in h:
		if c=='<' : s=1
		elif c=='>' :
			s=0
			p+= ' '
		elif s==0: 
			p+=c
	return p
	
def separatewords(text) :
	splitter=re.compile('\\W+')
	return [s.lower() for s in splitter.split(text) if len(s) > 3]
	
def getarticlewords() :
	allwords={}
	articlewords=[]
	articletitles=[]
	ec=0
	# Loop over every feed
	for feed in feedlist:
		f=feedparser.parse(feed)

		# Loop over every article 
		for e in f.entries:
			# Ignore identical articles
			if e.title in articletitles : continue
			
			# Extract the words
			txt = e.title + stripHTML(e.description)
			words = separatewords(txt)
			articlewords.append({})
			articletitles.append(e.title)
			
			# Increase the counts for each word in allwords and articlewords
			for word in words:
				allwords.setdefault(word,0)
				allwords[word]+=1
				articlewords[ec].setdefault(word,0)
				articlewords[ec][word]+=1
			ec+=1
	return allwords,articlewords,articletitles
		
def makematrix(allw,articlew) :
	wordvec = []
	
	# Only take words which are common but not too common (in 3 articles but fewer than 60% of the total)
	for w,c in allw.items() :
		if c > 3 and c < len(articlew)*0.6 :
			wordvec.append(w)
			
	# Create word matrix
	l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
	
	return l1,wordvec
	
# Execute the functions
allw,artw,artt = getarticlewords()
wordmatrix,wordvec = makematrix(allw,artw)
#print(wordvec[0:10])
#print(artt[1])
#print(wordmatrix[3][0:10])

out = codecs.open('articledata.txt','w','utf-8')
out.write('Article')
for word in wordvec : 
	out.write('\t%s' % word)
out.write('\n')

for idx, wordcounts in enumerate(wordmatrix) : 
	out.write(artt[idx] + '\t')
	out.write(',\t'.join(str(x) for x in wordcounts))
	out.write('\n')
	

