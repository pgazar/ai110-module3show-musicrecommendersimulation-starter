"""Simple Tkinter UI for the RhythmPulse music recommender."""

from pathlib import Path
import tkinter as tk
from tkinter import ttk

from .recommender import load_songs, recommend_songs


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "songs.csv"


class RhythmPulseUI:
    """Minimal desktop UI for exploring recommendations."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("RhythmPulse 1.0")
        self.root.geometry("860x640")
        self.root.minsize(760, 560)

        self.songs = load_songs(str(DATA_PATH))
        self.genres = sorted({song["genre"] for song in self.songs})
        self.moods = sorted({song["mood"] for song in self.songs})

        self.genre_var = tk.StringVar(value="pop")
        self.mood_var = tk.StringVar(value="happy")
        self.energy_var = tk.DoubleVar(value=0.80)
        self.valence_var = tk.DoubleVar(value=0.82)
        self.danceability_var = tk.DoubleVar(value=0.78)
        self.acousticness_var = tk.DoubleVar(value=0.20)
        self.tempo_var = tk.IntVar(value=122)
        self.k_var = tk.IntVar(value=5)

        self._build_layout()
        self.update_recommendations()

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        title = ttk.Label(
            container,
            text="RhythmPulse 1.0",
            font=("Helvetica", 22, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            container,
            text="Pick a vibe and get quick song recommendations.",
        )
        subtitle.pack(anchor="w", pady=(4, 12))

        controls = ttk.LabelFrame(container, text="User Preferences", padding=12)
        controls.pack(fill="x")

        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=1)

        self._add_combobox(controls, "Genre", self.genre_var, self.genres, 0, 0)
        self._add_combobox(controls, "Mood", self.mood_var, self.moods, 0, 2)
        self._add_scale(controls, "Energy", self.energy_var, 1, 0)
        self._add_scale(controls, "Valence", self.valence_var, 1, 2)
        self._add_scale(controls, "Danceability", self.danceability_var, 2, 0)
        self._add_scale(controls, "Acousticness", self.acousticness_var, 2, 2)

        ttk.Label(controls, text="Tempo BPM").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=(10, 0)
        )
        ttk.Spinbox(
            controls,
            from_=50,
            to=200,
            textvariable=self.tempo_var,
            width=8,
        ).grid(row=3, column=1, sticky="w", pady=(10, 0))

        ttk.Label(controls, text="Top K").grid(
            row=3, column=2, sticky="w", padx=(16, 8), pady=(10, 0)
        )
        ttk.Spinbox(
            controls,
            from_=1,
            to=10,
            textvariable=self.k_var,
            width=6,
        ).grid(row=3, column=3, sticky="w", pady=(10, 0))

        button_row = ttk.Frame(container)
        button_row.pack(fill="x", pady=(12, 10))

        ttk.Button(
            button_row,
            text="Get Recommendations",
            command=self.update_recommendations,
        ).pack(side="left")

        ttk.Button(
            button_row,
            text="Reset to Pop Profile",
            command=self.reset_defaults,
        ).pack(side="left", padx=(8, 0))

        results_frame = ttk.LabelFrame(container, text="Recommendations", padding=12)
        results_frame.pack(fill="both", expand=True)

        self.results_text = tk.Text(
            results_frame,
            wrap="word",
            font=("Menlo", 12),
            padx=8,
            pady=8,
        )
        self.results_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical",
            command=self.results_text.yview,
        )
        scrollbar.pack(side="right", fill="y")
        self.results_text.configure(yscrollcommand=scrollbar.set)

    def _add_combobox(
        self,
        parent: ttk.Frame,
        label: str,
        variable: tk.StringVar,
        values: list[str],
        row: int,
        column: int,
    ) -> None:
        ttk.Label(parent, text=label).grid(
            row=row, column=column, sticky="w", padx=(0, 8), pady=6
        )
        combo = ttk.Combobox(parent, textvariable=variable, values=values, state="readonly")
        combo.grid(row=row, column=column + 1, sticky="ew", pady=6)

    def _add_scale(
        self,
        parent: ttk.Frame,
        label: str,
        variable: tk.DoubleVar,
        row: int,
        column: int,
    ) -> None:
        ttk.Label(parent, text=label).grid(
            row=row, column=column, sticky="w", padx=(0, 8), pady=6
        )
        scale_frame = ttk.Frame(parent)
        scale_frame.grid(row=row, column=column + 1, sticky="ew", pady=6)
        scale_frame.columnconfigure(0, weight=1)

        scale = ttk.Scale(
            scale_frame,
            variable=variable,
            from_=0.0,
            to=1.0,
            orient="horizontal",
        )
        scale.grid(row=0, column=0, sticky="ew")

        value_label = ttk.Label(scale_frame, width=5)
        value_label.grid(row=0, column=1, padx=(8, 0))

        def refresh_label(*_: object) -> None:
            value_label.config(text=f"{variable.get():.2f}")

        variable.trace_add("write", refresh_label)
        refresh_label()

    def reset_defaults(self) -> None:
        self.genre_var.set("pop")
        self.mood_var.set("happy")
        self.energy_var.set(0.80)
        self.valence_var.set(0.82)
        self.danceability_var.set(0.78)
        self.acousticness_var.set(0.20)
        self.tempo_var.set(122)
        self.k_var.set(5)
        self.update_recommendations()

    def update_recommendations(self) -> None:
        prefs = {
            "genre": self.genre_var.get(),
            "mood": self.mood_var.get(),
            "energy": round(self.energy_var.get(), 2),
            "valence": round(self.valence_var.get(), 2),
            "danceability": round(self.danceability_var.get(), 2),
            "acousticness": round(self.acousticness_var.get(), 2),
            "tempo_bpm": self.tempo_var.get(),
        }
        recommendations = recommend_songs(prefs, self.songs, k=self.k_var.get())

        lines = [
            f"Genre: {prefs['genre']}",
            f"Mood: {prefs['mood']}",
            (
                "Targets: "
                f"energy={prefs['energy']:.2f}, "
                f"valence={prefs['valence']:.2f}, "
                f"danceability={prefs['danceability']:.2f}, "
                f"acousticness={prefs['acousticness']:.2f}, "
                f"tempo={prefs['tempo_bpm']}"
            ),
            "",
        ]

        for index, (song, score, explanation) in enumerate(recommendations, start=1):
            lines.append(f"{index}. {song['title']} - {song['artist']}")
            lines.append(
                f"   Score: {score:.2f} | {song['genre']} | {song['mood']}"
            )
            lines.append(f"   Why: {explanation}")
            lines.append("")

        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", "\n".join(lines))


def main() -> None:
    root = tk.Tk()
    RhythmPulseUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
