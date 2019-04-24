#this handles scraping of data from the mandate media site

import scrapy
from MandateMediaMigrator.items import *
from scrapy.http import FormRequest
import os
class MandateScraper(scrapy.Spider):
    name = "MandateScraper"
    #def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
    
    def start_requests(self):
        if self.base_url == "" or self.username == "" or self.password == "":
            print("Credentials and base url are required")
            exit()
        self.targets = [
            (f'https://{self.base_url}/admin/taggit/tag/?all=',self.parseTags), #works fine
            (f'https://{self.base_url}/admin/navbar/navbarentry/?all=',self.parseNav), #works fine
            (f'https://{self.base_url}/admin/mm_slideshow/slideshowimage/?all=',self.parseSlideshow), #N/A - no equivalent
            (f'https://{self.base_url}/admin/mm_redirects/redirect/?all=',self.parseRedirect), #N/A - no equivalent
            (f'https://{self.base_url}/admin/mm_page/page/?all=',self.parsePage),#works fine
            (f'https://{self.base_url}/admin/mm_news/newsitem/?all=',self.parseNewsPost),#works fine
            (f'https://{self.base_url}/admin/mm_blog/entry/?all=',self.parseBlogPost),#works fine
            (f'https://{self.base_url}/admin/mm_blog/category/?all=',self.parseCategory), #works fine
            (f'https://{self.base_url}/admin/mm_blog/author/?all=',self.parseAuthor) #there arent any
        ]
        yield scrapy.Request(f'https://{self.base_url}/admin', callback=self.login)
    
    def login(self, response):
        csrf = response.xpath('//*[@name="csrfmiddlewaretoken"]/@value').extract_first()
        return FormRequest.from_response(response, dont_filter=True, formdata={"csrfmiddlewaretoken":csrf,"username":self.username,"password":self.password,"this_is_the_login_form":"1","next":"/admin"},callback=self.start)
    
    def start(self,response):
        yield scrapy.Request(f'https://{self.base_url}/admin/filebrowser/browse', callback=self.parseFiles)
        for target in self.targets:
            request = scrapy.Request(target[0], callback=self.parseList)
            request.meta['callback'] = target[1]
            yield request

    def parseList(self, response):
        callback = response.meta['callback']
        for row in response.xpath('//*[@id="result_list"]/tbody/tr'):
            url = row.xpath('th/a/@href').get()
            yield scrapy.Request(f'https://{self.base_url}{url}', callback=callback)

    def checkList(self, item):
        if len(item) == 0:
            return 'None'
        if len(item) == 1:
            return item[0]
        return item

    def rowParser(self, response, handlers, formId):
        values = {}
        for row in response.xpath(f'//*[@id="{formId}"]/div/fieldset/div[contains(@class,"grp-row")]'):
            fieldName = row.xpath('div/div[contains(@class,"c-1")]/label/text()').get()
            fieldValue = row.xpath(f'div/div[contains(@class,"c-2")]/{handlers[fieldName]}').getall()
            values[fieldName.lower().replace(" ","_")] = self.checkList(fieldValue)
        return values

    def rowParserWithCheckboxes(self, response, handlers, formId):
        values = {}
        for row in response.xpath(f'//*[@id="{formId}"]/div/fieldset/div[contains(@class,"grp-row")]'):
            fieldName = row.xpath('div/div[contains(@class,"c-1")]/label/text()').get()
            if fieldName is None: 
                fieldName = row.xpath(f'div/div[contains(@class,"c-2")]/label/text()').get()
                fieldValue = row.xpath(f'div/div[contains(@class,"c-2")]/input[@checked]').get()
                checked = fieldValue is not None
                values[fieldName.lower().replace(" ","_")] = checked
            elif "Date" in fieldName or "date" in fieldName: 
                selectors = row.xpath(f'div/div[contains(@class,"c-2")]/input')
                date = selectors[0].xpath('@value').get()
                time = selectors[1].xpath('@value').get()
                values[fieldName.lower().replace(" ","_")] = {"date":date,"time":time}
            else:
                fieldValue = row.xpath(f'div/div[contains(@class,"c-2")]/{handlers[fieldName]}').getall()
                values[fieldName.lower().replace(" ","_")] = self.checkList(fieldValue)
        return values

    def parseTags(self, response):
        handlers = {
            "Name":'input/@value',
            "Slug":'input/@value'
        }
        yield Tag(**self.rowParser(response, handlers, "tag_form"), itemid=response.url.split("/")[-2])

    def parseNav(self, response):
        handlers = {
            "Order":'input/@value',
            "Url":'input/@value',
            "Title":'input/@value',
            "Name":'input/@value',
            "Parent":'select/option[@selected="selected"]/text()',
            "Path match type":'select/option[@selected="selected"]/text()',
            "User login type":'select/option[@selected="selected"]/text()',
            "Groups":'select[contains(@id,"id_groups_to")]/option/text()',
            }
        yield NavElement(**self.rowParser(response, handlers, "navbarentry_form"), itemid=response.url.split("/")[-2])

    def parseSlideshow(self,response):
        handlers = {
            "URL":'input/@value',
            "Title":'input/@value',
            "Rank":'input/@value',
            "Image URL":'p[contains(@class,"file-upload")]/a/@href'
            }
        values = self.rowParserWithCheckboxes(response, handlers, "slideshowimage_form")
        if values['image_url'] != "":
            yield File(url=values["image_url"])
        yield Slideshow(**values, itemid=response.url.split("/")[-2])

    def parseRedirect(self,response):
        handlers = {
            "Redirect from":'input/@value',
            "Redirect to":'input/@value',
            }
        yield Redirect(**self.rowParser(response, handlers, "redirect_form"), itemid=response.url.split("/")[-2])
    
    def parseCategory(self,response):
        handlers = {
            "Name":'input/@value',
            "Slug":'input/@value',
            "Description":'textarea/text()',
            }
        yield Category(**self.rowParser(response, handlers, "category_form"), itemid=response.url.split("/")[-2])

    def parseAuthor(self,response):
        handlers = {
            "Name":'input/@value',
            "Slug":'input/@value',
            "Bio":'textarea/text()',
            }
        yield Category(**self.rowParser(response, handlers, "author_form"), itemid=response.url.split("/")[-2])

    def parsePage(self,response): 
        handlers = {
            "Title":'input/@value',
            "URL":'input/@value',
            "Content":'textarea/text()',
            "Template name":'input/@value',
            #Featured, Published checkboxes and Publish Date are detected+handled in the row parser function
            }
        yield Page(**self.rowParserWithCheckboxes(response, handlers, "page_form"), itemid=response.url.split("/")[-2])

    def parseNewsPost(self,response):
        handlers = {
            "Title":'input/@value',
            "Publication":'input/@value',
            "Url":'input/@value',
            "Description":'textarea/text()',
            "Categories":'select[contains(@id,"id_categories_to")]/option/text()',
            #Featured, Published checkboxes and Date are detected+handled in the row parser function
            }
        yield NewsPost(**self.rowParserWithCheckboxes(response, handlers, "newsitem_form"), itemid=response.url.split("/")[-2])

    def parseBlogPost(self,response):
        handlers = {
            "Author":'select[contains(@id,"id_author")]/option[@selected="selected"]/text()',
            "Title":'input/@value',
            "Slug":'input/@value',
            "Publish date":'textarea/text()',
            "Categories":'select[contains(@id,"id_categories_to")]/option/text()',
            "Tags":'input/@value',
            "Markup":'select[contains(@id,"id_markup")]/option[@selected="selected"]/text()',
            "Body":'textarea/text()',
            "Extended body":'textarea/text()',
            "Image":'p[contains(@class,"file-upload")]/a/@href',
            "Image caption":'input/@value',
            "Pull quote":'input/@value',
            "Video":'textarea/text()'
            #Featured, Published checkboxes and Publish Date etc are detected+handled in the row parser function
            }
        values = self.rowParserWithCheckboxes(response, handlers, "entry_form")
        if values['image'] != "":
            yield File(url=values["image"])
        yield BlogPost(**values, itemid=response.url.split("/")[-2])

    def parseFiles(self, response):
        current_page = 1
        for li in response.xpath('//*[@id="grp-content-container"]/div[1]/div/div/div/nav/ul/li/text()').getall():
            if "\n" not in li:
                current_page = int(li)
        max_page = response.xpath('//*[@id="grp-content-container"]/div[1]/div/div/div/nav/ul/li')[-1].xpath("a/text()").get()

        #iterate over rows and yield File items
        for row in response.xpath('//*[@id="grp-changelist"]/div/table/tbody/tr[contains(@class,"grp-row")]'):
            if row.xpath('td/span[contains(@class,"fb_type")]/text()').get() == "Folder":
                yield scrapy.Request(f"https://{self.base_url}{row.xpath('td')[2].xpath('a/@href').get()}", callback=self.parseFiles)
            else:
                yield File(url=row.xpath('td[contains(@class,"fb_thumbnail")]/a/@href').get())

        if current_page != max_page:
            yield scrapy.Request(f'https://{self.base_url}/admin/filebrowser/browse/?p='+str(current_page+1), callback=self.parseFiles)    