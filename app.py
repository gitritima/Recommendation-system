from flask import Flask, render_template,request, flash, redirect, url_for
from get_recommendation import*
from poster import*

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recommender',methods=['GET','POST'])
def forminput():
    return render_template('form.html')


@app.route('/results', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        by = request.form['by']
        count = request.form['count']
        print(f'name: {name}, by: {by}, count: {count}')
        count = int(count)
        match by:
            case 'name':
                movies = get_recommendations(name, count=count)
            case 'word':
                movies = get_recommendations(name, count=count)
        if movies.empty:
            flash('No movies available', 'danger')
            return redirect(url_for('forminput'))
        
        if 'Movie not found' in movies.values:
            flash('Movie not found', 'danger')
            return redirect(url_for('forminput'))
        else:
            results = [movie_data_from_tmdb(movie) for movie in movies]
            return render_template('results.html', name=name, by=by, count=count, results=results)
        
    return redirect(url_for('forminput'))


if __name__ == '__main__':
    app.run()


#flask run --debug  