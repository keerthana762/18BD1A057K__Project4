
from flask import Flask, render_template, request
from twilio.rest import Client
import requests
import requests_cache





account_sid='AC18e3f3f760fc56621439d97b3d1c4b36'
#auth_token='f32d473f0c79f74073dcf9b8bec9949b'
auth_token='f46ec385f62613343e30b73d706449fa'




client=Client(account_sid,auth_token)
app=Flask(__name__,static_url_path='/static')
@app.route('/')
def registration_form():
    return render_template('test_page.html')



@app.route('/AddData',methods=['POST','GET'])
def user_registration_dtls():
    f_name=request.form['fname']
    l_name=request.form['lname']
    email=request.form['email']
    source_st=request.form['src']
    source_dt = request.form['srcD']
    destination_st=request.form['dest']
    destination_dt = request.form['destD']
    phoneNumber=request.form['pno']
    aid=request.form['aid']
    date=request.form['date']
    full_name=f_name+" "+l_name
    r=requests.get('https://api.covid19india.org/v4/data.json')
    json_data=r.json()
    cnt=json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass=((cnt/pop)*100)
    if travel_pass<30 and request.method=='POST':
        status='CONFIRMED'
        client.messages.create(to="whatsapp:+91**********",
                               from_="whatsapp:+14155238886",
                               body="Hi "+" "+full_name+" "+"Your Travel From "+" "+source_dt+" "+"To"+" "+destination_dt+" "+"Has"+
              " "+status+" On"+" "+date+" "+", Apply later")
        return render_template('user_registration_dtls.html',var=full_name,var1=email,var2=aid,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,var7=phoneNumber,
                               var8=date,var9=status)
    else:
        status = 'Not Confirmed'
        client.messages.create(to="whatsapp:+91**********",
                               from_="whatsapp:+14155238886",
                               body="Hi " + " " + full_name + "  " + "Your travel from" + source_dt + " " + "To" + " " + destination_dt + " "
                                    + "Has" + " " + status + " On" + " " + date + " " + ", Apply later")
        return render_template('user_registration_dlts.html', var=full_name, var1=email, var2=aid,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)
if __name__ == "__main__":
        app.run(port=9001, debug=True)