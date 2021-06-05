import mysql.connector as connection
import csv

import linecache
import sys


class db_operations:
    error = 0
    message = ''

    def __init__(self, host, user, password, database, table):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table

    def establish_mysql_connection(self):
        try:
            conn = connection.connect(host=self.host, user=self.user, password=self.password, use_pure=True)
            return conn

        except Exception as e:
            print(str(e))
            self.error = 1
            self.message = 'Connection Error'
            return self.error, self.message

    def create_mysql_database(self, mysql):
        try:
            cursor = mysql.cursor()
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')

        except Exception as e:
            print(str(e))
            self.error = 2
            self.message = 'Database Error'
            return self.error, self.message

    def fetch_column_and_datatype_mysql(self, table_structure):
        try:
            if type(table_structure) == dict:
                column_and_datatype = ''
                for key, val in table_structure.items():
                    column_and_datatype += key + ' ' + val + ', '
                column_and_datatype = column_and_datatype[:-2]
                return column_and_datatype
            else:
                self.error = 3
                self.message = 'Table structure should be in key value pair'

        except Exception as e:
            print(str(e))
            self.error = 3
            self.message = 'Table structure not proper'
            return self.error, self.message

    def create_mysql_table(self, table_structure):
        try:
            mysql = self.establish_mysql_connection()
            if self.error == 0:
                self.create_mysql_database(mysql)
                primary_key = next(iter(table_structure))  # first column will always become primary key
                column_and_datatype = self.fetch_column_and_datatype_mysql(table_structure)
                cursor = mysql.cursor()

                query = f'CREATE TABLE IF NOT EXISTS {self.database}.{self.table} ({column_and_datatype} ' \
                        f', PRIMARY KEY({primary_key}))'
                print(query)
                cursor.execute(query)
                self.message = 'Table created successfully'

            else:
                self.message = 'Table already exists in the database'

            return self.message

        except Exception as e:
            print(str(e))
            self.error = 4
            self.message = 'Error in Table creation'
            return self.error, self.message

    def format_insert_data_mysql(self, row_structure):
        try:
            if type(row_structure) == dict:
                insert_values = ''
                for key, val in row_structure.items():
                    if type(val) == str:
                        insert_values += '"' + str(val) + '"' + ', '
                    elif val == None:
                        val = "NULL"
                        insert_values += str(val) + ', '
                    else:
                        insert_values += str(val) + ', '
                insert_values = insert_values[:-2]
                return insert_values

        except Exception as e:
            print(str(e))
            self.error = 5
            self.message = 'row structure should be in key-value pair'
            return self.error, self.message

    def insert_mysql_data(self, row_structure):
        # assuming that db and table exists and hence we insert the record directly
        try:
            mysql = self.establish_mysql_connection()
            if self.error == 0:
                insert_values = self.format_insert_data_mysql(row_structure)
                cursor = mysql.cursor()

                query = f'INSERT INTO {self.database}.{self.table} VALUES({insert_values})'
                print(query)
                cursor.execute(query)
                cursor.execute('COMMIT')
                self.message = 'Row inserted successfully'

            else:
                self.error = 6
                self.message = 'Column-value mapping is not proper'

            return self.message

        except Exception as e:
            print(str(e))
            self.error = 6
            self.message = 'Error in Inserting record'
            return self.error, self.message

    def bulk_upload_mysql(self, file_location):
        try:
            inserted, not_inserted = 0, 0
            mysql = self.establish_mysql_connection()
            if self.error == 0:
                cursor = mysql.cursor()
                # data_csv = open(file_location, 'r')
                with open(file_location, 'r') as data:
                    next(data)
                    data_csv = csv.reader(data, delimiter='\n')
                    try:
                        for values in data_csv:
                            query = f'INSERT INTO {self.database}.{self.table} VALUES ({str(values[0])})'
                            cursor.execute(query)
                            inserted += 1

                            mysql.commit()
                        self.message = f'{inserted} records inserted successfully'

                    except Exception as e:
                        not_inserted += 1
                        self.error = 7
                        self.message = f'{not_inserted} records not inserted due to:  {str(e)}'

                return self.message

        except Exception as e:
            print(str(e))
            self.error = 7
            self.message = 'Bulk upload Error'
            return self.error, self.message

    def format_update_data_mysql(self, update_data):
        try:
            update_columns = ''
            if type(update_data) == dict:
                for key, val in update_data.items():
                    update_columns += key + ' = '
                    if type(val) == str:
                        update_columns += '"' + str(val) + '"' + ', '
                    else:
                        update_columns += str(val) + ', '
                update_columns = update_columns[:-2]
                return update_columns

            else:
                self.error = 8
                self.message = 'Update values should be given in key-value pair'

        except Exception as e:
            print(str(e))
            self.error = 8
            self.message = 'Error in update structure'

        return self.error, self.message

    def format_selection_criteria(self, selection_criteria):
        try:
            selection_columns = 'where '
            if type(selection_criteria) == dict:
                for key, val in selection_criteria.items():
                    selection_columns += key + ' = '
                    if type(val) == str:
                        selection_columns += '"' + str(val) + '"' + ' and '
                    else:
                        selection_columns += str(val) + ' and '
                selection_columns = selection_columns[:-5]
                return selection_columns

            else:
                self.error = 9
                self.message = 'Selection criteria should be in key-value pair'

        except Exception as e:
            print(str(e))
            self.error = 9
            self.message = 'Error in selection criteria'

        return self.message

    # code for printing filename, line number, line itself and exception description in class variable self.message
    def print_exception(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

    def update_mysql_data(self, update_data, selection_criteria):
        try:
            update_columns = self.format_update_data_mysql(update_data)
            selection_columns = self.format_selection_criteria(selection_criteria)
            if self.error == 0:
                mysql = self.establish_mysql_connection()
                cursor = mysql.cursor()
                query = f'UPDATE {self.database}.{self.table} SET {update_columns} {selection_columns}'
                cursor.execute(query)

                number_of_rows_affected = cursor.rowcount
                mysql.commit()

                self.message = f'{number_of_rows_affected} records updated successfully'

            else:
                self.error = 10
                self.message = 'Records not updated'

        except Exception as e:
            print(str(e))
            self.error = 10
            self.message = self.print_exception()

        return self.error, self.message

    def delete_mysql_data(self, selection_criteria):
        try:
            selection_columns = self.format_selection_criteria(selection_criteria)
            if self.error == 0:
                mysql = self.establish_mysql_connection()
                cursor = mysql.cursor()
                query = f'DELETE FROM {self.database}.{self.table} {selection_columns}'
                cursor.execute(query)

                number_of_rows_affected = cursor.rowcount
                mysql.commit()

                self.message = f'{number_of_rows_affected} records deleted successfully'
            else:
                self.error = 11
                self.message = 'Issue in deleting the records'

        except Exception as e:
            print(str(e))
            self.error = 11
            self.message = self.print_exception()

        return self.error, self.message

    def download_mysql_data(self, selection_criteria, file_location):
        try:
            if selection_criteria == "" or "*":
                selection_columns = ''
            else:
                selection_columns = self.format_selection_criteria(selection_criteria)

            if self.error == 0:
                mysql = self.establish_mysql_connection()
                cursor = mysql.cursor()
                query = f'SELECT * FROM {self.database}.{self.table} {selection_columns}'
                print(query)
                cursor.execute(query)
                result = cursor.fetchall()

                with open(file_location+'\\download_data.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(result)

                    self.message = 'Data downloaded to the csv file'

        except Exception as e:
            print(str(e))
            self.error = 12
            self.message = self.print_exception()

        return self.error, self.message
