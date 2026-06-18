// Modal
function openModal(id) {
  document.getElementById(id).classList.add("open");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("open");
}

function openEditModal(id, name, location, capacity, facilities, status) {
  document.getElementById("edit-name").value = name;
  document.getElementById("edit-location").value = location;
  document.getElementById("edit-capacity").value = capacity;
  document.getElementById("edit-facilities").value = facilities;
  document.getElementById("edit-status").value = status;
  document.getElementById("edit-form").action = `/admin/rooms/edit/${id}`;
  openModal("modal-edit");
}

// Close modal on overlay click
document.addEventListener("click", function (e) {
  if (e.target.classList.contains("modal-overlay")) {
    e.target.classList.remove("open");
  }
});

function openImagePreview(src, name) {
  document.getElementById("preview-img").src = src;
  document.getElementById("preview-title").textContent = name;
  openModal("modal-image");
}

// Filter bookings table
document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const status = this.dataset.status;

    // update active button
    document
      .querySelectorAll(".filter-btn")
      .forEach((b) => b.classList.remove("active"));
    this.classList.add("active");

    // filter rows
    document.querySelectorAll("tbody tr[data-status]").forEach((row) => {
      if (status === "all" || row.dataset.status === status) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  });
});
