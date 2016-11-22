import web

urls = (
    '/', 'getEvents.GetEvents',
    '/lol', 'med'
)

class med:
    def GET(self):
        return "test"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
