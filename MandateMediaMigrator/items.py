# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Author(scrapy.Item):
    name = scrapy.Field()
    slug = scrapy.Field() #??
    bio = scrapy.Field()  #??
    itemid = scrapy.Field()

    def format(self):
        namesplit = self["name"].split(" ")
        fname = namesplit[0]
        lname = " ".join(namesplit[1:])
        email = ""
        return f"""
        <wp:author>
            <wp:author_id>{self["itemid"]}</wp:author_id>
            <wp:author_login><![CDATA[{fname}]]></wp:author_login>
            <wp:author_email><![CDATA[{email}]]></wp:author_email>
            <wp:author_display_name><![CDATA[{self["name"]}]]></wp:author_display_name>
            <wp:author_first_name><![CDATA[{fname}]]></wp:author_first_name>
            <wp:author_last_name><![CDATA[{lname}]]></wp:author_last_name>
        </wp:author>
        """

class Category(scrapy.Item):
    name = scrapy.Field()
    slug = scrapy.Field()        
    description = scrapy.Field() 
    itemid = scrapy.Field()
    #apparently does not support parents from mandate medias side
    def format(self):
        return f"""
        <wp:category>
            <wp:term_id>{self["itemid"]}</wp:term_id>
            <wp:category_nicename><![CDATA[{self["slug"]}]]></wp:category_nicename>
            <wp:category_parent><![CDATA[]]></wp:category_parent>
            <wp:cat_name><![CDATA[{self["name"]}]]></wp:cat_name>
            <wp:category_description><![CDATA[{self["description"]}]]></wp:category_description>
        </wp:category>
        """

