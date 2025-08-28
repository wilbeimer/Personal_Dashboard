
import { handleAuth } from './auth.js';

const loginBtn = document.getElementById("loginBtn");
if (loginBtn) loginBtn.addEventListener("click", () => handleAuth("login", "/home", "loginError"));

const registerBtn = document.getElementById("registerBtn");
if (registerBtn) registerBtn.addEventListener("click", () => handleAuth("register", "/home", "signupError"));

const dltBtn = document.getElementById("dltBtn");
if (dltBtn) {
    dltBtn.addEventListener("click", async () => {
        const errorLabel = document.getElementById("deleteError");
        errorLabel.textContent = "";
        try {
            const response = await fetch("http://127.0.0.1:8000/users/delete_all", {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
            });
            errorLabel.textContent = response.ok ? "Deleted" : (await response.json()).detail;
        } catch {
            errorLabel.textContent = "Network error";
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const notesList = document.getElementById("notesList");
    const createNoteBtn = document.getElementById("createNoteBtn");
    const placeholder = document.getElementById("notePlaceholder");
    const noteTitle = document.getElementById("noteTitleDisplay");
    const noteContent = document.getElementById("noteContentDisplay");
    const saveStatus = document.getElementById("noteSaveStatus");

    let currentNoteId = null;
    let saveTimeout = null;

    async function loadNotes() {
        const res = await fetch("/notes/", { credentials: "include" });
        if (!res.ok) return [];
        const notes = await res.json();

        notesList.innerHTML = "";
        notes.forEach(note => {
            const li = document.createElement("li");
            li.textContent = `(${note.id}) ${note.title || "Untitled Note"}`; // include note ID
            li.dataset.id = note.id;
            li.addEventListener("click", () => openNote(note));
            notesList.appendChild(li);
        });
        return notes;
    }

    function openNote(note) {
        currentNoteId = note.id;
        placeholder.style.display = "none";
        noteTitle.style.display = "block";
        noteContent.style.display = "block";
        saveStatus.style.display = "inline";

        noteTitle.value = note.title || "Untitled Note";
        noteContent.value = note.content || "";
        saveStatus.textContent = "All changes saved.";

        Array.from(notesList.children).forEach(li => {
            li.classList.toggle("active", li.dataset.id == note.id);
        });
    }

    createNoteBtn.addEventListener("click", async () => {
        const res = await fetch("/notes/", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: "Untitled Note", content: "" }),
        });
        if (!res.ok) return;
        const note = await res.json();
        openNote(note);
        loadNotes();
    });

    async function saveNote(noteId) {
        if (!noteId) return;
        if (saveTimeout) clearTimeout(saveTimeout);
        saveTimeout = null;

        try {
            const res = await fetch(`/notes/${noteId}`, {
                method: "PUT",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: noteTitle.value,
                    content: noteContent.value,
                }),
            });

            if (res.ok) {
                saveStatus.textContent = "Saved";

                // Get updated note from server
                const updatedNote = await res.json();

                // Refresh sidebar completely
                const notes = await loadNotes();

                // Re-open the current note (so content is synced)
                const refreshedNote = notes.find(n => n.id === noteId);
                if (refreshedNote) openNote(refreshedNote);

                setTimeout(() => { saveStatus.style.display = "none"; }, 1200);
            } else {
                saveStatus.textContent = "Error saving";
            }
        } catch (err) {
            console.error(err);
            saveStatus.textContent = "Network error";
        }
    }

    function scheduleSave() {
        if (!currentNoteId) return;
        saveStatus.style.display = "inline";
        saveStatus.textContent = "Saving...";
        saveStatus.style.fontSize = "0.8em";
        if (saveTimeout) clearTimeout(saveTimeout);

        const noteId = currentNoteId; // capture current note id for timeout
        saveTimeout = setTimeout(() => saveNote(noteId), 500);
    }

    // Attach auto-save listeners once
    noteTitle.addEventListener("input", scheduleSave);
    noteContent.addEventListener("input", scheduleSave);

    loadNotes();
});

