from flask import Flask, request, render_template
import logging
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
mysql_config = {
    'host': 'db',
    'user': 'wordpress',
    'password': 'abc@123',
    'database': 'wordpress'
}

@app.route('/')
def index():
    """
    Renders the index.html template.

    Returns:
        str: The rendered HTML template.
    """
    return render_template('index.html')

@app.route('/save_word', methods=['POST'])
def save_word():
    """
    Saves a word to the MySQL database.

    Returns:
        str: A success message if the word is saved successfully, or an error message if there is an error.
    """
    if request.method == 'POST':
        word = request.form['word']
        logging.info(f'Word to save: {word}')
        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO words (word) VALUES (%s)", (word,))
            connection.commit()
            return f'The word "{word}" has been saved successfully!'
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            if 'connection' in locals():
                connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
