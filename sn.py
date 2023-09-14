from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite Database Initialization
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()

    return render_template('index.html', notes=notes)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute('UPDATE notes SET title=?, content=? WHERE id=?', (title, content, note_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    conn.close()
    return render_template('edit.html', note=note)


if __name__ == '__main__':
    app.run(debug=True)