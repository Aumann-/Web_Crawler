Python-based web crawler.

When launched, program will ask for a starting URL from whihc to crawl. Starting at this origin point, crawl will parse the HTML source of each page, locating all <a href> (hyperlink) tags. The URL contained in this tag will be appended to a tocrawl list for later.

The crawler will continue to crawl each found link that is in the tocrawl list until no more links are available or the program is terminated. The crawler will ask if it should stop based on a predefined limit that can be changed in-code. The crawler will also wait 10 seconds between each link to prevent sending too many requests to a single server in a short period.

As it crawls, the program will write each crawled links to a textfile.

If a link that has already been crawled is encountered, the link will be written to a second file.

Upon successful termination, all links remaining in the tocrawl list will be written to a third file.

The crawler will also keep track of how many links are discovered from each crawl and will write this tier lines to the crawled file for analysis. In the event that the number of links between tier lines if less than the tier lines shows, it is due to the unlisted links being duplicates.