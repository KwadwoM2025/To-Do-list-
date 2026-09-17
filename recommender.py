from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#Import sklearn features to recommend tasks to do

from models import Todo_Items

#Gain attributes from the models file 


class Task_Recommendation_Engine:
    RECOMMENDATIONS = [
        ("Break project work into smaller steps",
        "project report presentation milestone deadline work"),
        ("Review your calendar and upcoming deadlines",
        "meeting calendar appointment schedule deadline work"),
        ("Write down your top three priorities",
        "priority planning organize focus productive work"),
        ("Reply to important messages",
        "email message client colleague communication follow up"),
        ("Take a 10-minute walk or stretch break",
        "health wellness exercise break energy rest"),
        ("Plan meals and update the grocery list",
        "food groceries shopping home meal cooking"),
        ("Spend 20 minutes learning something new",
        "learning study course practice reading skill education"),
        ("Tidy one small area of your space",
        "clean home organize tidy laundry chores"),
    ]


    def suggest(self, tasks: list[Todo_Items], extra_info: str = "") -> str:
        existing_titles = {
            " ".join(task.title.lower().split())
            for task in tasks
        }

        available = [
            recommend 
            for recommend in self.RECOMMENDATIONS
            if recommend[0].lower() not in existing_titles
        ]

        profile = " ".join(task.title for task in tasks)
        profile = f"{profile} {extra_info}".strip()

        if not profile:
            return "Write down your top 5 priorites"
        recommend_text = [
            f"{title} {keywords}"
            for title, keywords in available
        ]

        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(recommend_text + [profile])
        scores =  cosine_similarity(matrix[-1], matrix[:-1]).flatten()

        return available[scores.argmax()][0]
