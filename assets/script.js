/**
 * review_form_patch.js
 * Tambahkan script ini di contact.html, SETELAH <script src="assets/main.js">
 *
 * Fungsi: Override submit form ulasan agar kirim data ke Flask API /api/ulasan
 */

document.addEventListener("DOMContentLoaded", () => {
    const reviewForm = document.getElementById("review-form");
    if (!reviewForm) return;

    reviewForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        e.stopImmediatePropagation(); // cegah handler main.js ikut jalan

        const nama  = document.getElementById("review-name")?.value?.trim();
        const email = document.getElementById("review-email")?.value?.trim();
        const pesan = document.getElementById("review-message")?.value?.trim();

        if (!nama || !email || !pesan) {
            showNotif("Semua kolom wajib diisi.", "error");
            return;
        }

        const submitBtn = reviewForm.querySelector("button[type=submit]");
        if (submitBtn) {
            submitBtn.disabled    = true;
            submitBtn.textContent = "Mengirim…";
        }

        try {
            const res  = await fetch("/api/ulasan", {
                method : "POST",
                headers: { "Content-Type": "application/json" },
                body   : JSON.stringify({ nama, email, pesan })
            });

            const json = await res.json();

            if (res.ok && json.sukses) {
                showNotif("✅ " + json.pesan, "success");
                reviewForm.reset();
            } else {
                showNotif("❌ " + (json.pesan || "Gagal mengirim ulasan."), "error");
            }
        } catch (err) {
            console.error(err);
            showNotif("❌ Tidak dapat menghubungi server.", "error");
        } finally {
            if (submitBtn) {
                submitBtn.disabled    = false;
                submitBtn.textContent = "Kirim Ulasan";
            }
        }
    }, true); // capture phase → jalan sebelum handler lain


    // ── Notifikasi inline di bawah form ──────────────────────────────────
    function showNotif(msg, type = "success") {
        // Coba pakai #notification bawaan main.js dulu
        const notifEl = document.getElementById("notification");
        if (notifEl) {
            const p = notifEl.querySelector("p");
            if (p) p.textContent = msg;
            notifEl.style.display = "block";
            notifEl.style.background = type === "success" ? "#16a34a" : "#dc2626";
            setTimeout(() => { notifEl.style.display = "none"; }, 3500);
            return;
        }

        // Fallback: buat elemen sementara
        const toast = document.createElement("div");
        toast.textContent = msg;
        toast.style.cssText = `
            position:fixed; bottom:28px; left:50%; transform:translateX(-50%);
            padding:12px 24px; border-radius:24px; font-size:0.88rem;
            font-family:'Poppins',sans-serif; font-weight:500;
            color:#fff; z-index:9999; pointer-events:none;
            background: ${type === "success" ? "#16a34a" : "#dc2626"};
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3500);
    }
});
