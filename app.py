from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    ism = request.form.get('ism')
    yosh = request.form.get('yosh')
    shahar = request.form.get('shahar')

    if not ism.strip() or not yosh.strip() or not shahar.strip():
        return "❌ Ma'lumot to‘liq kiritilmadi!"

    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"Name: {ism} | Age: {yosh} | City: {shahar}\n")

    return "✅ Ma'lumot saqlandi!"

if __name__ == '__main__':
    app.run(debug=True)
