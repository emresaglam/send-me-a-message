from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField
import serial

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'IDontCareAboutThisSecret'
ser = serial.Serial('/dev/ttyUSB0')
app.config['ARDUINO'] = ser


class ReusableForm(Form):
    ledmessage = StringField('Send me a message:', validators=[validators.required(), validators.length(max=32)])

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)

        print form.errors
        if request.method == 'POST':
            ledmessage = request.form['ledmessage']
            ledmessage = ledmessage[0:32] + " \n"
            ledmessage = ledmessage.encode()
            print ledmessage, len(ledmessage)

        if form.validate():
            # Save the comment here.
            flash('Thanks for your message ')
            app.config['ARDUINO'].write(ledmessage)
        #else:
            #flash('All the form fields are required. ')

        return render_template('hello.html', form=form)


if __name__ == "__main__":
    host='0.0.0.0'
    app.run(host=host)
