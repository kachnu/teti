#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

# создаём объект с именем модуля
logger = logging.getLogger('tetcontrol')
# задаём уровень логгирования
logging.basicConfig(level=logging.INFO)
# создаём обрабочтик файла лога
handler = logging.FileHandler('logger1.log')
# форматируем записи
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# устанавливаем формат для обработчика
handler.setFormatter(formatter)
# добавляем обработчик к логгеру
logger.addHandler(handler)
