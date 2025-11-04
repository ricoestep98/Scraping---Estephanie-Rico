# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class HockeyteamsPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        #convert data to int
        field_names = ['team_wins', 'team_losses', 'goals_against', 'goals_for', 'diff_success']
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = int(value[0])
            print('*************')
            print(adapter[field_name])

        #convert data to float
        winpercentage = adapter.get('win_percentage')
        adapter['win_percentage'] = float(winpercentage[0])

        #null data convert to 0 and make it int
        value = adapter.get('team_ot_losses')[0]
        if adapter.get('team_ot_losses')[0] is '':
            value = 0
            adapter['team_ot_losses'] = value
        else:
            adapter['team_ot_losses'] = int(value)

        return item
