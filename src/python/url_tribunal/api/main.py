"""Flask application entrypoint."""

from url_tribunal.api.v1.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
