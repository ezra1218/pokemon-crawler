# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
import re
import traceback
from . import tags
from pokemons.items import PokemonsItem

class pokemonsSpider(scrapy.Spider):
    '''
    定义一个继承自 scrapy.Spider 的类，用于爬虫
    '''
    # 用于在 terminal 中执行 scrapy 爬虫命令的标示
    name = 'pokemons'

    # 爬取的链接
    start_urls = [
        'https://wiki.52poke.com/wiki/宝可梦列表（按全国图鉴编号）/简单版'
    ]

    #
    custom_settings = {
        'LOG_LEVEL': 'ERROR' # 只显示错误信息
    }

    # 解析网页
    def parse(self, response):
        '''
        解析初始网页
        '''
        # 爬虫获取到的 url 为相对链接
        # 因此定义一个 domain name
        domain = 'https://wiki.52poke.com'
        # 此处的 response 是 start_urls 中返回的数据
        soup = BeautifulSoup(response.body, 'html.parser')
        tags = soup.find_all(class_='mw-redirect', 
                             href=re.compile(r'/wiki/\w.*'))
        for tag in tags:
            # 每个 Pokemon 详情界面的 url
            url = (domain+tag.get('href'))
            yield scrapy.Request(url, callback=self.parse_deatils)

    def parse_deatils(self, response):
        '''
        解析详情网页
        '''
        # 此处的 response 是 Pokemon 详情界面返回的数据
        soup = BeautifulSoup(response.body, 'html.parser')
        # 返回一个 ResultSet（list）
        base_info_tables = soup.find_all('table', 
                                        class_=re.compile('roundy a-r at-c'))
        # 获取 ResultSet 中的第一个元素
        base_info_table = base_info_tables[0]
        # 获取所有 tr 节点
        base_info_trs = base_info_table.find_all('tr')

        # 获取 Pokemon 的种族值信息
        stats_info_table = soup.find_all('table', 
                            class_=re.compile('roundy alignt-center'))[0]
        stats_info_trs = stats_info_table.find_all('tr')

        # 获取 Pokemon 的属性相克信息
        against_info_table = soup.find_all(class_="bgwhite bw-1 bd-变化")[0].parent
        against_info_tds = against_info_table.find_all('td')
        
        try:
            # 获取 Pokemon 中文名字
            chinese_name = self.extract_chinese_name(base_info_trs)
            if chinese_name is None:
                raise Exception('Pokemon Chinese name not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 英文名字
            english_name = self.extract_english_name(base_info_trs)
            if english_name is None:
                raise Exception('Pokemon English name not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 序号
            pokdex = self.extract_pokdex(base_info_trs, soup)
            if pokdex is None:
                raise Exception('Pokemon index not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 属性
            types = self.extract_types(base_info_trs)
            if types is None:
                raise Exception('Pokemon types not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 分类
            category = self.extract_category(base_info_trs)
            if category is None:
                raise Exception('Pokemon category not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 特性
            abilities = self.extract_abilities(base_info_trs)
            if abilities is None:
                raise Exception('Pokemon abilities not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 100级时的经验值
            exp_100 = self.extract_exp_100(base_info_trs)
            if exp_100 is None:
                raise Exception('Pokemon Experience not found for {}'\
                    .format(response.url))

            # 获取 普通的精灵球在 Pokemon 满体力下的捕获率
            catch_rate = self.extract_catch_rate(base_info_trs)
            if catch_rate is None:
                raise Exception('Pokemon Catch Rate not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 是 male 的比例
            male_ratio = self.extract_male_ratio(base_info_trs)
            if male_ratio is None:
                raise Exception('Pokemon Male Ratio not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 孵化步数
            hatch_time = self.extract_hatch_time(base_info_trs)
            if hatch_time is None:
                raise Exception('Pokemon Hatch Time not found for {}'\
                    .format(response.url))

            # 获取 Pokemon HP
            hp = self.extract_hp(stats_info_trs)
            if hp is None:
                raise Exception('Pokemon HP not found for {}'\
                    .format(response.url))

            # 获取 Pokemon attack
            atk = self.extract_atk(stats_info_trs)
            if atk is None:
                raise Exception('Pokemon Attack not found for {}'\
                    .format(response.url))

            # 获取 Pokemon HP
            defense = self.extract_def(stats_info_trs)
            if defense is None:
                raise Exception('Pokemon Defense not found for {}'\
                    .format(response.url))

            # 获取 Pokemon special attack
            spatk = self.extract_spatk(stats_info_trs)
            if spatk is None:
                raise Exception('Pokemon Special Attack not found for {}'\
                    .format(response.url))

            # 获取 Pokemon special defense
            spdef = self.extract_spdef(stats_info_trs)
            if spdef is None:
                raise Exception('Pokemon Special Defense not found for {}'\
                    .format(response.url))

            # 获取 Pokemon Speed
            speed = self.extract_speed(stats_info_trs)
            if speed is None:
                raise Exception('Pokemon Speed not found for {}'\
                    .format(response.url))

            # 获取 Pokemon total
            total = self.extract_total(stats_info_trs)
            if total is None:
                raise Exception('Pokemon Total not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 图片链接
            image_url = self.extract_image_url(base_info_trs)
            if image_url is None:
                raise Exception('Pokemon Image URL not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 一般 属性的抗性
            against_normal = self.extract_against_norml(against_info_tds, soup)
            if against_normal is None:
                raise Exception('Pokemon Against Normal not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 格斗 属性的抗性
            against_fight = self.extract_against_fight(against_info_tds)
            if against_fight is None:
                raise Exception('Pokemon Against Fight not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 飞行 属性的抗性
            against_flying = self.extract_against_flying(against_info_tds)
            if against_flying is None:
                raise Exception('Pokemon Against Flying not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 毒 属性的抗性
            against_poison = self.extract_against_poison(against_info_tds)
            if against_poison is None:
                raise Exception('Pokemon Against Poison not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 地面 属性的抗性
            against_ground = self.extract_against_ground(against_info_tds)
            if against_ground is None:
                raise Exception('Pokemon Against Ground not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 岩石 属性的抗性
            against_rock = self.extract_against_rock(against_info_tds)
            if against_rock is None:
                raise Exception('Pokemon Against Rock not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 虫 属性的抗性
            against_bug = self.extract_against_bug(against_info_tds)
            if against_bug is None:
                raise Exception('Pokemon Against Bug not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 幽灵 属性的抗性
            against_ghost = self.extract_against_ghost(against_info_tds)
            if against_ghost is None:
                raise Exception('Pokemon Against Ghost not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 钢 属性的抗性
            against_steel = self.extract_against_steel(against_info_tds)
            if against_steel is None:
                raise Exception('Pokemon Against Steel not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 火 属性的抗性
            against_fire = self.extract_against_fire(against_info_tds)
            if against_fire is None:
                raise Exception('Pokemon Against Fire not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 水 属性的抗性
            against_water = self.extract_against_water(against_info_tds)
            if against_water is None:
                raise Exception('Pokemon Against Water not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 草 属性的抗性
            against_grass = self.extract_against_grass(against_info_tds)
            if against_grass is None:
                raise Exception('Pokemon Against Grass not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 电 属性的抗性
            against_electric = self.extract_against_electric(against_info_tds)
            if against_electric is None:
                raise Exception('Pokemon Against Electric not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 超能力 属性的抗性
            against_psychic = self.extract_against_psychic(against_info_tds)
            if against_psychic is None:
                raise Exception('Pokemon Against Psychic not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 冰 属性的抗性
            against_ice = self.extract_against_ice(against_info_tds)
            if against_ice is None:
                raise Exception('Pokemon Against Ice not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 龙 属性的抗性
            against_dragon = self.extract_against_dragon(against_info_tds)
            if against_dragon is None:
                raise Exception('Pokemon Against Dragon not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 恶 属性的抗性
            against_dark = self.extract_against_dark(against_info_tds)
            if against_dark is None:
                raise Exception('Pokemon Against Dark not found for {}'\
                    .format(response.url))

            # 获取 Pokemon 对 妖精 属性的抗性
            against_fairy = self.extract_against_fairy(against_info_tds)
            if against_fairy is None:
                raise Exception('Pokemon Against Fairy not found for {}'\
                    .format(response.url))

            # 保存成 item 以存储至 mongodb
            pokemon_item = PokemonsItem(_id=pokdex, chinese_name=chinese_name, 
                                        english_name=english_name, types=types, 
                                        category=category, abilities=abilities,
                                        exp_100=exp_100, catch_rate=catch_rate,
                                        male_ratio=male_ratio, 
                                        hatch_time=hatch_time, hp=hp, atk=atk, 
                                        defense=defense,  spatk=spatk, 
                                        spdef=spdef, speed=speed, 
                                        total=total, image_url=image_url, 
                                        against_normal=against_normal,
                                        against_fight=against_fight, 
                                        against_flying=against_flying,
                                        against_poison=against_poison, 
                                        against_ground=against_ground, 
                                        against_rock=against_rock,
                                        against_bug=against_bug, 
                                        against_ghost=against_ghost,
                                        against_steel=against_steel, 
                                        against_fire=against_fire,
                                        against_water=against_water, 
                                        against_grass=against_grass,
                                        against_electric=against_electric, 
                                        against_psychic=against_psychic,
                                        against_ice=against_ice, 
                                        against_dragon=against_dragon, 
                                        against_dark=against_dark, 
                                        against_fairy=against_fairy)
            yield pokemon_item

        except Exception as err:
            self.logger.error(str(err))
            self.logger.error(traceback.format_exc())


    @staticmethod
    def extract_chinese_name(trs):
        '''
        提取 Pokemon 中文名字
        '''
        return trs[0].find_all('b')[0].text

    @staticmethod
    def extract_english_name(trs):
        '''
        提取 Pokemon 英文名字
        '''
        return trs[0].find_all('b')[-1].text


    @staticmethod
    def extract_pokdex(trs, soup):
        '''
        提取 Pokemon 序号
        '''
        # selector = 'h1#firstHeading.firstHeading'
        # if len(soup.select(selector)) != 0:
        #     print(soup.select(selector)[0].text)

        return re.findall(r'\d{3}', trs[0].text)[0]

    @staticmethod
    def extract_types(trs):
        '''
        提取 Pokemon 属性
        '''
        return trs[6].text.strip().split('\xa0\xa0')

    @staticmethod
    def extract_category(trs):
        '''
        提取 Pokemon 类别
        '''
        return trs[8].text.strip()

    @staticmethod
    def extract_abilities(trs):
        '''
        提取 Pokemon 特性
        '''
        return trs[11].text.strip().replace('\xa0', ' ').split('\n\n')
    
    @staticmethod
    def extract_exp_100(trs):
        '''
        提取 Pokemon 100级时的经验值
        '''
        if len(trs) == 60:
            return trs[13].text.strip()
        return trs[14].text.strip()

    @staticmethod
    def extract_height(trs):
        '''
        提取 Pokemon 身高（m）
        '''
        if len(trs) == 60:
            return re.findall(r'\d.\d', trs[31].text.strip())[0]
        return re.findall(r'\d.\d', trs[32].text.strip())[0]

    @staticmethod
    def extract_weight(trs):
        '''
        提取 Pokemon 体重（kg）
        '''
        if len(trs) == 60:
            return re.findall(r'\d.\d', trs[33].text.strip())[0]   
        return re.findall(r'\d.\d', trs[34].text.strip())[0]

    @staticmethod
    def extract_catch_rate(trs):
        '''
        提取 普通的精灵球在 Pokemon 满体力下的捕获率
        '''
        if len(trs) == 60:
            return trs[43].find('span').text
        return trs[44].find('span').text

    @staticmethod
    def extract_male_ratio(trs):
        '''
        提取 Pokemon 是 male 的比例
        '''
        if len(trs) == 60 and trs[48].find('span'):
            return re.findall(r'[\d.\d]*%', trs[48].find('span').text)[0]
        elif len(trs) == 61 and trs[49].find('span'):
            return re.findall(r'[\d.\d]*%', trs[49].find('span').text)[0]
        else:
            return trs[48].text.strip()

    @staticmethod
    def extract_hatch_time(trs):
        '''
        提取 Pokemon 的孵化步数
        '''
        if len(trs) == 60:
            return re.findall(r'[\d]*步', trs[51].find_all('td')[-1].text)[0]
        return re.findall(r'[\d]*步', trs[52].find_all('td')[-1].text)[0]

    @staticmethod
    def extract_hp(trs):
        '''
        提取 Pokemon hp
        '''
        return trs[3].find_all('th', class_='bgl-HP')[-1].text.strip()

    @staticmethod
    def extract_atk(trs):
        '''
        提取 Pokemon attack
        '''
        return trs[5].find_all('th', class_='bgl-攻击')[-1].text.strip()

    @staticmethod
    def extract_def(trs):
        '''
        提取 Pokemon defense
        '''
        return trs[7].find_all('th', class_='bgl-防御')[-1].text.strip()

    @staticmethod
    def extract_spatk(trs):
        '''
        提取 Pokemon special attack
        '''
        return trs[9].find_all('th', class_='bgl-特攻')[-1].text.strip()

    @staticmethod
    def extract_spdef(trs):
        '''
        提取 Pokemon special defense
        '''
        return trs[11].find_all('th', class_='bgl-特防')[-1].text.strip()

    @staticmethod
    def extract_speed(trs):
        '''
        提取 Pokemon speed
        '''
        return trs[13].find_all('th', class_='bgl-速度')[-1].text.strip()

    @staticmethod
    def extract_total(trs):
        '''
        提取 Pokemon 种族值总值
        '''
        return re.findall(r'\d{3}', trs[15].text)[0].strip()

    @staticmethod
    def extract_image_url(trs):
        '''
        提取 Pokemon 图片链接
        '''
        domain = 'https://'
        try:
            image_url = re.findall(r'media.*png', trs[3]\
                .find('img').get('data-srcset').split(',')[-1])[0]
        except:
            image_url = trs[3].find('img').get('data-url')

        return domain + image_url

    @staticmethod
    def extract_against_norml(tds, soup):
        '''
        提取 Pokemon 对 一般 属性的抗性
        '''
        # selector = 'h1#firstHeading.firstHeading'
        # if len(soup.select(selector)) != 0:
        #     print('name: {}'.format(soup.select(selector)[0].text))
        if tds[3]:
            return tds[3].text.strip()

    @staticmethod
    def extract_against_fight(tds):
        '''
        提取 Pokemon 对 格斗 属性的抗性
        '''
        if tds[4]:
            return tds[4].text.strip()

    @staticmethod
    def extract_against_flying(tds):
        '''
        提取 Pokemon 对 飞行 属性的抗性
        '''
        if tds[5]:
            return tds[5].text.strip()

    @staticmethod
    def extract_against_poison(tds):
        '''
        提取 Pokemon 对 毒 属性的抗性
        '''
        if tds[6]:
            return tds[6].text.strip()

    @staticmethod
    def extract_against_ground(tds):
        '''
        提取 Pokemon 对 地面 属性的抗性
        '''
        if tds[7]:
            return tds[7].text.strip()

    @staticmethod
    def extract_against_rock(tds):
        '''
        提取 Pokemon 对 岩石 属性的抗性
        '''
        if tds[8]:
            return tds[8].text.strip()

    @staticmethod
    def extract_against_bug(tds):
        '''
        提取 Pokemon 对 虫 属性的抗性
        '''
        if tds[9]:
            return tds[9].text.strip()

    @staticmethod
    def extract_against_ghost(tds):
        '''
        提取 Pokemon 对 幽灵 属性的抗性
        '''
        if tds[10]:
            return tds[10].text.strip()

    @staticmethod
    def extract_against_steel(tds):
        '''
        提取 Pokemon 对 钢 属性的抗性
        '''
        if tds[11]:
            return tds[11].text.strip()

    @staticmethod
    def extract_against_fire(tds):
        '''
        提取 Pokemon 对 火 属性的抗性
        '''
        if tds[12]:
            return tds[12].text.strip()

    @staticmethod
    def extract_against_water(tds):
        '''
        提取 Pokemon 对 水 属性的抗性
        '''
        if tds[13]:
            return tds[13].text.strip()

    @staticmethod
    def extract_against_grass(tds):
        '''
        提取 Pokemon 对 草 属性的抗性
        '''
        if tds[14]:
            return tds[14].text.strip()

    @staticmethod
    def extract_against_electric(tds):
        '''
        提取 Pokemon 对 电 属性的抗性
        '''
        if tds[15]:
            return tds[15].text.strip()

    @staticmethod
    def extract_against_psychic(tds):
        '''
        提取 Pokemon 对 超能力 属性的抗性
        '''
        if tds[16]:
            return tds[16].text.strip()

    @staticmethod
    def extract_against_ice(tds):
        '''
        提取 Pokemon 对 冰 属性的抗性
        '''
        if tds[17]:
            return tds[17].text.strip()

    @staticmethod
    def extract_against_dragon(tds):
        '''
        提取 Pokemon 对 龙 属性的抗性
        '''
        if tds[18]:
            return tds[18].text.strip()

    @staticmethod
    def extract_against_dark(tds):
        '''
        提取 Pokemon 对 恶 属性的抗性
        '''
        if tds[19]:
            return tds[19].text.strip()

    @staticmethod
    def extract_against_fairy(tds):
        '''
        提取 Pokemon 对 妖精 属性的抗性
        '''
        if tds[20]:
            return tds[20].text.strip()