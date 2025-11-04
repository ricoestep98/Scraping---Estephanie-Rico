import scrapy
from hockeyteams.items import HockeyteamsItem


class HtspiderSpider(scrapy.Spider):
    name = "htSpider"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/forms/"]

    custom_settings = {
        'FEEDS': {
            'hockeyteams.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
      
        pages = response.css('ul.pagination li')

        for i in range(len(pages) - 1):

            next_page = pages[i].css('li a ::attr(href)').get()
            next_page_url = 'https://www.scrapethissite.com' + next_page
            
            yield response.follow(next_page_url, callback = self.HockeyTeamProcessing)
            
    
    def HockeyTeamProcessing(self, response):

        hockeyteam_item = HockeyteamsItem()

        hockeyteams = response.css('table tr.team')

        for hockeyteam in hockeyteams:

            winpercentage = hockeyteam.css('td.pct.text-success').xpath('normalize-space(text())').get()
            diffsuccess = hockeyteam.css('td.diff.text-success').xpath('normalize-space(text())').get()

            if winpercentage is None:
                winpercentage = hockeyteam.css('td.pct.text-danger').xpath('normalize-space(text())').get()
            
            if diffsuccess is None:
                diffsuccess = hockeyteam.css('td.diff.text-danger').xpath('normalize-space(text())').get()

            hockeyteam_item['team_name'] = hockeyteam.css('td.name').xpath('normalize-space(text())').get(),
            hockeyteam_item['year'] = hockeyteam.css('td.year').xpath('normalize-space(text())').get(),
            hockeyteam_item['team_wins'] = hockeyteam.css('td.wins').xpath('normalize-space(text())').get(),
            hockeyteam_item['team_losses'] = hockeyteam.css('td.losses').xpath('normalize-space(text())').get(),
            hockeyteam_item['team_ot_losses'] = hockeyteam.css('td.ot-losses').xpath('normalize-space(text())').get(),
            hockeyteam_item['win_percentage'] = winpercentage,
            hockeyteam_item['goals_for'] = hockeyteam.css('td.gf').xpath('normalize-space(text())').get(),
            hockeyteam_item['goals_against'] = hockeyteam.css('td.ga').xpath('normalize-space(text())').get(),
            hockeyteam_item['diff_success'] = diffsuccess,

            yield hockeyteam_item