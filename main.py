
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import requests
from flask_wtf import Form
from wtforms import StringField,PasswordField,FloatField,SubmitField
from wtforms.validators import InputRequired,Email,Length,AnyOf
from flask_bootstrap import Bootstrap
from iexfinance import Stock
import pytz
import tzlocal
import datetime
from werkzeug.exceptions import BadRequest


app=Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']='Ekmys@123'


class investmentForm(Form):
    stockSymbol=StringField('Stock Symbol',validators=[InputRequired(),Length(min=2,max=5,message='Please Enter Correct symbol')])
    submit=SubmitField()
 

    

def datetimeConverstion():
        currentLocalTime= datetime.datetime.now()
        currentUtcTime=datetime.datetime.utcnow()
        localTimeZone=tzlocal.get_localzone()
        ct=currentUtcTime.replace(tzinfo=pytz.utc).astimezone(localTimeZone)
        return (ct)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404    


 

@app.route("/",methods=['GET','POST'])
def index():
    form=investmentForm()
    if request.method== 'POST' and form.validate():

        #Get form field data
        symb=form.stockSymbol.data
        stock=Stock(symb)
        openPrice=stock.get_open()
        nowPrice=stock.get_price()
        companyInfo=stock.get_company()
        companyName=companyInfo['companyName']
        symbol=companyInfo['symbol']
        calculate=openPrice-nowPrice
        calc="{:.2f}".format(calculate)


        ct=datetimeConverstion()
        percentage=((openPrice - nowPrice) / openPrice)*100
        percent="{:.2f}".format(percentage)
        new_date = ct.strftime('%A %Y-%m-%d %I:%M %p')

        return render_template('price.html',symbol=symbol,companyName=companyName,nowPrice=nowPrice,new_date=new_date,calc=calc,percent=percent)
    return render_template('home.html',form=form)

if __name__=='__main__':
    app.run()


