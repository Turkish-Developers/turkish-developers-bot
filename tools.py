class Article:
    @staticmethod
    def get_article(article_link):
        import feedparser
        feed = feedparser.parse(article_link)

        first_article = feed.entries[0]
        link, title, summary = first_article.link, first_article.title, first_article.summary

        return link,title,summary


class Reddit:
    @staticmethod
    def get_last_image_on_subreddit(subreddit="ProgrammerHumor"):
        import praw
        app_id = 'ECrnLy8ChXiYypbO9noeCQ'
        secret = 'Z00rgSXtV2lWmlbwx_0nlNASedzU7g'
        
        reddit = praw.Reddit(
        client_id=app_id,
        client_secret=secret,
        user_agent="turkishdevelopers",
        )

        for submission in reddit.subreddit(subreddit).hot(limit=1):
            title = submission.title
            link = submission.preview.get('images')[0].get('source').get('url')

        return title, link



class Guild:
    @staticmethod
    def get_turkish_developers_guild(bot, id):
        return bot.get_guild(id)