published = {True:"publish",False:""}
featured = {True:0,False:""}
#TODO: this should end up translated to a gallery somehow
class Slideshow(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    rank = scrapy.Field()
    image_url = scrapy.Field()
    itemid = scrapy.Field()
    
    def format(self):
        return f"""
        """

class NavElement(scrapy.Item):
    order = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()            
    parent = scrapy.Field()
    path_match_type = scrapy.Field() 
    user_login_type = scrapy.Field() 
    groups = scrapy.Field()          
    itemid = scrapy.Field()
    #most of these fields dont appear to have wordpress equivalents
    def format(self):
        return f"""
        <item>
		<title>{self["title"]}</title>
		<link>{self["url"]}</link>
		<pubDate></pubDate>
		<dc:creator><![CDATA[wpadmin]]></dc:creator>
		<guid isPermaLink="false">{self["url"]}</guid>
		<description></description>
		<content:encoded>
				<![CDATA[ ]]>		</content:encoded>
		<excerpt:encoded>
				<![CDATA[]]>		</excerpt:encoded>
		<wp:post_id>{self["itemid"]}</wp:post_id>
		<wp:post_date><![CDATA[]]></wp:post_date>
		<wp:post_date_gmt><![CDATA[]]></wp:post_date_gmt>
		<wp:comment_status><![CDATA[closed]]></wp:comment_status>
		<wp:ping_status><![CDATA[closed]]></wp:ping_status>
		<wp:post_name><![CDATA[5]]></wp:post_name>
		<wp:status><![CDATA[publish]]></wp:status>
		<wp:post_parent>{self["parent"]}</wp:post_parent>
		<wp:menu_order>{self["order"]}</wp:menu_order>
		<wp:post_type><![CDATA[nav_menu_item]]></wp:post_type>
		<wp:post_password><![CDATA[]]></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
        <wp:postmeta>
		<wp:meta_key><![CDATA[_menu_item_type]]></wp:meta_key>
		<wp:meta_value><![CDATA[post_type]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_menu_item_menu_item_parent]]></wp:meta_key>
			<wp:meta_value><![CDATA[0]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_menu_item_object_id]]></wp:meta_key>
			<wp:meta_value><![CDATA[2]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_menu_item_object]]></wp:meta_key>
			<wp:meta_value><![CDATA[page]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_menu_item_target]]></wp:meta_key>
			<wp:meta_value><![CDATA[]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_menu_item_classes]]></wp:meta_key>
			<wp:meta_value><![CDATA[a:1:{{i:0;s:0:"";}}]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_menu_item_xfn]]></wp:meta_key>
			<wp:meta_value><![CDATA[]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key><![CDATA[_menu_item_url]]></wp:meta_key>
			<wp:meta_value><![CDATA[]]></wp:meta_value>
		</wp:postmeta>
							</item>
    <wp:term>
		<wp:term_id><![CDATA[{self["itemid"]}]]></wp:term_id>
		<wp:term_taxonomy><![CDATA[nav_menu]]></wp:term_taxonomy>
		<wp:term_slug><![CDATA[{self["url"]}]]></wp:term_slug>
		<wp:term_parent><![CDATA[{self["parent"]}]]></wp:term_parent>
		<wp:term_name><![CDATA[{self["name"]}]]></wp:term_name>
	</wp:term>
        """

class Tag(scrapy.Item):
    name = scrapy.Field()
    slug = scrapy.Field()
    itemid = scrapy.Field()
    #Mandate media tags do not have descriptions
    def format(self):
        return f"""
        <wp:tag>
			<wp:term_id>{self["itemid"]}</wp:term_id>
			<wp:tag_slug><![CDATA[{self["slug"]}]]></wp:tag_slug>
			<wp:tag_name><![CDATA[{self["name"]}]]></wp:tag_name>
			<wp:tag_description><![CDATA[]]></wp:tag_description>
		</wp:tag>
        """
#TODO: this requires plugin
class Redirect(scrapy.Item):
    redirect_from = scrapy.Field()
    redirect_to = scrapy.Field()
    itemid = scrapy.Field()
    
    def format(self):
        return f"""        """

class BlogPost(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    slug = scrapy.Field()
    publish_date = scrapy.Field()
    published = scrapy.Field()
    enable_comments = scrapy.Field()
    top_story = scrapy.Field()
    featured_post = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field()
    markup = scrapy.Field()
    body = scrapy.Field()
    extended_body = scrapy.Field()
    image = scrapy.Field()
    image_caption = scrapy.Field()
    pull_quote = scrapy.Field()
    video = scrapy.Field()
    itemid = scrapy.Field()
    delete_image = scrapy.Field()
    def format(self):
        return f"""
        <item>
			<title>{self["title"]}</title>
			<link>{self["slug"]}</link>
			<pubDate>{self["publish_date"]["date"]} {self["publish_date"]["time"]}</pubDate>
			<dc:creator><![CDATA[wpadmin]]></dc:creator>
			<guid isPermaLink="false">{self["slug"]}</guid>
			<description></description>
			<content:encoded><![CDATA[{self["body"]}]]></content:encoded>
			<excerpt:encoded><![CDATA[]]></excerpt:encoded>
			<wp:post_id>{self["itemid"]}</wp:post_id>
			<wp:post_date><![CDATA[{self["publish_date"]["date"]} {self["publish_date"]["time"]}]]></wp:post_date>
			<wp:post_date_gmt><![CDATA[{self["publish_date"]["date"]} {self["publish_date"]["time"]}]]></wp:post_date_gmt>
			<wp:comment_status><![CDATA[open]]></wp:comment_status>
			<wp:ping_status><![CDATA[open]]></wp:ping_status>
			<wp:post_name><![CDATA[{self["title"]}]]></wp:post_name>
			<wp:status><![CDATA[{published[self["published"]]}]]></wp:status>
			<wp:post_parent>0</wp:post_parent>
			<wp:menu_order>0</wp:menu_order>
			<wp:post_type><![CDATA[post]]></wp:post_type>
			<wp:post_password><![CDATA[]]></wp:post_password>
			<wp:is_sticky>{featured[self["featured_post"]]}</wp:is_sticky>
			<category domain="category" nicename="uncategorized"><![CDATA[Uncategorized]]></category>
	    </item>
        """

class NewsPost(scrapy.Item):
    published = scrapy.Field()
    featured = scrapy.Field()
    title = scrapy.Field()
    publication = scrapy.Field() #?
    url = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field() #?
    date = scrapy.Field()
    itemid = scrapy.Field()
    
    def format(self):
        return f"""
        <item>
		<title>{self["title"]}</title>
		<link>{self["url"]}</link>
		<pubDate>{self["date"]["date"]} {self["date"]["time"]}</pubDate>
		<dc:creator><![CDATA[wpadmin]]></dc:creator>
		<guid isPermaLink="false">{self["url"]}</guid>
		<description>{self["description"]}</description>
		<content:encoded>
				<![CDATA[{self["publication"]}]]>		</content:encoded>
		<excerpt:encoded>
				<![CDATA[]]>		</excerpt:encoded>
		<wp:post_id>{self["itemid"]}</wp:post_id>
		<wp:post_date><![CDATA[{self["date"]["date"]} {self["date"]["time"]}]]></wp:post_date>
		<wp:post_date_gmt><![CDATA[{self["date"]["date"]} {self["date"]["time"]}]]></wp:post_date_gmt>
		<wp:comment_status><![CDATA[open]]></wp:comment_status>
		<wp:ping_status><![CDATA[open]]></wp:ping_status>
		<wp:post_name><![CDATA[{self["title"]}]]></wp:post_name>
		<wp:status><![CDATA[{published[self["published"]]}]]></wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type><![CDATA[post]]></wp:post_type>
		<wp:post_password><![CDATA[]]></wp:post_password>
		<wp:is_sticky>{featured[self["featured"]]}</wp:is_sticky>
		<category domain="category" nicename="uncategorized"><![CDATA[Uncategorized]]></category>
		</item>
        """

class Page(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    publish_date = scrapy.Field()
    template_name = scrapy.Field()
    published = scrapy.Field() #this corresponds to  wp:status
    featured = scrapy.Field() #corresponds to is sticky (i think)
    itemid = scrapy.Field()
    def format(self):
        return f"""
        <item>
		<title>{self["title"]}</title>
		<link>{self["url"]}</link>
		<pubDate>{self["publish_date"]["date"]} {self["publish_date"]["time"]}</pubDate>
		<dc:creator><![CDATA[wpadmin]]></dc:creator>
		<guid isPermaLink="false">{self["url"]}</guid>
		<description>{self["template_name"]}</description>
		<content:encoded><![CDATA[{self["content"]}]]></content:encoded>
		<excerpt:encoded><![CDATA[]]></excerpt:encoded>
		<wp:post_id>{self["itemid"]}</wp:post_id>
		<wp:post_date><![CDATA[{self["publish_date"]["date"]} {self["publish_date"]["time"]}]]></wp:post_date>
		<wp:post_date_gmt><![CDATA[{self["publish_date"]["date"]} {self["publish_date"]["time"]}]]></wp:post_date_gmt>
		<wp:comment_status><![CDATA[closed]]></wp:comment_status>
		<wp:ping_status><![CDATA[open]]></wp:ping_status>
		<wp:post_name><![CDATA[{self["title"]}]]></wp:post_name>
		<wp:status><![CDATA[{published[self["published"]]}]]></wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type><![CDATA[page]]></wp:post_type>
		<wp:post_password><![CDATA[]]></wp:post_password>
		<wp:is_sticky>{featured[self["featured"]]}</wp:is_sticky>
		<wp:postmeta>
		<wp:meta_key><![CDATA[_wp_page_template]]></wp:meta_key>
		<wp:meta_value><![CDATA[default]]></wp:meta_value>
		</wp:postmeta>
		</item>
        """

class File(scrapy.Item):
    url = scrapy.Field()