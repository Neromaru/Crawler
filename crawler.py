# coding: utf-8
import urllib as ur
import urlparse as parse
import re
import sys


class Crawler:
    def __init__(self):
        self.email = []
        self.link = sys.argv[1]
        self.depth = int(sys.argv[2])

    def crawl(self, link):
        read = ur.urlopen(link).read()  # считывание ссылки в строку
        find_e = re.findall(r'[a-zA-Z0-9_.=+-]+@[a-zA-Z0-9_.=+-]+.[a-zA-Z0-9_.=+-]+[a-zA-Z0-9_.=+-]',
                            read)  # нахождение всех имэйлов по паттерну(возвращает массив имэйлов)
        self.email.extend(find_e)  # расширение массива имэйлов найденными на данной странице
        self.email = list(set(self.email))  # исключение повторяющихся элементов массива
        find_de = re.findall(r'a href=[\'"]?([^\'" >]+)', read)  # поиск всех ссылок на странице
        find_de = list(set(find_de))  # удаление повторяющихся ссылок из массива
        return find_de  # Возвращаем массив ссылок

    def loop(self, link, depth):
        depth = depth
        if depth == 0:
            self.crawl(self.link)
            return self
        else:
            main_urls = self.crawl(
                link)  # массив ссылок на данной странице т.е. странница на которую переходим для углубления становиться главной относительно других вложеных или внешних
            for links in main_urls:  # цыкл пробега по всем ссылкам на данной странице
                pattern = re.compile(
                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # паттерн для http|https ссылок, т.е : ссылок на другие источники
                if re.match(pattern,
                            links):  # сравнивание паттерна с ссылкой переданой цыклом, если сходиться присваевает ссылке для извлечения имэйлов
                    self.link = links
                else:
                    self.link = parse.urljoin(self.link, links)
                    # если нет перехода на внешние ссылки, значить переход идет в глубь каталога сайта и извлечения ведутся оттуда
                    # использую urlparse для того что бы
                self.crawl(self.link)  # поиск имэйлов на данной странице
                self.loop(self.link, depth - 1)  # рекурсия для прохождения вглубь каталога
                self.link = sys.argv[
                    1]  # возвращение к первоначальной ссылке для возможности прохождения по другим страницам каталога сайта
        return self


def main():
    a = Crawler()
    a.loop(sys.argv[1], 0)  # нахождение имэйлов на начальной странице
    a.loop(sys.argv[1], a.depth)
    print a.email


main()
