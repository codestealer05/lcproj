// Function to read form data and handle submission
function readForm() {
  // Get the selected genres, decade, and checkbox value from the form
  let genres = document.getElementById("genres");
  let decade = document.getElementById("decade");
  let checkbox = document.getElementById("checkbox").checked;

  // Convert selected genres to an array of values
  let selectedGenres = Array.from(genres.selectedOptions).map(
    (option) => option.value
  );

  // Check if no genres are selected and alert the user
  if (selectedGenres.length === 0) {
    alert("Genres unselected");
    return;
  }

  // Get the selected decade value and convert it to an integer
  let selectedDecade = parseInt(decade.value);

  // Log selected genres to the console and show an alert with selected genres
  console.log(selectedGenres);
  alert("Selected genres: " + selectedGenres.join(", "));

  // Create a vertical list of selected genres
  let verticalList = "";
  for (let i = 0; i < selectedGenres.length; i++) {
    verticalList += selectedGenres[i] + "<br />";
  }

  // Create a new section element for displaying user submission history
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

  // Create a new section element for displaying the user's submission
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

  // Get the history element and append the new submission section (commented out as it was moved to python)
  //let history = document.getElementById("history");
  //history.appendChild(newHero);

  // Create an object with the form data
  let formData = {
    genres: selectedGenres,
    decade: selectedDecade,
    agreement: checkbox,
  };

  // Send the form data to the server using a POST request
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
        window.location.href = response.url; // Force browser to navigate
      }
    })
    .then((data) => alert(data.message)) // Show success message
    .catch((error) => {
      console.error("Error:", error); // Handle any errors
    });

  // Optionally disable the form after submission (commented out as it was moved to python)
  //document.getElementById("poll").className = "container section disabled";
}
