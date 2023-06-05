from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src','templates')


app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicacion
@app.route('/')
def home():
    cursor =db.database.cursor()
    cursor.execute("SELECT * FROM bebidas")
    myresult = cursor.fetchall()
    #convertir los datos a diccionario
    insertObjet = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObjet.append(dict(zip(columnNames,record)))
    cursor.close()
    return render_template('index.html', data=insertObjet)

#Ruta para guardar los registros
@app.route('/bebidas',methods=['POST'])
def addNombre():
    nombre= request.form['nombre']
    precio= request.form['precio']
    clasificacion= request.form['clasificacion']
    marca= request.form['marca']

    if nombre and precio and clasificacion and marca:
        cursor = db.database.cursor()
        sql ="INSERT INTO bebidas (nombre,precio,id_clasificacion,id_marca) VALUES (%s,%s,%s,%s)"
        data = (nombre,precio,clasificacion,marca)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))

#ELIMINAR UN REGISTRO

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql ="DELETE FROM bebidas WHERE id=%s)"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))


#EDITAR UN REGISTRO
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre= request.form['nombre']
    precio= request.form['precio']
    clasificacion= request.form['clasificacion']
    marca= request.form['marca']

    if nombre and precio and clasificacion and marca:
        cursor = db.database.cursor()
        sql ="UPDATE bebidas SET nombre= %s,precio=%s,id_clasificacion=%s,id_marca=%s WHERE id =%s"
        data = (nombre,precio,clasificacion,marca,id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__=='__main__':
    app.run(debug=True, port=4000)

    