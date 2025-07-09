const eventList = document.getElementById("events-list");

async function fetchEvents() {
  try {
    const response = await fetch("/events");
    const data = await response.json();

    // Clear previous list
    eventList.innerHTML = "";

    // Append each event message
    data.forEach(event => {
      const li = document.createElement("li");
      li.textContent = event.message;
      eventList.appendChild(li);
    });

  } catch (error) {
    console.error("Error fetching events:", error);
  }
}

// Initial call
fetchEvents();

// Poll every 15 seconds
setInterval(fetchEvents, 15000);
