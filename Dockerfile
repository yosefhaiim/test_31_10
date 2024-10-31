# הגדרת בסיס התמונה עבור הקונטיינר, כאן משתמשים בתמונה של Python 3.9 בגרסה רזה
FROM python:3.9-slim

# הגדרת משתנה סביבה שמבטיח שהפלט של הפייתון לא י buffered
ENV PYTHONBUFFERED 1

# קביעת התיקייה הראשית שבה יימצא הקוד
WORKDIR /app

# העתקת קובץ הדרישות (requirements.txt) לתיקייה הראשית
COPY requirements.txt /app/

# התקנת החבילות המפורטות בקובץ requirements.txt, ללא שמירה על קבצי cache
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הקבצים של הפרויקט לתוך הקונטיינר
COPY . /app/

# חשיפת הפורט 5001 (הפורט שבו האפליקציה תאזין)
EXPOSE 5001

# הפעלת האפליקציה על ידי הרצת הקובץ app.py
CMD ["python", "app.py"]
