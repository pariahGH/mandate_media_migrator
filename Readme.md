# Mandate Media Migrator

TexProtects, a non-profit I do work for, wanted to migrate away from their CMS provider to Wordpress. The MM interface is not the best. Instead of doing a bunch of copy and paste, I wrote this to automate the archiving of material and files as well as generate a Wordpress import file - while not perfect, it was significantly more fun than doing it by hand and significantly faster. 

Can be run from run.sh with args (in order): base url of source (ie google.com), username, password, base url of new website. If anyone ever needs to migrate away from MM, let me know and maybe we can improve this together. 

Example:

./run.sh google.com foo foobar new.google.com

# Dependencies

This uses Scrapy to handle everything, except for downloading media files which uses requests. 