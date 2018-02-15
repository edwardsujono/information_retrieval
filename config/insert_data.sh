#!/bin/bash

curl http://128.199.207.105:8983/solr/shopee_collection/update -H "Content-Type: text/xml" --data-binary @insert_example.xml
