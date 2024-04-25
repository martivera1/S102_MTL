from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='frontend/build', static_url_path='')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and path != "favicon.ico":
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
