#!/usr/bin/env python3

#BoBoBo#

from pin.router import pin_app
import controller

app = pin_app(True)

if __name__ == "__main__":
    import pin.embed.server as server
    server.bootstrap(app)
