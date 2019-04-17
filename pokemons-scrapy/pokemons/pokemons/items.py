# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PokemonsItem(scrapy.Item):

    # =======================================
    # 基础信息
    _id = scrapy.Field()# Pokemon 全国编号
    name = scrapy.Field() # 名字
    types = scrapy.Field() # 属性
    category = scrapy.Field() # 类别
    abilities = scrapy.Field() # 特性
    exp_100 = scrapy.Field() # 100级时经验值
    catch_rate = scrapy.Field() # 普通精灵球在 Pokemon 满血状态下抓到的概率
    male_ratio = scrapy.Field() # male比例
    hatch_time = scrapy.Field() # 孵化步数
    hp = scrapy.Field() # 生命值
    atk = scrapy.Field() # 攻击力
    defense = scrapy.Field() # 防御力
    spatk = scrapy.Field() # 特殊攻击力
    spdef = scrapy.Field() # 特殊防御力
    speed = scrapy.Field() # 速度
    total = scrapy.Field() # 种族值总和
    image_url = scrapy.Field() # 图片链接

    # =======================================
    # 属性相克
    against_normal = scrapy.Field() # 对 一般 系的抗性
    against_fight = scrapy.Field() # 对 格斗 系的抗性
    against_flying = scrapy.Field() # 对 飞行 系的抗性
    against_poison = scrapy.Field() # 对 毒 系的抗性
    against_ground = scrapy.Field() # 对 地面 系的抗性
    against_rock = scrapy.Field() # 对 岩石 系的抗性
    against_bug = scrapy.Field() # 对 虫 系的抗性
    against_ghost = scrapy.Field() # 对 幽灵 系的抗性
    against_steel = scrapy.Field() # 对 钢 系的抗性
    against_fire = scrapy.Field() # 对 火 系的抗性
    against_water = scrapy.Field() # 对 水 系的抗性
    against_grass = scrapy.Field() # 对 草 系的抗性
    against_electric = scrapy.Field() # 对 电 系的抗性
    against_psychic = scrapy.Field() # 对 超能力 系的抗性
    against_ice = scrapy.Field() # 对 冰 系的抗性
    against_dragon = scrapy.Field() # 对 龙 系的抗性
    against_dark = scrapy.Field() # 对 恶 系的抗性
    against_fairy = scrapy.Field() # 对 妖精 系的抗性
    
    pass
