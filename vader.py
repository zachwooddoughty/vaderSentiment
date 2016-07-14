import sys
import time

from vaderSentiment.vaderSentiment import sentiment as vs


def main():
    try:
        max_reviews = int(sys.argv[-1]) if len(sys.argv) > 1 else None
    except Exception, e:
        print "Whoops:", str(e)
        print "Usage: python vader.py [max_reviews]"
        return
    print "Processing %s reviews" % (str(max_reviews) if max_reviews else "all")

    d = {}

    start = time.time()
    with open("reviews.csv") as infile:
        with open("reviews_sentiments.csv", "w") as outfile:
            index = -1
            for line in infile:
                index += 1
                if index == 0:
                    outfile.write(line)
                    continue
                if index % 100 == 0:
                    print index / 100,
                
                text_split = line.strip().split(',', 4)
                text = text_split[4].decode('ascii', 'ignore')
                everything_else = ','.join(text_split[:4])
                score = str(vs(text)['compound'])
                new_line = everything_else + "," + score + "," + text + "\n"

                outfile.write(new_line)            
                d[text] = score

                if max_reviews and index >= max_reviews:
                    break

    print
    if max_reviews:
        duration = time.time() - start
        print "%d reviews took %f seconds for an average of %f seconds per review" % (index, duration, duration/index)

        sorted_reviews = sorted(d.items(), key=lambda x: x[1])
        worst = sorted_reviews[:10]
        best = sorted_reviews[-10:]
        print "WORST"
        for w in worst:
            print w[0], w[1]

        print "BEST"
        for b in best:
            print b[0], b[1]


if __name__ == "__main__":
    main()
