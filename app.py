from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask import Markup

app = Flask(__name__)
app.config['SECRET_KEY'] = '######Anything######'
app.jinja_env.add_extension('jinja2.ext.do')

from forms import ReqForm, BaseForm
from models import FundRequest


@app.route('/', methods=['GET','POST'])
def form():
    form = ReqForm()
    numLumpSum = 0

    if 'numberLumpSum' in request.args:
        numLumpSum = int(request.args.get('numberLumpSum'))
        
    if request.method == 'POST':

        if form.validate_on_submit():
            fundCode = str(form.fundCode.data)
            sipAmount = form.sipAmount.data
            startDate = form.startDate.data
            endDate = form.endDate.data

            req = FundRequest(fundCode, startDate, endDate, sipAmount)

            lumpSumsList = form.lumpSums.data
            for lumpSum in lumpSumsList:
                date = lumpSum['lumpSumDate']
                amount = lumpSum['lumpSumAmount']
                df = req.add_lump_sum(date, amount)

            fundName = req.fundName
            xirr = req.calculate_xirr()
            totalQuantity = req.totalQuantity


            df = Markup(str(req.df.to_html(na_rep='-',justify='left',classes=["table","table-bordered","table-striped"])))

            print(req.df)

            return render_template('result.html', df=df, fundName=fundName, xirr=xirr, totalQuantity=totalQuantity)
        
        else:
            return render_template('req.html',reqForm=form, numLumpSum=numLumpSum)
        
            
    else:
        return render_template('req.html', reqForm=form, numLumpSum=numLumpSum)




if __name__ == '__main__':

    app.run(debug=True)