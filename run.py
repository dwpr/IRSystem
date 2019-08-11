from app import app
if __name__ == '__main__':  
    app.run(host='localhost', port=8808, debug=True)
# if doesn't run with localhost please change to 127.0.0.1 or 0.0.0.0