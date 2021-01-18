from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = 'endpoint'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db'
 
mysql = MySQL(app)

# settings

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM prueba')
    data = cur.fetchall()
    return render_template('index.html', contactos = data)

@app.route('/add', methods=['POST'])
def Add():
    if request.method == 'POST':
        username = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO prueba (nombre, phone, email) VALUES (%s, %s, %s)', 
            (username, phone, email))

        mysql.connection.commit()

        flash('El contacto se agrego correctamente')
        return redirect(url_for('Index'))


@app.route('/edit/<string:id>')
def Edit(id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM prueba WHERE id = {id} ')
    data = cur.fetchall()

    return render_template('edit.html', contacto = data[0])

@app.route('/update/<string:id>', methods=['POST'])
def Update(id):
    if request.method == 'POST':

        username = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE prueba
            SET nombre = %s,
                phone = %s,
                email = %s
            WHERE id = %s 
        """,(username, phone, email, id))
        mysql.connection.commit()
        flash('La información ha sido actualizada')
        
        return redirect(url_for('Index'))

        

@app.route('/delete/<string:id>')
def Delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM prueba WHERE id = {id}')
    mysql.connection.commit()

    flash('El contacto ha sido eliminado')
    return redirect(url_for('Index'))

@app.route('/prueba')
def Prueba():
    return ('Esto es una prueba')

if __name__ == "__main__":
    app.run(port=4000, debug = True)    
