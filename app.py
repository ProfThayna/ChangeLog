from flask import Flask, jsonify, request
from config import swaggerui_blueprint
from datetime import datetime
import pymysql  

app = Flask(__name__)


app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')


def get_db_connection():
    
    return pymysql.connect(host='', user='', password='', db='versionamentosoftware')

# GET - Obter todos os IDs
@app.route('/api/revnumbers', methods=['GET'])
def get_all_rev_numbers():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM ChangeLogs")
        result = cursor.fetchall()  # Obtém todas as linhas

    conn.close()

    if result:
        revnumbers = []
        for row in result:
            rev_number_data = {
                "ID": row[0],          
                "Titulo": row[1],      
                "Conteudo": row[2],    
                "DateTime": row[3].isoformat() if isinstance(row[3], datetime) else row[3],
                "Data": row[4].isoformat() if isinstance(row[4], datetime) else row[4],
                "Hora": str(row[5]),   
                "RevNumber": row[6],   
                "Major": row[7],       
                "Minor": row[8],       
                "FixPatch": row[9],    
            }
            revnumbers.append(rev_number_data)

        return jsonify(revnumbers), 200
    else:
        return jsonify({'message': 'Nenhuma versão encontrada!'}), 404

# GET - Obter através do id
@app.route('/api/revnumbers/<int:id>', methods=['GET'])
def get_rev_number(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM ChangeLogs WHERE ID = %s", (id,))
        result = cursor.fetchone()

    conn.close()

    if result:
        # Mapeia o resultado para um dicionário
        rev_number_data = {
            "ID": result[0],          
            "Titulo": result[1],     
            "Conteudo": result[2],    
            "DateTime": result[3].isoformat() if isinstance(result[3], datetime) else result[3],
            "Data": result[4].isoformat() if isinstance(result[4], datetime) else result[4],
            "Hora": str(result[5]),   
            "RevNumber": result[6],    
            "Major": result[7],       
            "Minor": result[8],        
            "FixPatch": result[9],    
        }

        return jsonify(rev_number_data), 200
    else:
        return jsonify({'message': 'RevNumber não encontrado!'}), 404

# POST - Criar uma nova versão
@app.route('/api/revnumbers', methods=['POST'])
def create_rev_number():
    data = request.json
    Titulo = data.get('Titulo')
    Conteudo = data.get('Conteudo')
    RevNumber = data.get('RevNumber')
    now = datetime.now()

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ChangeLogs (Titulo, Conteudo, DateTime, Data, Hora, RevNumber, Major, Minor, FixPatch)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (Titulo, Conteudo, now, now.date(), now.time(), RevNumber, 
              RevNumber.split('.')[0], RevNumber.split('.')[1], RevNumber.split('.')[2]))
        conn.commit()
    conn.close()

    return jsonify({'message': 'RevNumber criado com sucesso!'}), 201

# PUT - Atualiza através do ID
@app.route('/api/revnumbers/<int:id>', methods=['PUT'])
def update_rev_number(id):
    data = request.json
    Titulo = data.get('Titulo')
    Conteudo = data.get('Conteudo')
    RevNumber = data.get('RevNumber')

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE ChangeLogs 
            SET Titulo = %s, Conteudo = %s, RevNumber = %s, Major = %s, Minor = %s, FixPatch = %s
            WHERE ID = %s
        """, (Titulo, Conteudo, RevNumber, 
              RevNumber.split('.')[0], RevNumber.split('.')[1], RevNumber.split('.')[2], id))
        conn.commit()
    conn.close()

    return jsonify({'message': 'RevNumber atualizado com sucesso!'}), 200

# DELETE - Deleta através do ID
@app.route('/api/revnumbers/<int:id>', methods=['DELETE'])
def delete_rev_number(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM ChangeLogs WHERE ID = %s", (id,))
        conn.commit()
    conn.close()

    return jsonify({'message': 'RevNumber deletado com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)