function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
          headers: { "Content-Type": "application/json" },
    })
    .then((response) => {
        if (response.ok) {
            document.getElementById(`note-${noteId}`).remove();
            alert("Note deleted successfully.");
        } else {
            alert("Failed to delete note.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred.");
    }).then((_res) => {
        window.location.href="/notes";
    });
}

function deleteImage(filename) {
    if (confirm("Are you sure you want to delete this image?")) {
        fetch("/delete-image", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ filename: filename }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Image deleted successfully.");
                window.location.reload(); // Refresh the page to update the list
            } else {
                alert(data.error || "An error occurred while deleting the image.");
            }
        }).then((_res) => {
            window.location.href="/imagefiles";
        });
    }
}
function deleteTextfile(filename) {
    if (confirm("Are you sure you want to delete this file?")) {
        fetch("/delete_textfile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ filename: filename }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("File deleted successfully.");
                window.location.reload(); // Refresh the page to update the list
            } else {
                alert(data.error || "An error occurred while deleting the file.");
            }
        }).then((_res) => {
            window.location.href="/textfiles";
        });
    }
}
