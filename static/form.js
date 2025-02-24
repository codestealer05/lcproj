function readForm() {
  let genres = document.getElementById("genres");
  let decade = document.getElementById("decade");
  let checkbox = document.getElementById("checkbox").checked;

  let selectedGenres = Array.from(genres.selectedOptions).map(
    (option) => option.value
  );
  if (selectedGenres.length === 0) {
    alert("Genres unselected");
    return;
  }
  let selectedDecade = parseInt(decade.value);

  console.log(selectedGenres); // Logs selected genres to the console
  alert("Selected genres: " + selectedGenres.join(", ")); // Shows an alert with selected genres

  let verticalList = "";
  for (let i = 0; i < selectedGenres.length; i++) {
    verticalList += selectedGenres[i] + "<br />";
  }

  let historyHero = document.createElement("section");
  historyHero.className = "hero is-medium is-success";
  historyHero.innerHTML = `
  <div class="hero-body">
    <p class="title">According to users of this service: </p>
      <div class="is-size-5">
        Three most popular movie genres are: <b>{{genres3 | safe}}</b> <br />
        The "golden decade" of cinematography is <b>{{decade1 | safe}}</b> <br />
        Whether a "good movie" should be longer than 2 hour is <b>{{opinion | safe}}</b>
      </div>
    </p>
  </div>
  `;

  let newHero = document.createElement("section");
  newHero.className = "hero is-small is-success";
  newHero.innerHTML = `
  <div class="hero-body">
  <p class="title">Your submission:</p>
    <div class="columns">
      <div class="column">
        <div class="is-size-5">${verticalList}</div>
      </div>
      <div class="column">
        <div class="is-size-5">${selectedDecade}</div>
      </div>
      <div class="column">
        <div class="is-size-5">${checkbox}</div>
      </div>
    </div>
  </div>
  `;

  let history = document.getElementById("history");
  //history.appendChild(newHero);

  let formData = {
    genres: selectedGenres,
    decade: selectedDecade,
    agreement: checkbox,
  };

  fetch("/form", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      response.json();
      if (response.redirected) {
        window.location.href = response.url;  // Force browser to navigate
      }})
    .then((data) => alert(data.message)) // Show success message
    .catch((error) => {
      console.error("Error:", error); // Handle any errors
    });

  //document.getElementById("poll").className = "container section disabled";


}

