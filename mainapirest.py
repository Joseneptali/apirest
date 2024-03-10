#CONEXION MYSQL#
from flask import Flask, jsonify, request
import pymysql.cursors

app = Flask(__name__)

# Función para establecer la conexión a MySQL
def connection_mysql():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='',
                                 database='python',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# Endpoint para crear un nuevo usuario
@app.route('/usuarios', methods=["POST"])
def create():
    data = request.get_json()
    connection = connection_mysql()

    try:
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
                cursor.execute(sql, (data['email'], data['password']))
            connection.commit()

        return jsonify({'message': 'Creacion Exitosa'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
  
# Endpoint para listar todos los usuarios
@app.route('/usuarios', methods=['GET'])
def list():
    connection = connection_mysql()

    try:
        with connection.cursor() as cursor:
            sql = 'SELECT id, email, password FROM users'
            cursor.execute(sql)
            result = cursor.fetchall()

            return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


# Endpoint para actualizar los usuarios
@app.route('/usuarios', methods=["PUT"])
def update_user():
    data = request.get_json()
    connection = connection_mysql()

    # Verificar si los datos necesarios están presentes
    if 'id' not in data or ('email' not in data and 'password' not in data):
        return jsonify({'error': 'Se requiere id, correo o contraseña para actualizar'}), 400

    try:
        with connection.cursor() as cursor:
            # Verificar si el usuario existe
            cursor.execute("SELECT * FROM users WHERE id = %s", (data['id'],))
            user = cursor.fetchone()

            if user is None:
                return jsonify({'error': 'Usuario no encontrado'}), 404

            # Actualizar correo y contraseña si se proporcionan
            if 'correo' in data:
                cursor.execute("UPDATE users SET email = %s WHERE id = %s", (data['correo'], data['id']))
            if 'contraseña' in data:
                cursor.execute("UPDATE users SET password = %s WHERE id = %s", (data['contraseña'], data['id']))

            connection.commit()

        return jsonify({'message': 'Usuario actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Endpoint para borar los usuarios

@app.route('/usuarios', methods=["DELETE"])
def delete():
    data = request.get_json()
    connection = connection_mysql()
    
    try:
        with connection.cursor() as cursor:
            
            
            cursor.execute("DELETE FROM users WHERE id = %s", (data['id']))
           
            connection.commit()

        return jsonify({'message': 'Usuario Borrado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
