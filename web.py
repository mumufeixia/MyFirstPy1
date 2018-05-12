from flask import Flask, render_template, request
app = Flask(__name__)  # create the application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cal', methods=['GET', 'POST'])
def cal():
    print request.method
    if request.method == 'POST':
        print True
        firstNum=request.form['first']
        secondNum = request.form['second']
        operator=request.form['operator']
        if operator =='plus':
            result=int(firstNum)+int(secondNum)
            return render_template('res.html',res=result)




    return render_template('cal.html')


if __name__ == '__main__':
    app.run('127.0.0.1', 8888, True)