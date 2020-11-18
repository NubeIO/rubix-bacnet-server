from src import app

ip = '0.0.0.0'
port = 1717
debug = False

if __name__ == '__main__':
    app.run(host=ip, port=port, debug=debug)
