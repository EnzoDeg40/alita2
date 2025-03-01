from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(debug=True)