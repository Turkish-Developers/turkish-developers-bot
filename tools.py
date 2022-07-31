class Article:
    @staticmethod
    def get_article(article_link):
        import feedparser
        feed = feedparser.parse(article_link)

        first_article = feed.entries[0]
        link, title, summary = first_article.link, first_article.title, first_article.summary

        return link,title,summary


class Guild:
    @staticmethod
    def get_turkish_developers_guild(bot, id):
        return bot.get_guild(id)

