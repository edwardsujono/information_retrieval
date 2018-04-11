# E-Commerce Crawler

For shopee and lazada, you need to run Splash. See splash documentation: (here)[splash.readthedocs.io]

## Shopee
Go to the shopee_scrapy directory and run the following command
```scrapy crawl shopee -o shopee_products.json```

## Lazada
Go to the lazada_scrapy directory and run the following command
```scrapy crawl LazCat -o lazada_products.json```

## Amazon
Go to the amazon_scrapy directory and run the following command

### Amazon Products
```scrapy crawl AmazonScraper -o amazon_products.json```

### Amazon Comments
After scraping the amazon products, you can scrape the available comments by running the following command in the same directory
```scrapy crawl AmazonCommentScraper -o amazon_comments.json```

## After crawling
You can run the db.py script to insert the data to the database. 
For the further information on how to run and database credentials, please ask any of the members

