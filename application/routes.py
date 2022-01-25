from flask.helpers import url_for
from application import app
from flask import render_template, request, redirect
from flask_mysqldb import MySQL, MySQLdb
from datetime import datetime

conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "",
                           db = "datawarehouse")

@app.route("/")

@app.route("/prediksi")
def prediksi():
    return render_template("index.html")

@app.route("/inputsample", methods=["GET", "POST"])
def inputsample():
    if request.method == "POST":
        tanggal = request.form["tanggal"]
        hasil_penjualan = request.form["hasilpenjualan"]

        cur = conn.cursor()
        cur.execute("INSERT INTO hasil_penjualan(tanggal,jumlah) VALUES (%s,%s)",(tanggal,hasil_penjualan,))
        conn.commit()
    
    return redirect(url_for('index'))

@app.route("/perhitungan", methods=["GET", "POST"])
def perhitungan():

    def perhitungan(awal,akhir):
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM hasil_penjualan")
            data1 = cur.fetchall()

            tanggalawal = datetime.strptime(awal, '%Y-%m-%d').date()
            tanggalakhir = datetime.strptime(akhir, '%Y-%m-%d').date()

            selisih = (tanggalakhir - tanggalawal).days
            selisih = int(selisih)
            print (selisih)

            # row_plus = len(data1)
            # row_min = -len(data1)
            row_plus = selisih
            row_min = -selisih

            
            data_x = []
            for x in range(row_min+1, row_plus+1,2):
                if x != (x % 2 == 0):
                    data_x.append(float(x))

            # print("x = ",data_x)


            data_y = []
            for j in data1:
                a = j['jumlah']
                data_y.append(float(a))
            
            # print("y = ",data_y)


            data_xy = []
            for i in range(len(data_x)):
                xy = data_x[i]*data_y[i]
                data_xy.append(xy)

            # print("xy = ",data_xy)


            data_x2 = []
            for i in range(len(data_x)):
                x2 = data_x[i]*data_x[i]
                data_x2.append(x2)

            # print("x2 = ",data_x2)


            jumlahY = sum(data_y)
            # print("jumlah Y = ",jumlahY)


            a = jumlahY/selisih
            # print("a = ",a)

            b = sum(data_xy)/sum(data_x2)
            # print("b = ",b)

            y = a + b * sum(data_x)
            # print("Y = ",y)

            return y

    if request.method == "POST":
        tanggalawal = request.form["tanggalawal"]
        tanggalakhir = request.form["tanggalakhir"]
        hasil = perhitungan(tanggalawal,tanggalakhir)

        
    return render_template("index.html", data = hasil) 
    

     
