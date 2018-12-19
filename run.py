from flup.server.fcgi import WSGIServer

from app import app

if __name__ == "__main__":
    # app.run(
    #    host="0.0.0.0",
    #    port=7980,
    #    threaded=True,
    #    debug=True
    # )

    WSGIServer(app, bindAddress=("127.0.0.1", 7980)).run()
