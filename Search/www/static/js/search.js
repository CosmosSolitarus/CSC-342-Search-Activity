function search() {
    // these params get passed to app.py for sorting and filtering
    const searchBy = document.querySelector('select[name="search-by"]').value;
    const sortBy = document.querySelector('select[name="sort-by"]').value;
    const includeExplicit = document.querySelector('input[type="checkbox"]').checked;
    const searchText = document.getElementById("searchbar").value;

    const params = {
        searchBy: searchBy,
        sortBy: sortBy,
        includeExplicit: includeExplicit,
        searchText: searchText
    };

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results'); // the #results div in home.htmml
        resultsDiv.innerHTML = '';  // clear previous results

        // loop through each track and add data to html template
        data.forEach(track => {
            // trackDiv will contain all other elements for this song and get appended to #results in home.html
            const trackDiv = document.createElement('div');

            // title and artist(s)
            const titleArtists = document.createElement('p');
            titleArtists.innerHTML = `${track.title} by ${track.artists.join(", ")}`;
            
            // genre(s)
            const genres = document.createElement('p');
            genres.innerText = `Genres: ${track.genres.join(", ")}`;

            // popularity score
            const popularity = document.createElement('p');
            popularity.innerText = `Popularity score: ${track.popularity}`;

            // duration
            const duration = document.createElement('p');
            duration.innerText = `Duration: ${track.duration_mins} minutes`;

            // spotify link
            const spotifyLink = document.createElement('a');
            spotifyLink.href = track.url;
            spotifyLink.innerText = 'Listen on Spotify';
            spotifyLink.target = '_blank';

            // append all elements to trackDiv
            trackDiv.appendChild(titleArtists);
            trackDiv.appendChild(genres);
            trackDiv.appendChild(popularity);
            trackDiv.appendChild(duration);
            trackDiv.appendChild(spotifyLink);

            // append html song info to #results
            resultsDiv.appendChild(trackDiv);
        });
    })
    .catch(error => {
        console.error('Error:', error); // just in case
    });
}
