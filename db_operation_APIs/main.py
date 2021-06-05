from db_operation import db_operations
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sql/create_table', methods=['POST'])
def create_table_sql():
    host = request.json['host']
    user = request.json['user']
    password = request.json['password']
    database = request.json['database']
    table = request.json['table']
    table_structure = request.json['table_structure']

    db_obj = db_operations(host, user, password, database, table)
    return jsonify(db_obj.create_mysql_table(table_structure))


@app.route('/sql/insert_row',methods=['POST'])
def insert_record_mysql():
    host = request.json['host']
    user = request.json['user']
    password = request.json['password']
    database = request.json['database']
    table = request.json['table']
    row_structure = request.json['row_structure']

    db_obj = db_operations(host, user, password, database, table)
    return jsonify(db_obj.insert_mysql_data(row_structure))


@app.route('/sql/bulk_upload',methods = ['POST'])
def bulk_upload_mysql():
    host = request.json['host']
    user = request.json['user']
    password = request.json['password']
    database = request.json['database']
    table = request.json['table']
    file_location = request.json['file_location']

    db_obj = db_operations(host, user, password, database, table)
    return jsonify(db_obj.bulk_upload_mysql(file_location))

@app.route('/sql/update',methods = ['POST'])
def update_mysql_records():
    host = request.json['host']
    user = request.json['user']
    password = request.json['password']
    database = request.json['database']
    table = request.json['table']
    update_data = request.json['update_data']
    selection_criteria = request.json['selection_criteria']

    db_obj = db_operations(host, user, password, database, table)
    return jsonify(db_obj.update_mysql_data(update_data, selection_criteria))

@app.route('/sql/delete',methods = ['POST'])
def delete_mysql_records():
    host = request.json['host']
    user = request.json['user']
    password = request.json['password']
    database = request.json['database']
    table = request.json['table']
    selection_criteria = request.json['selection_criteria']

    db_obj = db_operations(host, user, password, database, table)
    return jsonify(db_obj.delete_mysql_data(selection_criteria))

@app.route('/sql/download_data',methods = ['POST'])
def download_data_mysql():
    host = request.json['host']
    user = request.json['user']
    password = request.json['password']
    database = request.json['database']
    table = request.json['table']
    file_location = request.json['file_location']
    selection_criteria = request.json['selection_criteria']

    db_obj = db_operations(host, user, password, database, table)
    return jsonify(db_obj.download_mysql_data(selection_criteria, file_location))





if __name__ == '__main__':
    app.run()