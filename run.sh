#!/bin/bash
scrapy crawl MandateScraper -a base_url="$1" -a username="$2" -a password="$3" -a target_url="https://$4" -a title="$5"


