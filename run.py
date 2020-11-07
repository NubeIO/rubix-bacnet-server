from src import app


ip = '0.0.0.0'
port = 1515
debug = True


if __name__ == '__main__':
    app.run(host=ip, port=port, debug=debug)
