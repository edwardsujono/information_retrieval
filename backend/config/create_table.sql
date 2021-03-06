CREATE TABLE amazon_products (

  product_id VARCHAR (1000) NOT NULL PRIMARY KEY,
  product_name VARCHAR (1000) NOT NULL,
  original_price  VARCHAR (20) NOT NULL,
  current_price VARCHAR (20) NOT NULL,
  product_description VARCHAR (5000) NOT NULL,
  product_link VARCHAR (1000) NOT NULL UNIQUE,
  rating VARCHAR (10) NOT NULL,
  image_link VARCHAR (1000) NOT NULL,
  semantic_value INT(11) NOT NULL

);

CREATE TABLE amazon_comments (
  product_id VARCHAR (1000) NOT NULL,
  comment VARCHAR(1000) NOT NULL,
  semantic_value INT(11)
);

CREATE TABLE shopee_products (

  product_id INT(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
  product_name VARCHAR (1000) NOT NULL,
  original_price  VARCHAR (20) NOT NULL,
  current_price VARCHAR (20) NOT NULL,
  product_description VARCHAR (5000) NOT NULL,
  product_link VARCHAR (1000) NOT NULL UNIQUE,
  rating VARCHAR (10) NOT NULL,
  image_link VARCHAR (1000) NOT NULL,
  semantic_value INT(11) NOT NULL

);

CREATE TABLE shopee_comments (
  product_id VARCHAR (1000) NOT NULL,
  comment VARCHAR(1000) NOT NULL,
  semantic_value INT(11)
);



CREATE TABLE lazada_products (

  product_id VARCHAR (1000) NOT NULL PRIMARY KEY,
  product_name VARCHAR (1000) NOT NULL,
  original_price  VARCHAR (20) NOT NULL,
  current_price VARCHAR (20) NOT NULL,
  product_description VARCHAR (5000) NOT NULL,
  product_link VARCHAR (1000) NOT NULL UNIQUE,
  rating VARCHAR (10) NOT NULL,
  image_link VARCHAR (1000) NOT NULL,
  category_name VARCHAR (100) NOT NULL,
  semantic_value INT (11s) NOT NULL

);

CREATE TABLE lazada_comments (
  product_id VARCHAR (1000) NOT NULL,
  comment VARCHAR(1000) NOT NULL,
  semantic_value INT(11)
);



CREATE TABLE lazada_comments (
  product_id VARCHAR (1000) NOT NULL,
  comment VARCHAR(1000) NOT NULL
);


CREATE TABLE product_names (
  product_id INT(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
  product_link VARCHAR (1000) NOT NULL,
  product_name VARCHAR(1000) NOT NULL
);

CREATE TABLE product_token_counts (
  token_id INT(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
  token_name VARCHAR (1000) NOT NULL,
  token_count int(11)
);


CREATE TABLE rating_shop (
  id INT(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
  shop VARCHAR (1000) NOT NULL,
  rating FLOAT NOT NULL
);