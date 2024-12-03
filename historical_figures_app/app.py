from flask import Flask, render_template, request
import wikipediaapi

# Flask application
app = Flask(__name__)

class HistoricalFigureApp:
    def __init__(self):
        # Specify a custom User-Agent for Wikipedia
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent="HistoricalFiguresApp/1.0 (https://example.com; contact@example.com)"
        )

    def fetch_historical_figure(self, name):
        """Fetch details of a historical figure from Wikipedia."""
        page = self.wiki.page(name)
        if page.exists():
            # Extract the summary (biography)
            biography = page.summary

            # Extract birth, death, and occupation from the page text
            birth = self.extract_detail(page.text, r"born\s*(?:on)?\s*([\w\s,]+)")
            death = self.extract_detail(page.text, r"died\s*(?:on)?\s*([\w\s,]+)")
            occupation = self.extract_occupation(page.text)

            return {
                "name": name,
                "biography": biography,
                "birth": birth if birth else "Birth date not available",
                "death": death if death else "Death date not available",
                "occupation": occupation if occupation else "Occupation not available",
            }
        else:
            return None

    def extract_detail(self, text, pattern):
        """Extract a detail (e.g., birth or death) using a regular expression."""
        import re
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def extract_occupation(self, text):
        """Extract occupation from the text."""
        patterns = [r"occupation\s*[:\-]?\s*([\w\s]+)", r"profession\s*[:\-]?\s*([\w\s]+)"]
        for pattern in patterns:
            occupation = self.extract_detail(text, pattern)
            if occupation:
                return occupation
        return None


# Initialize the HistoricalFigureApp class
historical_app = HistoricalFigureApp()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/biography", methods=["POST"])
def get_biography():
    name = request.form.get("name")  # Get the name from the form
    biography = historical_app.fetch_historical_figure(name)

    if biography:
        return render_template("biography.html", biography=biography)
    return render_template("error.html", message=f"No information found for {name}")

if __name__ == "__main__":
    app.run(debug=True)
