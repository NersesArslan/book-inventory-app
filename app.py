from flask import Flask, render_template, request, redirect, url_for
import uuid
app = Flask(__name__)

entries = []


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    title = request.form.get('title')
    author = request.form.get('author')
    entry_id = str(uuid.uuid4())
    entries.append({
        'id': entry_id,
        'title': title,
        'author': author
    })

    return redirect(url_for('entries_page'))


@app.route('/entries')
def entries_page():
    return render_template('entries.html', entries=entries)


@app.route('/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):
    global entries
    entries = [entry for entry in entries if entry['id'] != entry_id]
    return redirect(url_for('entries_page'))


if __name__ == '__main__':
    app.run(debug=True)
